"""Module for competition_format adapter."""

from abc import ABC, abstractmethod
from typing import Any


class Adapter(ABC):
    """Class representing an adapter interface."""

    @classmethod
    @abstractmethod
    async def get_all_competition_formats(
        cls: Any, db: Any
    ) -> list:  # pragma: no cover
        """Get all competition_formats function."""
        raise NotImplementedError from None

    @classmethod
    @abstractmethod
    async def create_competition_format(
        cls: Any, db: Any, competition_format: dict
    ) -> str:  # pragma: no cover
        """Create competition_format function."""
        raise NotImplementedError from None

    @classmethod
    @abstractmethod
    async def get_competition_format_by_id(
        cls: Any, db: Any, competition_format_id: str
    ) -> dict:  # pragma: no cover
        """Get competition_format by id function."""
        raise NotImplementedError from None

    @classmethod
    @abstractmethod
    async def get_competition_format_by_name(
        cls: Any, db: Any, name: str
    ) -> dict:  # pragma: no cover
        """Get competition_format function."""
        raise NotImplementedError from None

    @classmethod
    @abstractmethod
    async def update_competition_format(
        cls: Any, db: Any, competition_format_id: str, competition_format: dict
    ) -> str | None:  # pragma: no cover
        """Get competition_format function."""
        raise NotImplementedError from None

    @classmethod
    @abstractmethod
    async def delete_competition_format(
        cls: Any, db: Any, competition_format_id: str
    ) -> str | None:  # pragma: no cover
        """Get competition_format function."""
        raise NotImplementedError from None
