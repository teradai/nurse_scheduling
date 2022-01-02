import typing

from schedule_creator.check_schedule import check_all_nurse_working_four_days_or_less
from schedule_creator.typedef import ResultPerson, ShiftType


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
