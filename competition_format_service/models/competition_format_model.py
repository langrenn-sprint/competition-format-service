"""Competition format data class module."""
from abc import ABC
from dataclasses import dataclass, field
from datetime import time
from typing import Dict, List, Optional, Union

from dataclasses_json import config, DataClassJsonMixin
from marshmallow.fields import Constant, Time


@dataclass
class CompetitionFormat(DataClassJsonMixin, ABC):  # noqa: B024
    """Abstract data class with details about a competition-format."""

    def __post_init__(self) -> None:  # pragma: no cover
        """Prevent instantiate abstract class."""
        if self.__class__ == CompetitionFormat:
            raise TypeError("Cannot instantiate abstract class.")

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
    timezone: str  # "Europe/Oslo"


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
        metadata=dict(marshmallow_field=Constant("interval_start")),
        default="interval_start",
    )
    id: Optional[str] = field(default=None)


@dataclass
class RaceConfig(DataClassJsonMixin):
    """Data class with details about the settings of a race."""

    max_no_of_contestants: int
    rounds: List[str]
    no_of_heats: Dict[str, Dict[str, int]]
    from_to: Dict[str, Dict[str, Dict[str, Dict[str, Union[int, str]]]]]


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
    rounds_ranked_classes: List[str]
    rounds_non_ranked_classes: List[str]
    race_config_ranked: List[RaceConfig]
    race_config_non_ranked: List[RaceConfig]
    datatype: str = field(
        metadata=dict(marshmallow_field=Constant("individual_sprint")),
        default="individual_sprint",
    )
    id: Optional[str] = field(default=None)
