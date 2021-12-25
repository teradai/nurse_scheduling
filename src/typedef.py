import typing
import enum


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


class CommandPerson(typing.TypedDict):
    name: str
    requests: typing.List[str]  # todo: 内部でEnumを定義する


class Command(typing.TypedDict):
    persons: typing.List[CommandPerson]


class ResultPerson(typing.TypedDict):
    name: str
    shifts: typing.List[ShiftType]


class Result(typing.TypedDict):
    status: str
    persons: typing.List[ResultPerson]
