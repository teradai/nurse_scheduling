import enum
from typing import List, TypedDict


@enum.unique
class ShiftType(enum.IntEnum):
    EarlyShift = 0
    LateShift = 1
    RestShift = 2

    def to_str(self):
        if self is self.EarlyShift:
            return "早番"
        if self is self.LateShift:
            return "遅番"

        return "休暇"


class CommandPerson(TypedDict):
    name: str
    requests: List[str]  # todo: 内部でEnumを定義する


class Command(TypedDict):
    persons: List[CommandPerson]


class ResultPerson(TypedDict):
    name: str
    shifts: List[ShiftType]


class Result(TypedDict):
    status: str
    persons: List[ResultPerson]
