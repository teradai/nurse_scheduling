import csv
import sys
import typing

from solver_schedule import ScheduleProblem
from typedef import Command, CommandPerson, Result, ShiftType


def read_request_csv(file_name: str) -> Command:
    with open(file_name, "r") as csv_file:
        reader = csv.reader(csv_file)
        persons: typing.List[CommandPerson] = list()
        for info in reader:
            person: CommandPerson = {"name": info[0], "requests": info[1:]}
            persons.append(person)

        return {"persons": persons}


def write_shift_csv(file_name: str, result: Result) -> None:
    with open(file_name, "w") as csv_file:
        writer = csv.writer(csv_file)
        for person in result["persons"]:
            writer.writerow([person["name"]] + list(map(ShiftType.to_str, person["shifts"])))


def main():
    args: list[str] = sys.argv
    if len(args) != 3:
        print("python main.py ${shift_request.csv}")
        sys.exit(1)

    shift_request: str = args[1]
    result_shift: str = args[2]
    command: Command = read_request_csv(shift_request)

    problem = ScheduleProblem()
    problem.create_model(command)

    result: Result = problem.solve_problem()
    print("optimize_status_code:{}".format(result["status"]))

    write_shift_csv(result_shift, result)


if __name__ == "__main__":
    main()
