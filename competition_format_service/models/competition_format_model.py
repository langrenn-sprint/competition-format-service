"""Competition format data class module."""

from abc import ABC
from dataclasses import dataclass, field
from datetime import time

from dataclasses_json import DataClassJsonMixin, config
from marshmallow.fields import Constant, Time


@dataclass
class CompetitionFormat(DataClassJsonMixin, ABC):
    """Abstract data class with details about a competition-format."""

    def __post_init__(self) -> None:  # pragma: no cover
        """Prevent instantiate abstract class."""
        if self.__class__ == CompetitionFormat:
            msg = "Cannot instantiate abstract class."
            raise TypeError(msg) from None

    name: str
    start_procedure: str
    starting_order: str
    max_no_of_contestants_in_raceclass: int
    max_no_of_contestants_in_race: int
    time_between_groups: time = field(
        metadata=config(
            encoder=time.isoformat,
            decoder=time.fromisoformat,
            mm_field=Time(format="iso"),
        )
    )


@dataclass
class IntervalStartFormat(CompetitionFormat, DataClassJsonMixin):
    """Data class with details about a interval start format."""

    intervals: time = field(
        metadata=config(
            encoder=time.isoformat,
            decoder=time.fromisoformat,
            mm_field=Time(format="iso"),
        )
    )
    datatype: str = field(
        metadata=dict(marshmallow_field=Constant("interval_start")),  # noqa: C408
        default="interval_start",
    )
    id: str | None = field(default=None)


@dataclass
class RaceConfig(DataClassJsonMixin):
    """Data class with details about the settings of a race."""

    max_no_of_contestants: int
    rounds: list[str]
    no_of_heats: dict[str, dict[str, int]]
    from_to: dict[str, dict[str, dict[str, dict[str, int | str]]]]


@dataclass
class IndividualSprintFormat(CompetitionFormat, DataClassJsonMixin):
    """Data class with details about a individual sprint format."""

    time_between_rounds: time = field(
        metadata=config(
            encoder=time.isoformat,
            decoder=time.fromisoformat,
            mm_field=Time(format="iso"),
        )
    )
    time_between_heats: time = field(
        metadata=config(
            encoder=time.isoformat,
            decoder=time.fromisoformat,
            mm_field=Time(format="iso"),
        )
    )
    rounds_ranked_classes: list[str]
    rounds_non_ranked_classes: list[str]
    race_config_ranked: list[RaceConfig]
    race_config_non_ranked: list[RaceConfig]
    datatype: str = field(
        metadata=dict(marshmallow_field=Constant("individual_sprint")),  # noqa: C408
        default="individual_sprint",
    )
    id: str | None = field(default=None)
