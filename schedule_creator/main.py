import csv
import io
import sys
import typing

from schedule_creator.check_schedule import (
    check_all_nurse_hoping_schedule,
    check_all_nurse_working_four_days_or_less,
    check_all_shift_exsisting_per_day,
    check_rest_day_num_equalized_per_nurse,
)
from schedule_creator.solve_schedule import ScheduleProblem
from schedule_creator.typedef import (
    Command,
    CommandPerson,
    HopeShiftType,
    Result,
    ShiftType,
)


def read_request_csv(file_name: str) -> Command:
    with open(file_name, "r") as csv_file:
        reader = csv.reader(csv_file)
        persons: typing.List[CommandPerson] = list()
        for info in reader:
            person: CommandPerson = {
                "name": info[0],
                "requests": list(map(HopeShiftType.from_str, info[1:])),
            }
            persons.append(person)

        return {"persons": persons}


def write_shift_csv(file_name: str, result: Result) -> None:
    with open(file_name, "w") as csv_file:
        writer = csv.writer(csv_file)
        for person in result["persons"]:
            writer.writerow(
                [person["name"]] + list(map(ShiftType.to_str, person["shifts"]))
            )


# todo: 日にちが0スタートになっているのでずらして出力する対応を実施する
def extract_from_constraint_violation(command: Command, result: Result) -> io.StringIO:
    str_io: io.StringIO = io.StringIO()

    check_result1: typing.Dict[
        int, typing.Set[ShiftType]
    ] = check_all_shift_exsisting_per_day(result["persons"])
    if check_result1:
        for day, shifts in check_result1.items():
            str_io.write(
                "{}日の出勤予定は{}である\n".format(
                    day, ", ".join(list(map(ShiftType.to_str, shifts)))
                )
            )
    del check_result1

    check_result2: typing.Dict[str, int] = check_all_nurse_working_four_days_or_less(
        result["persons"]
    )
    if check_result2:
        for name, work_num in check_result2.items():
            str_io.write("{}さんは最大で{}連勤実施予定になっている\n".format(name, work_num))
    del check_result2

    check_result3: typing.Set[
        typing.Tuple[str, int]
    ] = check_rest_day_num_equalized_per_nurse(result["persons"])
    if check_result3:
        assert len(check_result3) == 2
        for name, work_num in check_result3:
            str_io.write("{}さん休暇数{}日、".format(name, work_num))
    del check_result3

    check_result4: typing.Dict[str, typing.Set[int]] = check_all_nurse_hoping_schedule(
        command["persons"], result["persons"]
    )
    if check_result4:
        for name, not_desired_days in check_result4.items():
            str_io.write(
                "{}さんの希望シフトになっていない日付は{}である".format(
                    name, ", ".join(list(map(str, not_desired_days)))
                )
            )
    del check_result4

    return str_io


def write_text(file_name: str, string_io: io.StringIO) -> None:
    with open(file_name, "w") as text_file:
        text_file.write(string_io.getvalue())


def main():
    args: list[str] = sys.argv
    if len(args) != 4:
        print("python main.py ${shift_request.csv}")
        sys.exit(1)

    shift_request: str = args[1]
    result_shift: str = args[2]
    constraint_violation: str = args[3]
    command: Command = read_request_csv(shift_request)

    problem = ScheduleProblem()
    problem.create_model(command)

    result: Result = problem.solve_problem()
    print("optimize_status_code:{}".format(result["status"]))

    write_shift_csv(result_shift, result)

    str_io: io.StringIO = extract_from_constraint_violation(command, result)
    write_text(constraint_violation, str_io)


if __name__ == "__main__":
    main()
