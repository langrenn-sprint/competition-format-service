"""Module for competition_format adapter."""

import logging
from typing import Any

from .adapter import Adapter


class CompetitionFormatsAdapter(Adapter):
    """Class representing an adapter for competition_formats."""

    logger = logging.getLogger(
        "competition_format_service.competition_formats_adapter.CompetitionFormatsAdapter"
    )

    @classmethod
    async def get_all_competition_formats(
        cls: Any, db: Any
    ) -> list[dict]:  # pragma: no cover
        """Get all competition_formats function."""
        cursor = db.competition_formats_collection.find()
        return await cursor.to_list(None)

    @classmethod
    async def create_competition_format(
        cls: Any, db: Any, competition_format: dict
    ) -> str:  # pragma: no cover
        """Create competition_format function."""
        return await db.competition_formats_collection.insert_one(competition_format)

    @classmethod
    async def get_competition_format_by_id(
        cls: Any, db: Any, competition_format_id: str
    ) -> dict:  # pragma: no cover
        """Get competition_format by idfunction."""
        return await db.competition_formats_collection.find_one(
            {"id": competition_format_id}
        )

    @classmethod
    async def get_competition_formats_by_name(
        cls: Any, db: Any, competition_format_name: str
    ) -> list[dict]:  # pragma: no cover
        """Get competition_format by name function."""
        cls.logger.debug(f"Got request for name {competition_format_name}.")
        competition_formats: list = []
        query = {"$regex": f".*{competition_format_name}.*", "$options": "i"}
        cls.logger.debug(f"Query: {query}.")
        cursor = db.competition_formats_collection.find({"name": query})
        for competition_format in await cursor.to_list(None):
            cls.logger.debug(f"cursor - competition_format: {competition_format}")
            competition_formats.append(competition_format)
        return competition_formats

    @classmethod
    async def update_competition_format(
        cls: Any, db: Any, competition_format_id: str, competition_format: dict
    ) -> str | None:  # pragma: no cover
        """Get competition_format function."""
        return await db.competition_formats_collection.replace_one(
            {"id": competition_format_id}, competition_format
        )

    @classmethod
    async def delete_competition_format(
        cls: Any, db: Any, competition_format_id: str
    ) -> str | None:  # pragma: no cover
        """Get competition_format function."""
        return await db.competition_formats_collection.delete_one(
            {"id": competition_format_id}
        )
