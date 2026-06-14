from dataclasses import dataclass


@dataclass(frozen=True)
class Species:
    key: str
    min_weight: float
    max_weight: float


@dataclass(frozen=True)
class Location:
    key: str
    timer_seconds: int
    species: tuple[Species, ...]


POND = Location(
    key="pond",
    timer_seconds=5 * 60,
    species=(
        Species(key="crucian", min_weight=0.1, max_weight=2.0),
        Species(key="perch", min_weight=0.2, max_weight=1.5),
    ),
)

LOCATIONS = {POND.key: POND}
