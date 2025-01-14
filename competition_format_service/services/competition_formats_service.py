"""Module for competition_formats service."""

import datetime
import logging
import uuid
from typing import Any

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
    async def get_all_competition_formats(cls: Any, db: Any) -> list[CompetitionFormat]:
        """Get all competition_formats function."""
        competition_formats: list[CompetitionFormat] = []
        _competition_formats = (
            await CompetitionFormatsAdapter.get_all_competition_formats(db)
        )
        for e in _competition_formats:
            if e["datatype"] == "interval_start":
                competition_formats.append(IntervalStartFormat.from_dict(e))
            elif e["datatype"] == "individual_sprint":
                competition_formats.append(IndividualSprintFormat.from_dict(e))
        return sorted(
            competition_formats,
            key=lambda k: (k.name,),
            reverse=False,
        )

    @classmethod
    async def create_competition_format(
        cls: Any,
        db: Any,
        competition_format: IndividualSprintFormat | IntervalStartFormat,
    ) -> str | None:
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
            msg = "Cannot create competition-format with input id."
            raise ValidationError(msg) from None
        # Check if it exists:
        _competition_formats = (
            await CompetitionFormatsAdapter.get_competition_formats_by_name(
                db, competition_format.name
            )
        )
        if _competition_formats:
            msg = (
                f"Competition-format with name {competition_format.name} already exist."
            )
            raise CompetitionFormatAlreadyExistError(msg) from None
        # create id
        competition_format_id = create_id()
        competition_format.id = competition_format_id

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
        logging.debug(f"inserted competition_format with id: {competition_format_id}")
        if result:
            return competition_format_id
        return None

    @classmethod
    async def get_competition_format_by_id(
        cls: Any, db: Any, competition_format_id: str
    ) -> CompetitionFormat:
        """Get competition_format function."""
        competition_format = (
            await CompetitionFormatsAdapter.get_competition_format_by_id(
                db, competition_format_id
            )
        )
        # return the document if found:
        if competition_format:
            if competition_format["datatype"] == "interval_start":
                return IntervalStartFormat.from_dict(competition_format)
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

                return IndividualSprintFormat.from_dict(competition_format)

        msg = f"CompetitionFormat with id {competition_format_id} not found"
        raise CompetitionFormatNotFoundError(msg) from None

    @classmethod
    async def get_competition_formats_by_name(
        cls: Any, db: Any, name: str
    ) -> list[CompetitionFormat]:
        """Get competition_format by name function."""
        competition_formats: list[CompetitionFormat] = []
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
        competition_format_id: str,
        competition_format: IndividualSprintFormat | IntervalStartFormat,
    ) -> str | None:
        """Get competition_format function."""
        # Validate:
        await cls.validate_competition_format(competition_format)
        # get old document
        old_competition_format = (
            await CompetitionFormatsAdapter.get_competition_format_by_id(
                db, competition_format_id
            )
        )
        # update the competition_format if found:
        if old_competition_format:
            if competition_format.id != old_competition_format["id"]:
                msg = "Cannot change id for competition_format."
                raise IllegalValueError(msg) from None
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
            return await CompetitionFormatsAdapter.update_competition_format(
                db, competition_format_id, new_competition_format
            )

        msg = f"CompetitionFormat with id {competition_format_id} not found."
        raise CompetitionFormatNotFoundError(msg) from None

    @classmethod
    async def delete_competition_format(
        cls: Any, db: Any, competition_format_id: str
    ) -> str | None:
        """Get competition_format function."""
        # get old document
        competition_format = (
            await CompetitionFormatsAdapter.get_competition_format_by_id(
                db, competition_format_id
            )
        )
        # delete the document if found:
        if competition_format:
            return await CompetitionFormatsAdapter.delete_competition_format(
                db, competition_format_id
            )

        msg = f"CompetitionFormat with id {competition_format_id} not found."
        raise CompetitionFormatNotFoundError(msg) from None

    @classmethod
    async def validate_competition_format(
        cls: Any,
        competition_format: IndividualSprintFormat | IntervalStartFormat,
    ) -> None:  # pragma: no cover
        """Validate the competition-format."""
        # Max number of contestants in race must be greater than zero:
        if competition_format.max_no_of_contestants_in_race <= 0:
            msg = "Max number of contestants in race must be greater than zero."
            raise IllegalValueError(msg) from None
        # Max number of contestants in raceclass must be greater than zero:
        if competition_format.max_no_of_contestants_in_raceclass <= 0:
            msg = "Max number of contestants in raceclass must be greater than zero."
            raise IllegalValueError(msg) from None

        # Validate IntervalStartFormat:
        if (
            isinstance(competition_format, IntervalStartFormat)
            and competition_format.intervals == 0
        ):
            msg = "Intervals must be greater than zero."
            raise IllegalValueError(msg) from None

        # Validate IndividualSprintFormat:
        if isinstance(competition_format, IndividualSprintFormat):
            await cls.validate_individual_sprint_format(competition_format)

    @classmethod
    async def validate_race_config(  # noqa: C901
        cls: Any,
        max_no_of_contestants_in_raceclass: int,
        rounds: list,
        race_configs: list[RaceConfig],
    ) -> None:  # pragma: no cover
        """Validate the competition-format."""
        for race_config in race_configs:
            # Max number of contestants must be greater than zero:
            if race_config.max_no_of_contestants <= 0:
                msg = "Max number of contestants must be greater than zero."
                raise IllegalValueError(msg) from None
            # Max number of contestants must be less than
            # or equal to max_no_of_contestants_in_race:
            if race_config.max_no_of_contestants > max_no_of_contestants_in_raceclass:
                msg = "Max number of contestants in race_config must not be greater than max number of contestants in race."
                raise IllegalValueError(msg) from None
            # Every round must in race_config_non_ranked must correspond to a round in rounds:
            for race_round in race_config.rounds:
                if race_round not in rounds:
                    msg = (
                        f"Round {race_round} not found in rounds on competition_format."
                    )
                    raise IllegalValueError(msg) from None
            # Every key in no_of_heats must be in rounds:
            for key in race_config.no_of_heats:
                if key not in rounds:
                    msg = f"Round {key} not found in rounds on race_config."
                    raise IllegalValueError(msg) from None
            # Number of heats must be greater than zero:
            for race_round in race_config.no_of_heats.values():
                for _no_of_heat in race_round.values():
                    if _no_of_heat < 0:
                        msg = (
                            f"Config with key {race_config.max_no_of_contestants}:"
                            " Number of heats must not be less than zero."
                        )
                        raise IllegalValueError(msg) from None

    @classmethod
    async def validate_individual_sprint_format(
        cls: Any, competition_format: IndividualSprintFormat
    ) -> None:
        """Validate the IndividualSprintFormat."""
        if competition_format.time_between_heats == datetime.time(0, 0):
            msg = "Time between heats must be greater than zero."
            raise IllegalValueError(msg) from None

        if (
            hasattr(competition_format, "rounds_non_ranked_classes")
            and len(competition_format.rounds_non_ranked_classes) > 0
        ):
            pass
        else:
            msg = "Mandatory attbribute 'rounds_non_ranked_classes' missing."
            raise ValidationError(msg) from None

        if (
            hasattr(competition_format, "rounds_ranked_classes")
            and len(competition_format.rounds_ranked_classes) > 0
        ):
            pass
        else:
            msg = "Mandatory attbribute 'rounds_ranked_classes' missing."
            raise ValidationError(msg) from None

        if (
            hasattr(competition_format, "race_config_non_ranked")
            and len(competition_format.race_config_non_ranked) > 0
        ):
            await cls.validate_race_config(
                max_no_of_contestants_in_raceclass=competition_format.max_no_of_contestants_in_raceclass,
                rounds=competition_format.rounds_non_ranked_classes,
                race_configs=competition_format.race_config_non_ranked,
            )
        else:
            msg = "Mandatory attbribute 'race_config_non_ranked' missing."
            raise ValidationError(msg) from None

        if (
            hasattr(competition_format, "race_config_ranked")
            and len(competition_format.race_config_ranked) > 0
        ):
            await cls.validate_race_config(
                max_no_of_contestants_in_raceclass=competition_format.max_no_of_contestants_in_raceclass,
                rounds=competition_format.rounds_ranked_classes,
                race_configs=competition_format.race_config_ranked,
            )
        else:
            msg = "Mandatory attbribute 'race_config_ranked' missing."
            raise ValidationError(msg) from None
