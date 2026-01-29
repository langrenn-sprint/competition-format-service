"""Unit test cases for the competition-format-service module."""

from datetime import timedelta

import pytest
from pydantic import ValidationError as PydanticValidationError

from app.models import (
    IndividualSprintFormat,
    IntervalStartFormat,
    RaceConfig,
)
from app.services import (
    CompetitionFormatsService,
    IllegalValueError,
    ValidationError,
)


@pytest.mark.unit
async def test_competition_format_service_with_valid_interval_start_format() -> None:
    """Should not raise ValidationError."""
    competition_format: IntervalStartFormat = IntervalStartFormat(
        name="Test",
        start_procedure="Test",
        starting_order="Test",
        max_no_of_contestants_in_race=1,
        max_no_of_contestants_in_raceclass=1,
        time_between_groups=timedelta(minutes=1),
        intervals=timedelta(seconds=30),
    )
    try:
        await CompetitionFormatsService.validate_competition_format(
            competition_format=competition_format
        )
    except ValidationError:
        pytest.fail("ValidationError was raised unexpectedly!")


@pytest.mark.unit
async def test_validate_competition_format_valid_individual_sprint_format() -> None:
    """Should not raise ValidationError."""
    competition_format: IndividualSprintFormat = IndividualSprintFormat(
        name="Test",
        start_procedure="Test",
        starting_order="Test",
        max_no_of_contestants_in_race=1,
        max_no_of_contestants_in_raceclass=1,
        time_between_groups=timedelta(minutes=1),
        time_between_rounds=timedelta(seconds=30),
        time_between_heats=timedelta(seconds=30),
        rounds_non_ranked_classes=["R1", "R2"],
        rounds_ranked_classes=["R1", "R2"],
        race_config_non_ranked=[
            RaceConfig(
                max_no_of_contestants=1,
                rounds=["R1", "R2"],
                no_of_heats={"R1": {"A": 1}, "R2": {"A": 1}},
                from_to={"R1": {"A": {"R2": {"A": "ALL"}}}},
            )
        ],
        race_config_ranked=[
            RaceConfig(
                max_no_of_contestants=1,
                rounds=["R1", "R2"],
                no_of_heats={"R1": {"A": 1}, "R2": {"A": 1}},
                from_to={"R1": {"A": {"R2": {"A": "ALL"}}}},
            )
        ],
    )

    try:
        await CompetitionFormatsService.validate_competition_format(
            competition_format=competition_format
        )
    except ValidationError:
        pytest.fail("ValidationError was raised unexpectedly!")


@pytest.mark.unit
async def test_validate_competition_format_individual_sprint_format_no_time_between_heats() -> (
    None
):
    """Should raise ValidationError during construction."""
    with pytest.raises(PydanticValidationError):
        IndividualSprintFormat(
            name="Test",
            start_procedure="Test",
            starting_order="Test",
            max_no_of_contestants_in_race=1,
            max_no_of_contestants_in_raceclass=1,
            time_between_groups=timedelta(minutes=1),
            time_between_rounds=timedelta(seconds=30),
            time_between_heats=timedelta(seconds=0),
            rounds_non_ranked_classes=["Test"],
            rounds_ranked_classes=["Test"],
            race_config_non_ranked=[],
            race_config_ranked=[],
        )


