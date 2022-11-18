"""Module for competition_formats service."""
from datetime import time
import logging
from typing import Any, List, Optional, Union
import uuid

from competition_format_service.adapters import CompetitionFormatsAdapter
from competition_format_service.models import (
    CompetitionFormat,
    IndividualSprintFormat,
    IntervalStartFormat,
)
from .exceptions import (
    CompetitionFormatAllreadyExistError,
    CompetitionFormatNotFoundError,
    IllegalValueError,
    InvalidDateFormatError,
    ValidationError,
)


def create_id() -> str:  # pragma: no cover
    """Creates an uuid."""
    return str(uuid.uuid4())


class CompetitionFormatsService:
    """Class representing a service for competition_formats."""

    @classmethod
    async def get_all_competition_formats(cls: Any, db: Any) -> List[CompetitionFormat]:
        """Get all competition_formats function."""
        competition_formats: List[CompetitionFormat] = []
        _competition_formats = (
            await CompetitionFormatsAdapter.get_all_competition_formats(db)
        )
        for e in _competition_formats:
            if e["datatype"] == "interval_start":
                competition_formats.append(IntervalStartFormat.from_dict(e))
            elif e["datatype"] == "individual_sprint":
                competition_formats.append(IndividualSprintFormat.from_dict(e))
        _s = sorted(
            competition_formats,
            key=lambda k: (k.name,),
            reverse=False,
        )
        return _s

    @classmethod
    async def create_competition_format(
        cls: Any,
        db: Any,
        competition_format: Union[IndividualSprintFormat, IntervalStartFormat],
    ) -> Optional[str]:
        """Create competition_format function.

        Args:
            db (Any): the db
            competition_format (CompetitionFormat): a competition_format instanse to be created

        Returns:
            Optional[str]: The id of the created competition_format. None otherwise.

        Raises:
            CompetitionFormatAllreadyExistError: A format with the same name allready exist
            ValidationError: input object has illegal values
        """
        # Validate that the id is not set:
        if competition_format.id:
            raise ValidationError(
                "Cannot create competition-format with input id."
            ) from None
        # Check if it exists:
        _competition_formats = (
            await CompetitionFormatsAdapter.get_competition_formats_by_name(
                db, competition_format.name
            )
        )
        if _competition_formats:
            raise CompetitionFormatAllreadyExistError(
                f"Competition-format with name {competition_format.name} allready exist."
            ) from None
        # create id
        id = create_id()
        competition_format.id = id

        # Validation:
        try:
            await validate_competition_format(competition_format)
        except ValidationError as e:
            raise e from e

        # Sort the race_configs:
        if type(competition_format) == IndividualSprintFormat:
            competition_format.race_config_non_ranked.sort(
                key=lambda k: (k.max_no_of_contestants,),
                reverse=False,
            )
            competition_format.race_config_ranked.sort(
                key=lambda k: (k.max_no_of_contestants,),
                reverse=False,
            )

        # insert new competition_format
        new_competition_format = competition_format.to_dict()
        result = await CompetitionFormatsAdapter.create_competition_format(
            db, new_competition_format
        )
        logging.debug(f"inserted competition_format with id: {id}")
        if result:
            return id
        return None

    @classmethod
    async def get_competition_format_by_id(
        cls: Any, db: Any, id: str
    ) -> CompetitionFormat:
        """Get competition_format function."""
        competition_format = (
            await CompetitionFormatsAdapter.get_competition_format_by_id(db, id)
        )
        # return the document if found:
        if competition_format:
            if competition_format["datatype"] == "interval_start":
                return IntervalStartFormat.from_dict(competition_format)
            elif competition_format["datatype"] == "individual_sprint":
                # sort the race-configs by max_no_of_contestants:
                competition_format["race_config_non_ranked"].sort(
                    key=lambda k: (k["max_no_of_contestants"],),
                    reverse=False,
                )
                competition_format["race_config_ranked"].sort(
                    key=lambda k: (k["max_no_of_contestants"],),
                    reverse=False,
                )

                return IndividualSprintFormat.from_dict(competition_format)
        raise CompetitionFormatNotFoundError(
            f"CompetitionFormat with id {id} not found"
        ) from None

    @classmethod
    async def get_competition_formats_by_name(
        cls: Any, db: Any, name: str
    ) -> List[CompetitionFormat]:
        """Get competition_format by name function."""
        competition_formats: List[CompetitionFormat] = []
        _competition_formats = (
            await CompetitionFormatsAdapter.get_competition_formats_by_name(db, name)
        )
        for competition_format in _competition_formats:
            if competition_format["datatype"] == "interval_start":
                competition_formats.append(
                    IntervalStartFormat.from_dict(competition_format)
                )
            if competition_format["datatype"] == "individual_sprint":
                # sort the race-configs by max_no_of_contestants:
                competition_format["race_config_non_ranked"].sort(
                    key=lambda k: (k["max_no_of_contestants"],),
                    reverse=False,
                )
                competition_format["race_config_ranked"].sort(
                    key=lambda k: (k["max_no_of_contestants"],),
                    reverse=False,
                )
                competition_formats.append(
                    IndividualSprintFormat.from_dict(competition_format)
                )
        return competition_formats

    @classmethod
    async def update_competition_format(
        cls: Any,
        db: Any,
        id: str,
        competition_format: Union[IndividualSprintFormat, IntervalStartFormat],
    ) -> Optional[str]:
        """Get competition_format function."""
        # Validate:
        await validate_competition_format(competition_format)
        # get old document
        old_competition_format = (
            await CompetitionFormatsAdapter.get_competition_format_by_id(db, id)
        )
        # update the competition_format if found:
        if old_competition_format:
            if competition_format.id != old_competition_format["id"]:
                raise IllegalValueError(
                    "Cannot change id for competition_format."
                ) from None
            # Sort the race_configs:
            if type(competition_format) == IndividualSprintFormat:
                competition_format.race_config_non_ranked.sort(
                    key=lambda k: (k.max_no_of_contestants,),
                    reverse=False,
                )
                competition_format.race_config_ranked.sort(
                    key=lambda k: (k.max_no_of_contestants,),
                    reverse=False,
                )
            new_competition_format = competition_format.to_dict()
            result = await CompetitionFormatsAdapter.update_competition_format(
                db, id, new_competition_format
            )
            return result
        raise CompetitionFormatNotFoundError(
            f"CompetitionFormat with id {id} not found."
        ) from None

    @classmethod
    async def delete_competition_format(cls: Any, db: Any, id: str) -> Optional[str]:
        """Get competition_format function."""
        # get old document
        competition_format = (
            await CompetitionFormatsAdapter.get_competition_format_by_id(db, id)
        )
        # delete the document if found:
        if competition_format:
            result = await CompetitionFormatsAdapter.delete_competition_format(db, id)
            return result
        raise CompetitionFormatNotFoundError(
            f"CompetitionFormat with id {id} not found"
        ) from None


