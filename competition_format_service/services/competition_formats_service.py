"""Module for competition_formats service."""
import logging
from typing import Any, List, Optional, Union
import uuid

from competition_format_service.adapters import CompetitionFormatsAdapter
from competition_format_service.models import (
    CompetitionFormat,
    IndividualSprintFormat,
    IntervalStartFormat,
    RaceConfig,
)
from .exceptions import (
    CompetitionFormatAlreadyExistError,
    CompetitionFormatNotFoundError,
    IllegalValueError,
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
            CompetitionFormatAlreadyExistError: A format with the same name already exist
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
            raise CompetitionFormatAlreadyExistError(
                f"Competition-format with name {competition_format.name} already exist."
            ) from None
        # create id
        id = create_id()
        competition_format.id = id

        # Validation:
        try:
            await cls.validate_competition_format(competition_format)
        except ValidationError as e:
            raise e from e

        # Sort the race_configs:
        if isinstance(competition_format, IndividualSprintFormat):
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
        await cls.validate_competition_format(competition_format)
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
            if isinstance(competition_format, IndividualSprintFormat):
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

    @classmethod
    async def validate_competition_format(  # noqa: C901
        cls: Any,
        competition_format: Union[IndividualSprintFormat, IntervalStartFormat],
    ) -> None:  # pragma: no cover
        """Validate the competition-format."""
        # Max number of contestants in race must be greater than zero:
        if competition_format.max_no_of_contestants_in_race <= 0:
            raise IllegalValueError(
                "Max number of contestants in race must be greater than zero."
            ) from None
        # Max number of contestants in raceclass must be greater than zero:
        if competition_format.max_no_of_contestants_in_raceclass <= 0:
            raise IllegalValueError(
                "Max number of contestants in raceclass must be greater than zero."
            ) from None

        # Validate IntervalStartFormat:
        if isinstance(competition_format, IntervalStartFormat):
            if competition_format.intervals == 0:
                raise IllegalValueError(
                    "Intervals must be greater than zero."
                ) from None

        # Validate IndividualSprintFormat:
        if isinstance(competition_format, IndividualSprintFormat):
            if competition_format.time_between_heats == 0:
                raise IllegalValueError(
                    "Time between heats must be greater than zero."
                ) from None

            if (
                hasattr(competition_format, "rounds_non_ranked_classes")
                and competition_format.rounds_non_ranked_classes
            ):
                pass
            else:
                raise ValidationError(
                    "Mandatory attbribute 'rounds_non_ranked_classes' missing."
                )

            if (
                hasattr(competition_format, "rounds_ranked_classes")
                and competition_format.rounds_ranked_classes
            ):
                pass
            else:
                raise ValidationError(
                    "Mandatory attbribute 'rounds_ranked_classes' missing."
                )

            if (
                hasattr(competition_format, "race_config_non_ranked")
                and competition_format.race_config_non_ranked
            ):
                await cls.validate_race_config(
                    max_no_of_contestants_in_raceclass=competition_format.max_no_of_contestants_in_raceclass,
                    rounds=competition_format.rounds_non_ranked_classes,
                    race_configs=competition_format.race_config_non_ranked,
                )
            else:
                raise ValidationError(
                    "Mandatory attbribute 'race_config_non_ranked' missing."
                )

            if (
                hasattr(competition_format, "race_config_ranked")
                and competition_format.race_config_ranked
            ):
                await cls.validate_race_config(
                    max_no_of_contestants_in_raceclass=competition_format.max_no_of_contestants_in_raceclass,
                    rounds=competition_format.rounds_ranked_classes,
                    race_configs=competition_format.race_config_ranked,
                )
            else:
                raise ValidationError(
                    "Mandatory attbribute 'race_config_non_ranked' missing."
                )

    @classmethod
    async def validate_race_config(  # noqa: C901
        cls: Any,
        max_no_of_contestants_in_raceclass: int,
        rounds: List,
        race_configs: List[RaceConfig],
    ) -> None:  # pragma: no cover
        """Validate the competition-format."""
        for race_config in race_configs:
            # Max number of contestants must be greater than zero:
            if race_config.max_no_of_contestants <= 0:
                raise IllegalValueError(
                    "Max number of contestants must be greater than zero."
                ) from None
            # Max number of contestants must be less than
            # or equal to max_no_of_contestants_in_race:
            if race_config.max_no_of_contestants > max_no_of_contestants_in_raceclass:
                raise IllegalValueError(
                    "Max number of contestants in race_config must not be greater than max number of contestants in race."  # noqa: B950
                ) from None
            # Every round must in race_config_non_ranked must correspond to a round in rounds:
            for round in race_config.rounds:
                if round not in rounds:
                    raise IllegalValueError(
                        f"Round {round} not found in rounds on competition_format."
                    ) from None
            # Every key in no_of_heats must be in rounds:
            for key in race_config.no_of_heats.keys():
                if key not in rounds:
                    raise IllegalValueError(
                        f"Round {key} in no_of_heats not found in rounds on race_config."
                    ) from None
            # Number of heats must be greater than zero:
            for _round in race_config.no_of_heats.values():
                for _no_of_heat in _round.values():
                    if _no_of_heat < 0:
                        raise IllegalValueError(
                            f"Config with key {race_config.max_no_of_contestants}:"
                            " Number of heats must not be less than zero."
                        ) from None
