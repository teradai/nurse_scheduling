import typing

from schedule_creator.typedef import CommandPerson, ResultPerson


def check_schedule(
    ommand_person: typing.List[CommandPerson], result_persons: typing.List[ResultPerson]
) -> None:
    pass


# 全てのナースは(休暇を含む)必ず何かのシフトが割り当てられる
def check_all_nurse_assigned_shift(result_persons: typing.List[ResultPerson]) -> bool:
    pass


# 全ての日にちにおいて休暇以外のシフトが必ず一人いる
def check_all_shift_exsisting_per_day(
    result_persons: typing.List[ResultPerson],
) -> bool:
    pass


# 全てのナースにおいて、5連勤以上を禁止する( 連続する5日間において必ず休みが存在する )
def check_all_nurse_working_four_days_or_less(
    result_persons: typing.List[ResultPerson],
) -> bool:
    pass


# なるべく勤務日数を平等にしたい -> 休暇数を平等にしたい
def check_rest_day_num_equalized_per_nurse(
    result_persons: typing.List[ResultPerson],
) -> bool:
    pass


# 希望表通りのスケジュールか?
def check_all_nurse_hoping_schedule(
    command_person: typing.List[CommandPerson],
    result_persons: typing.List[ResultPerson],
) -> bool:
    pass
