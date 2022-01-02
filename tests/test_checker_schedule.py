import typing

from schedule_creator.check_schedule import (
    check_all_nurse_working_four_days_or_less,
    check_all_shift_exsisting_per_day,
    check_rest_day_num_equalized_per_nurse,
    check_all_nurse_hoping_schedule,
)
from schedule_creator.typedef import CommandPerson, HopeShiftType, ResultPerson, ShiftType


def test_check_all_shift_exsisting_per_day():
    persons: typing.List[ResultPerson] = list()

    persons.append(
        {
            "name": "one",
            "shifts": [
                ShiftType.EarlyShift,
                ShiftType.EarlyShift,
            ],
        }
    )
    assert check_all_shift_exsisting_per_day(persons) == {
        0: {ShiftType.EarlyShift},
        1: {ShiftType.EarlyShift},
    }

    persons.append(
        {
            "name": "two",
            "shifts": [
                ShiftType.LateShift,
                ShiftType.EarlyShift,
            ],
        }
    )
    assert check_all_shift_exsisting_per_day(persons) == {1: {ShiftType.EarlyShift}}

    persons.append(
        {
            "name": "three",
            "shifts": [
                ShiftType.LateShift,
                ShiftType.LateShift,
            ],
        }
    )
    assert check_all_shift_exsisting_per_day(persons) == dict()


def test_check_all_nurse_working_four_days_or_less():
    persons: typing.List[ResultPerson] = list()

    persons.append(
        {
            "name": "one",
            "shifts": [
                ShiftType.EarlyShift,
                ShiftType.EarlyShift,
                ShiftType.RestShift,
                ShiftType.LateShift,
                ShiftType.LateShift,
                ShiftType.LateShift,
            ],
        }
    )
    assert check_all_nurse_working_four_days_or_less(persons) == dict()

    persons.append(
        {
            "name": "two",
            "shifts": [
                ShiftType.EarlyShift,
                ShiftType.EarlyShift,
                ShiftType.EarlyShift,
                ShiftType.LateShift,
                ShiftType.LateShift,
                ShiftType.LateShift,
            ],
        }
    )
    assert check_all_nurse_working_four_days_or_less(persons) == {"two": 6}

    persons.append(
        {
            "name": "three",
            "shifts": [
                ShiftType.LateShift,
                ShiftType.LateShift,
                ShiftType.LateShift,
                ShiftType.LateShift,
                ShiftType.LateShift,
                ShiftType.RestShift,
            ],
        }
    )
    assert check_all_nurse_working_four_days_or_less(persons) == {"two": 6, "three": 5}


def test_check_rest_day_num_equalized_per_nurse():
    persons: typing.List[ResultPerson] = list()

    persons.append(
        {
            "name": "one",
            "shifts": [
                ShiftType.LateShift,
                ShiftType.RestShift,
                ShiftType.RestShift,
            ],
        }
    )

    persons.append(
        {
            "name": "two",
            "shifts": [
                ShiftType.EarlyShift,
                ShiftType.LateShift,
                ShiftType.RestShift,
            ],
        }
    )

    assert check_rest_day_num_equalized_per_nurse(persons) == set()

    persons.append(
        {
            "name": "three",
            "shifts": [
                ShiftType.RestShift,
                ShiftType.RestShift,
                ShiftType.RestShift,
            ],
        }
    )

    assert check_rest_day_num_equalized_per_nurse(persons) == {("two", 1), ("three", 3)}


def test_check_all_nurse_hoping_schedule():
    command_persons1: typing.List[CommandPerson] = list()
    result_persons1: typing.List[ResultPerson] = list()

    command_persons1.append(
        {
            "name": "one",
            "requests": [
                HopeShiftType.RestType,
                HopeShiftType.RequireType,
            ],
        }
    )

    result_persons1.append(
        {
            "name": "one",
            "shifts": [
                ShiftType.EarlyShift,
                ShiftType.RestShift,
            ],
        }
    )

    command_persons1.append(
        {
            "name": "two",
            "requests": [
                HopeShiftType.RestType,
                HopeShiftType.FreedType,
            ],
        }
    )

    result_persons1.append(
        {
            "name": "two",
            "shifts": [
                ShiftType.EarlyShift,
                ShiftType.EarlyShift,
            ],
        }
    )

    assert check_all_nurse_hoping_schedule(command_persons1, result_persons1) == {"one": {0, 1}, "two": {0}}

    command_persons2: typing.List[CommandPerson] = list()
    result_persons2: typing.List[ResultPerson] = list()

    command_persons2.append(
        {
            "name": "one",
            "requests": [
                HopeShiftType.RequireType,
                HopeShiftType.FreedType,
            ],
        }
    )

    result_persons2.append(
        {
            "name": "one",
            "shifts": [
                ShiftType.EarlyShift,
                ShiftType.EarlyShift,
            ],
        }
    )

    command_persons2.append(
        {
            "name": "two",
            "requests": [
                HopeShiftType.RestType,
                HopeShiftType.FreedType,
            ],
        }
    )

    result_persons2.append(
        {
            "name": "two",
            "shifts": [
                ShiftType.RestShift,
                ShiftType.RestShift,
            ],
        }
    )

    assert check_all_nurse_hoping_schedule(command_persons2, result_persons2) == dict()
