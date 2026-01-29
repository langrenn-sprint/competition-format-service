"""Competition format data class module."""

from abc import ABC
from datetime import timedelta
from typing import Annotated, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer


def serialize_timedelta(value: timedelta) -> str:
    """Serialize timedelta to HH:MM:SS format."""
    total_seconds = int(value.total_seconds())
    _, remainder = divmod(total_seconds, 86400)  # 24 * 60 * 60
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


TimedeltaField = Annotated[
    timedelta,
    PlainSerializer(serialize_timedelta, return_type=str),
]


class CompetitionFormat(BaseModel, ABC):
    """Abstract data class with details about a competition-format."""

    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: UUID = Field(default_factory=uuid4)
    name: str
    start_procedure: str
    starting_order: str
    max_no_of_contestants_in_raceclass: Annotated[int, Field(gt=0)]
    max_no_of_contestants_in_race: Annotated[int, Field(gt=0)]
    time_between_groups: Annotated[TimedeltaField, Field(gt=timedelta(0))]


class IntervalStartFormat(CompetitionFormat):
    """Data class with details about a interval start format."""

    datatype: Literal["interval_start"] = "interval_start"

    intervals: Annotated[TimedeltaField, Field(gt=timedelta(0))]


class RaceConfig(BaseModel):
    """Data class with details about the settings of a race."""

    max_no_of_contestants: Annotated[int, Field(gt=0)]
    rounds: list[str]
    no_of_heats: dict[str, dict[str, int]]
    from_to: dict[str, dict[str, dict[str, dict[str, int | str]]]]


class IndividualSprintFormat(CompetitionFormat):
    """Data class with details about a individual sprint format."""

    datatype: Literal["individual_sprint"] = "individual_sprint"

    time_between_rounds: Annotated[TimedeltaField, Field(gt=timedelta(0))]
    time_between_heats: Annotated[TimedeltaField, Field(gt=timedelta(0))]
    rounds_ranked_classes: list[str]
    rounds_non_ranked_classes: list[str]
    race_config_ranked: list[RaceConfig]
    race_config_non_ranked: list[RaceConfig]


CompetitionFormatUnion = Annotated[
    IntervalStartFormat | IndividualSprintFormat, Field(discriminator="datatype")
]
