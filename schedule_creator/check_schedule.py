import sys
import typing

from schedule_creator.typedef import CommandPerson, ResultPerson, ShiftType


# memo: personはこの関数で回す
def check_schedule(
    command_person: typing.List[CommandPerson],
    result_persons: typing.List[ResultPerson],
) -> None:
    pass


# 一日あたりに休暇以外の全てのシフトが存在する
def check_all_shift_exsisting_per_day(
    result_persons: typing.List[ResultPerson],
) -> bool:
    pass


# 5連勤以上しているナースを連勤数と共に列挙する
def check_all_nurse_working_four_days_or_less(
    result_persons: typing.List[ResultPerson],
) -> typing.Dict[str, int]:

    violations: typing.Dict[str, int] = dict()
    for person in result_persons:
        work_count: int = 0
        max_count: int = 0
        for shift in person["shifts"]:
            if shift == ShiftType.RestShift:
                work_count = 0
                continue
            else:
                work_count += 1

            max_count = max(max_count, work_count)

        if max_count >= 5:
            violations[person["name"]] = max_count

    return violations


# なるべく勤務日数を平等にしたい -> 休暇数を平等にしたい
def check_rest_day_num_equalized_per_nurse(
    result_persons: typing.List[ResultPerson],
) -> typing.Set[typing.Tuple[str, int]]:

    max_person: typing.Tuple[str, int] = ("", -1)
    min_person: typing.Tuple[str, int] = ("", sys.maxsize)
    for person in result_persons:
        rest_num = 0
        for shift in person["shifts"]:
            if shift == ShiftType.RestShift:
                rest_num += 1

        if rest_num > max_person[1]:
            max_person = (person["name"], rest_num)
        if rest_num < min_person[1]:
            min_person = (person["name"], rest_num)

    result: typing.Set[typing.Tuple[str, int]] = set()
    if max_person[1] - min_person[1] > 1:
        result.add(min_person)
        result.add(max_person)

    return result


# 希望表通りのスケジュールか?
def check_all_nurse_hoping_schedule(
    command_person: typing.List[CommandPerson],
    result_persons: typing.List[ResultPerson],
) -> bool:
    pass
