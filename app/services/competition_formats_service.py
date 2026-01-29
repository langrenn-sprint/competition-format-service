"""Module for competition_formats service."""

import logging
from typing import Any
from uuid import UUID

from app.adapters import CompetitionFormatsAdapter
from app.models import (
    CompetitionFormatUnion,
    IndividualSprintFormat,
    RaceConfig,
)

from .exceptions import (
    CompetitionFormatAlreadyExistError,
    CompetitionFormatNotFoundError,
    IllegalValueError,
    ValidationError,
)


class CompetitionFormatsService:
    """Class representing a service for competition_formats."""

    logger = logging.getLogger(
        "competition_format_service.competition_formats_service.CompetitionFormatsService"
    )

    @classmethod
    async def create_competition_format(
        cls: Any,
        competition_format: CompetitionFormatUnion,
    ) -> UUID | None:
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
        # Check if it exists:
        _competition_formats = (
            await CompetitionFormatsAdapter.get_competition_formats_by_name(
                competition_format.name
            )
        )
        if _competition_formats:
            msg = (
                f"Competition-format with name {competition_format.name} already exist."
            )
            raise CompetitionFormatAlreadyExistError(msg) from None

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
        result = await CompetitionFormatsAdapter.create_competition_format(
            competition_format
        )
        cls.logger.debug(
            f"inserted competition_format with id: {competition_format.id.hex} and result: {result}"
        )
        if result:
            return competition_format.id
        return None

    @classmethod
    async def update_competition_format(
        cls: Any,
        competition_format_id: UUID,
        competition_format: CompetitionFormatUnion,
    ) -> str | None:
        """Get competition_format function."""
        # Validate:
        await cls.validate_competition_format(competition_format)
        # get old document
        old_competition_format = (
            await CompetitionFormatsAdapter.get_competition_format_by_id(
                competition_format_id
            )
        )
        # update the competition_format if found:
        if old_competition_format:
            if competition_format.id != old_competition_format.id:
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
            return await CompetitionFormatsAdapter.update_competition_format(
                competition_format_id, competition_format
            )

        msg = f"CompetitionFormat with id {competition_format_id.hex} not found."
        raise CompetitionFormatNotFoundError(msg) from None

    @classmethod
    async def delete_competition_format(
        cls: Any, competition_format_id: UUID
    ) -> str | None:
        """Get competition_format function."""
        # get old document
        competition_format = (
            await CompetitionFormatsAdapter.get_competition_format_by_id(
                competition_format_id
            )
        )
        # delete the document if found:
        if competition_format:
            return await CompetitionFormatsAdapter.delete_competition_format(
                competition_format_id
            )

        msg = f"CompetitionFormat with id {competition_format_id.hex} not found."
        raise CompetitionFormatNotFoundError(msg) from None

    @classmethod
    async def validate_competition_format(
        cls: Any,
        competition_format: CompetitionFormatUnion,
    ) -> None:  # pragma: no cover
        """Validate the competition-format."""
        # Validate IndividualSprintFormat:
        if isinstance(competition_format, IndividualSprintFormat):
            await cls.validate_individual_sprint_format(competition_format)

    @classmethod
    async def validate_race_config(
        cls: Any,
        max_no_of_contestants_in_raceclass: int,
        rounds: list,
        race_configs: list[RaceConfig],
    ) -> None:  # pragma: no cover
        """Validate the competition-format."""
        for race_config in race_configs:
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
