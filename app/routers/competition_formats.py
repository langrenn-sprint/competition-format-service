"""Resource module for competition_formats resources."""

import logging
import os
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response

from app.adapters import CompetitionFormatsAdapter
from app.authorization import RoleChecker, UserRole
from app.models import CompetitionFormatUnion
from app.services import (
    CompetitionFormatAlreadyExistError,
    CompetitionFormatNotFoundError,
    CompetitionFormatsService,
    IllegalValueError,
    ValidationError,
)

HOST_SERVER = os.getenv("HOST_SERVER", "localhost")
HOST_PORT = os.getenv("HOST_PORT", "8080")
BASE_URL = f"http://{HOST_SERVER}:{HOST_PORT}"


logger = logging.getLogger(
    "competition_format_service.competition_formats_view.CompetitionFormatsView"
)

router = APIRouter()


@router.get("/competition-formats")
async def get(
    name: Annotated[
        str | None,
        Query(description="The name of the competition format"),
    ] = None,
) -> list[CompetitionFormatUnion]:
    """Get all competition formats."""
    if name:
        return await CompetitionFormatsAdapter.get_competition_formats_by_name(name)

    return await CompetitionFormatsAdapter.get_all_competition_formats()


@router.post(
    "/competition-formats",
    dependencies=[Depends(RoleChecker([UserRole.Admin]))],
)
async def post(
    competition_format: CompetitionFormatUnion,
) -> Response:
    """Post route function."""
    logger.debug(
        f"Got create request for competition_format {competition_format} of type {type(competition_format)}"
    )
    try:
        competition_format_id = (
            await CompetitionFormatsService.create_competition_format(
                competition_format
            )
        )
    except CompetitionFormatAlreadyExistError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e)) from e
    except ValidationError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e
    if competition_format_id:
        logger.debug(
            f"inserted document with competition_format_id {competition_format_id}"
        )
        headers = {"Location": f"/competition-formats/{competition_format_id}"}

        return Response(status_code=HTTPStatus.CREATED, headers=headers)
    raise HTTPException(
        HTTPStatus.BAD_REQUEST, detail="Error when creating competition format."
    ) from None


@router.get("/competition-formats/{competition_format_id}")
async def get_by_id(
    competition_format_id: UUID,
) -> CompetitionFormatUnion:
    """Get competition-format by id function."""
    logger.debug(f"Got get request for competition_format {competition_format_id.hex}")
    competition_format = await CompetitionFormatsAdapter.get_competition_format_by_id(
        competition_format_id
    )
    if not competition_format:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Competition-format with id {competition_format_id} is not found.",
        )
    logger.debug(f"Got competition_format: {competition_format}")
    return competition_format


@router.put(
    "/competition-formats/{competition_format_id}",
    dependencies=[Depends(RoleChecker([UserRole.Admin]))],
)
async def put(
    competition_format_id: UUID,
    competition_format: CompetitionFormatUnion,
) -> Response:
    """Put route function."""
    logger.debug(
        f"Got request-body {competition_format} for {competition_format_id.hex} of type {type(competition_format)}"
    )
    try:
        await CompetitionFormatsService.update_competition_format(
            competition_format_id, competition_format
        )
    except (ValidationError, IllegalValueError) as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e
    except CompetitionFormatNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e)) from e
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.delete(
    "/competition-formats/{competition_format_id}",
    dependencies=[Depends(RoleChecker([UserRole.Admin]))],
)
async def delete(competition_format_id: UUID) -> Response:
    """Delete route function."""
    logger.debug(
        f"Got delete request for competition_format {competition_format_id.hex}"
    )

    try:
        await CompetitionFormatsService.delete_competition_format(competition_format_id)
    except CompetitionFormatNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e)) from e
    return Response(status_code=HTTPStatus.NO_CONTENT)
