"""Resource module for competition_formats resources."""

import json
import logging
import os

from aiohttp import hdrs
from aiohttp.web import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPUnprocessableEntity,
    Response,
    View,
)
from dotenv import load_dotenv
from multidict import MultiDict

from competition_format_service.adapters import UsersAdapter
from competition_format_service.models import (
    IndividualSprintFormat,
    IntervalStartFormat,
)
from competition_format_service.services import (
    CompetitionFormatAlreadyExistError,
    CompetitionFormatNotFoundError,
    CompetitionFormatsService,
    ValidationError,
)

from .utils import extract_token_from_request

load_dotenv()
HOST_SERVER = os.getenv("HOST_SERVER", "localhost")
HOST_PORT = os.getenv("HOST_PORT", "8080")
BASE_URL = f"http://{HOST_SERVER}:{HOST_PORT}"


class CompetitionFormatsView(View):
    """Class representing competition_formats resource."""

    async def get(self) -> Response:
        """Get route function."""
        db = self.request.app["db"]

        competition_formats = []
        if "name" in self.request.rel_url.query:
            name = self.request.rel_url.query["name"]
            competition_formats = (
                await CompetitionFormatsService.get_competition_formats_by_name(
                    db, name
                )
            )
        else:
            competition_formats = (
                await CompetitionFormatsService.get_all_competition_formats(db)
            )
        # Create json representation
        result = [_c.to_dict() for _c in competition_formats]
        body = json.dumps(result, default=str, ensure_ascii=False)
        return Response(status=200, body=body, content_type="application/json")

    async def post(self) -> Response:
        """Post route function."""
        db = self.request.app["db"]
        token = extract_token_from_request(self.request)
        try:
            await UsersAdapter.authorize(token, roles=["admin", "event-admin"])
        except Exception as e:
            raise e from e

        body = await self.request.json()
        logging.debug(
            f"Got create request for competition_format {body} of type {type(body)}"
        )
        try:
            competition_format: IndividualSprintFormat | IntervalStartFormat
            if body["datatype"] == "interval_start":
                competition_format = IntervalStartFormat.from_dict(body)
            elif body["datatype"] == "individual_sprint":
                competition_format = IndividualSprintFormat.from_dict(body)
            else:
                raise HTTPBadRequest(
                    reason=f"Unknown datatype {body['datatype']}"
                ) from None
        except (KeyError, ValueError) as e:
            raise HTTPUnprocessableEntity(reason=str(e)) from e

        try:
            competition_format_id = (
                await CompetitionFormatsService.create_competition_format(
                    db, competition_format
                )
            )
        except CompetitionFormatAlreadyExistError as e:
            raise HTTPBadRequest(reason=str(e)) from e
        except ValidationError as e:
            raise HTTPUnprocessableEntity(reason=str(e)) from e
        if competition_format_id:
            logging.debug(
                f"inserted document with competition_format_id {competition_format_id}"
            )
            headers = MultiDict(
                [
                    (
                        hdrs.LOCATION,
                        f"{BASE_URL}/competition-formats/{competition_format_id}",
                    )
                ]
            )

            return Response(status=201, headers=headers)
        raise HTTPBadRequest from None


class CompetitionFormatView(View):
    """Class representing a single competition_format resource."""

    async def get(self) -> Response:
        """Get route function."""
        db = self.request.app["db"]

        competition_format_id = self.request.match_info["id"]
        logging.debug(f"Got get request for competition_format {competition_format_id}")

        try:
            competition_format = (
                await CompetitionFormatsService.get_competition_format_by_id(
                    db, competition_format_id
                )
            )
        except CompetitionFormatNotFoundError as e:
            raise HTTPNotFound(reason=str(e)) from e
        logging.debug(f"Got competition_format: {competition_format}")
        body = competition_format.to_json()
        return Response(status=200, body=body, content_type="application/json")

    async def put(self) -> Response:
        """Put route function."""
        db = self.request.app["db"]
        token = extract_token_from_request(self.request)
        try:
            await UsersAdapter.authorize(token, roles=["admin", "event-admin"])
        except Exception as e:
            raise e from e

        body = await self.request.json()
        competition_format_id = self.request.match_info["id"]
        logging.debug(
            f"Got request-body {body} for {competition_format_id} of type {type(body)}"
        )
        body = await self.request.json()
        logging.debug(
            f"Got put request for competition_format {body} of type {type(body)}"
        )
        try:
            competition_format: IndividualSprintFormat | IntervalStartFormat
            if body["datatype"] == "interval_start":
                competition_format = IntervalStartFormat.from_dict(body)
            elif body["datatype"] == "individual_sprint":
                competition_format = IndividualSprintFormat.from_dict(body)
            else:
                raise HTTPBadRequest(
                    reason=f"Unknown datatype {body['datatype']}"
                ) from None
        except (KeyError, ValueError) as e:
            raise HTTPUnprocessableEntity(reason=str(e)) from e

        try:
            await CompetitionFormatsService.update_competition_format(
                db, competition_format_id, competition_format
            )
        except ValidationError as e:
            raise HTTPUnprocessableEntity(reason=str(e)) from e
        except CompetitionFormatNotFoundError as e:
            raise HTTPNotFound(reason=str(e)) from e
        return Response(status=204)

    async def delete(self) -> Response:
        """Delete route function."""
        db = self.request.app["db"]
        token = extract_token_from_request(self.request)
        try:
            await UsersAdapter.authorize(token, roles=["admin", "event-admin"])
        except Exception as e:
            raise e from e

        competition_format_id = self.request.match_info["id"]
        logging.debug(
            f"Got delete request for competition_format {competition_format_id}"
        )

        try:
            await CompetitionFormatsService.delete_competition_format(
                db, competition_format_id
            )
        except CompetitionFormatNotFoundError as e:
            raise HTTPNotFound(reason=str(e)) from e
        return Response(status=204)
