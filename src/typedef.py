import enum
from typing import List, TypedDict


@enum.unique
class HopeShiftType(enum.Enum):
    RequireType = 1
    FreedType = 2
    RestType = 3

    @staticmethod
    def from_str(hope_shift: str) -> "HopeShiftType":
        if hope_shift == "o":
            return HopeShiftType.RequireType
        if hope_shift == "-":
            return HopeShiftType.FreedType

        return HopeShiftType.RestType


@enum.unique
class ShiftType(enum.IntEnum):
    EarlyShift = 0
    LateShift = 1
    RestShift = 2

    @staticmethod
    def to_str(cls: "ShiftType") -> str:
        if cls.value == ShiftType.EarlyShift:
            return "早番"
        if cls.value == ShiftType.LateShift:
            return "遅番"

        return "休暇"


class CommandPerson(TypedDict):
    name: str
    requests: List[HopeShiftType]


class Command(TypedDict):
    persons: List[CommandPerson]


class ResultPerson(TypedDict):
    name: str
    shifts: List[ShiftType]


class Result(TypedDict):
    status: str
    persons: List[ResultPerson]
