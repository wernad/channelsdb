from dataclasses import dataclass


@dataclass
class FilterBase:
    key: str


@dataclass
class SimpleFilter(FilterBase):
    value: int | float | str


@dataclass
class RangeFilter(FilterBase):
    from_: int | float
    to: int | float


@dataclass
class Filter:
    simple: list[SimpleFilter]
    range_: list[RangeFilter]
