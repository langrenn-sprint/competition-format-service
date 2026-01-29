"""Module for competition_format adapter."""

import logging
from typing import Any
from uuid import UUID

from pydantic import TypeAdapter

from app.models import CompetitionFormatUnion


class CompetitionFormatsAdapter:
    """Class representing an adapter for competition_formats."""

    database: Any
    logger: logging.Logger

    @classmethod
    async def init(cls, database: Any) -> None:  # pragma: no cover
        """Initialize class properties."""
        cls.database = database
        cls.logger = logging.getLogger(__name__)

    @classmethod
    async def get_all_competition_formats(
        cls: Any,
    ) -> list[CompetitionFormatUnion]:  # pragma: no cover
        """Get all competition_formats function."""
        cursor = cls.database.competition_formats_collection.find()
        return [
            TypeAdapter(CompetitionFormatUnion).validate_python(competition_format)
            for competition_format in await cursor.to_list(None)
        ]

    @classmethod
    async def create_competition_format(
        cls: Any, competition_format: CompetitionFormatUnion
    ) -> str:  # pragma: no cover
        """Create competition_format function."""
        return await cls.database.competition_formats_collection.insert_one(
            competition_format.model_dump()
        )

    @classmethod
    async def get_competition_format_by_id(
        cls: Any, competition_format_id: UUID
    ) -> CompetitionFormatUnion | None:  # pragma: no cover
        """Get competition_format by id function."""
        result = await cls.database.competition_formats_collection.find_one(
            {"id": competition_format_id}
        )
        return (
            TypeAdapter(CompetitionFormatUnion).validate_python(result)
            if result
            else None
        )

    @classmethod
    async def get_competition_formats_by_name(
        cls: Any, competition_format_name: str
    ) -> list[CompetitionFormatUnion]:  # pragma: no cover
        """Get competition_format by name function."""
        query = {"$regex": f".*{competition_format_name}.*", "$options": "i"}
        cls.logger.debug(f"Query: {query}.")
        cursor = cls.database.competition_formats_collection.find({"name": query})
        return [
            TypeAdapter(CompetitionFormatUnion).validate_python(competition_format)
            for competition_format in await cursor.to_list(None)
        ]

    @classmethod
    async def update_competition_format(
        cls: Any,
        competition_format_id: UUID,
        competition_format: CompetitionFormatUnion,
    ) -> str | None:  # pragma: no cover
        """Get competition_format function."""
        return await cls.database.competition_formats_collection.replace_one(
            {"id": competition_format_id}, competition_format.model_dump()
        )

    @classmethod
    async def delete_competition_format(
        cls: Any, competition_format_id: UUID
    ) -> str | None:  # pragma: no cover
        """Get competition_format function."""
        return await cls.database.competition_formats_collection.delete_one(
            {"id": competition_format_id}
        )
