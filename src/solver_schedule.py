import typing

from ortools.sat.python import cp_model

from typedef import Command, Result, ResultPerson, ShiftType


class ScheduleProblem:
    def __init__(self):
        self.__model = cp_model.CpModel()
        self.__x = dict()

    def create_model(self, command: Command) -> None:
        self.__num_nurses: int = len(command["persons"])
        self.__num_days: int = len(command["persons"][0]["requests"])
        num_shifts: int = len(ShiftType)

        # 変数の設定
        for i in range(self.__num_nurses):
            for j in range(self.__num_days):
                for k in range(num_shifts):
                    self.__x[(i, j, k)] = self.__model.NewBoolVar(
                        "shift_{}_{}_{}".format(command["persons"][i]["name"], j, k)
                    )

        # 全てのナースは(休暇を含む)必ず何かのシフトが割り当てられる
        for i in range(self.__num_nurses):
            for j in range(self.__num_days):
                self.__model.Add(sum(self.__x[(i, j, k)] for k in range(num_shifts)) == 1)

        # 全ての日にちにおいて休暇以外のシフトが必ず一人いる
        for j in range(self.__num_days):
            for k in range(num_shifts - 1):
                self.__model.Add(sum(self.__x[(i, j, k)] for i in range(self.__num_nurses)) == 1)

        # 全てのナースにおいて、5連勤以上を禁止する( 連続する5日間において必ず休みが存在する )
        for i in range(self.__num_nurses):
            for j in range(self.__num_days):
                # todo: 前月のシフトも考慮できるようにする
                if j <= 4:
                    continue
                self.__model.Add(sum(self.__x[(i, j - h, ShiftType.RestShift)] for h in range(0, 5)) >= 1)

        # 均等化の制約

        # 希望表に基づく制約

        # 目的関数の追加

    def solve_problem(self) -> Result:
        solver = cp_model.CpSolver()
        solver.Solve(self.__model)

        persons: typing.List[ResultPerson] = list()
        for i in range(self.__num_nurses):
            name = str()
            shitfs: typing.List[ShiftType] = [ShiftType.RestShift] * self.__num_days
            for j in range(self.__num_days):
                for k, type in enumerate(ShiftType):
                    if solver.Value(self.__x[(i, j, k)]) == 1:
                        shitfs[j] = type
                        name = str(self.__x[(i, j, k)])
            persons.append({"name": name.split("_")[1], "shifts": shitfs})

        return {"status": solver.StatusName(), "persons": persons}

    __model: cp_model.CpModel
    __x: typing.Dict
    __num_nurses: int
    __num_days: int