@pytest.mark.unit
async def test_validate_competition_format_individual_sprint_format_without_rounds() -> (
    None
):
    """Should raise ValidationError."""
    competition_format: IndividualSprintFormat = IndividualSprintFormat(
        name="Test",
        start_procedure="Test",
        starting_order="Test",
        max_no_of_contestants_in_race=1,
        max_no_of_contestants_in_raceclass=1,
        time_between_groups=timedelta(minutes=1),
        time_between_rounds=timedelta(seconds=30),
        time_between_heats=timedelta(seconds=30),
        rounds_non_ranked_classes=[],
        rounds_ranked_classes=[],
        race_config_non_ranked=[
            RaceConfig(
                max_no_of_contestants=1,
                rounds=["R1", "R2"],
                no_of_heats={"R1": {"A": 1}, "R2": {"A": 1}},
                from_to={"R1": {"A": {"R2": {"A": "ALL"}}}},
            )
        ],
        race_config_ranked=[
            RaceConfig(
                max_no_of_contestants=1,
                rounds=["R1", "R2"],
                no_of_heats={"R1": {"A": 1}, "R2": {"A": 1}},
                from_to={"R1": {"A": {"R2": {"A": "ALL"}}}},
            )
        ],
    )

    with pytest.raises(ValidationError):
        await CompetitionFormatsService.validate_competition_format(
            competition_format=competition_format
        )


@pytest.mark.unit
async def test_validate_competition_format_individual_sprint_format_without_race_config() -> (
    None
):
    """Should raise ValidationError."""
    competition_format: IndividualSprintFormat = IndividualSprintFormat(
        name="Test",
        start_procedure="Test",
        starting_order="Test",
        max_no_of_contestants_in_race=1,
        max_no_of_contestants_in_raceclass=1,
        time_between_groups=timedelta(minutes=1),
        time_between_rounds=timedelta(seconds=30),
        time_between_heats=timedelta(seconds=30),
        rounds_non_ranked_classes=["Test"],
        rounds_ranked_classes=["Test"],
        race_config_non_ranked=[],
        race_config_ranked=[],
    )

    with pytest.raises(ValidationError):
        await CompetitionFormatsService.validate_competition_format(
            competition_format=competition_format
        )


@pytest.mark.unit
async def test_validate_competition_format_individual_sprint_format_with_empty_race_config() -> (
    None
):
    """Should raise ValidationError."""
    competition_format: IndividualSprintFormat = IndividualSprintFormat(
        name="Test",
        start_procedure="Test",
        starting_order="Test",
        max_no_of_contestants_in_race=1,
        max_no_of_contestants_in_raceclass=1,
        time_between_groups=timedelta(minutes=1),
        time_between_rounds=timedelta(seconds=30),
        time_between_heats=timedelta(seconds=30),
        rounds_non_ranked_classes=["Test"],
        rounds_ranked_classes=["Test"],
        race_config_non_ranked=[],
        race_config_ranked=[],
    )

    with pytest.raises(ValidationError):
        await CompetitionFormatsService.validate_competition_format(
            competition_format=competition_format
        )


@pytest.mark.unit
async def test_validate_race_config_() -> None:
    """Should not raise ValidationError."""
    competition_format: IndividualSprintFormat = IndividualSprintFormat(
        name="Test",
        start_procedure="Test",
        starting_order="Test",
        max_no_of_contestants_in_race=1,
        max_no_of_contestants_in_raceclass=1,
        time_between_groups=timedelta(minutes=1),
        time_between_rounds=timedelta(seconds=30),
        time_between_heats=timedelta(seconds=30),
        rounds_non_ranked_classes=["Test"],
        rounds_ranked_classes=["R1", "R2"],
        race_config_non_ranked=[
            RaceConfig(
                max_no_of_contestants=1,
                rounds=["R1", "R2"],
                no_of_heats={"R1": {"A": 1}, "R2": {"A": 1}},
                from_to={"R1": {"A": {"R2": {"A": "ALL"}}}},
            )
        ],
        race_config_ranked=[
            RaceConfig(
                max_no_of_contestants=1,
                rounds=["R1", "R2"],
                no_of_heats={"R1": {"A": 1}, "R2": {"A": 1}},
                from_to={"R1": {"A": {"R2": {"A": "ALL"}}}},
            )
        ],
    )

    try:
        await CompetitionFormatsService.validate_race_config(
            competition_format.max_no_of_contestants_in_raceclass,
            competition_format.rounds_ranked_classes,
            competition_format.race_config_ranked,
        )
    except IllegalValueError:
        pytest.fail("IllegalValueError was raised unexpectedly!")
