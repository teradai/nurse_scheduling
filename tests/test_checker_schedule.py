import typing

from schedule_creator.check_schedule import check_all_nurse_assigned_shift
from schedule_creator.typedef import ResultPerson


def test_check_all_nurse_assigned_shift():
    persons: typing.List[ResultPerson] = list()
    persons.append({"name": "one", "shifts": [0, 1]})
    persons.append({"name": "two", "shifts": [2, 2]})

    # assert check_all_nurse_assigned_shift(persons) is True