#   Validation:
async def validate_competition_format(  # noqa: C901
    competition_format: Union[IndividualSprintFormat, IntervalStartFormat],
) -> None:
    """Validate the competition-format."""
    # Validate time_between_groups if set:
    if hasattr(competition_format, "time_between_groups"):
        try:
            time.fromisoformat(competition_format.time_between_groups)  # type: ignore
        except ValueError as e:
            raise InvalidDateFormatError(
                f'time_between_groups "{competition_format.time_between_groups}" has invalid time format.'  # noqa: B950
            ) from e
    # Validate intervals if set:
    if type(competition_format) is IntervalStartFormat and hasattr(
        competition_format, "intervals"
    ):
        try:
            time.fromisoformat(competition_format.intervals)  # type: ignore
        except ValueError as e:
            raise InvalidDateFormatError(
                f'intervals "{competition_format.intervals}" has invalid time format.'
            ) from e
    if type(competition_format) is IndividualSprintFormat:
        # Validate time_between_rounds if set:
        if hasattr(competition_format, "time_between_rounds"):
            try:
                time.fromisoformat(competition_format.time_between_rounds)  # type: ignore
            except ValueError as e:
                raise InvalidDateFormatError(
                    f'intervals "{competition_format.time_between_rounds}" has invalid time format.'  # noqa: B950
                ) from e
        # Validate time_between_rounds if set:
        if hasattr(competition_format, "time_between_heats"):
            try:
                time.fromisoformat(competition_format.time_between_heats)  # type: ignore
            except ValueError as e:
                raise InvalidDateFormatError(
                    f'intervals "{competition_format.time_between_heats}" has invalid time format.'  # noqa: B950
                ) from e
