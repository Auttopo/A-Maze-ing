
from typing import Any
from os.path import exists


class MazeConfigError(Exception):
    pass


class MazeInit():

    def __call__(self) -> dict[str, str | int | bool]:
        return self.config

    def __init__(self, file_name: str) -> None:
        self.config: dict[str, Any] = {}
        try:
            open(file_name, "r")
        except Exception:
            raise MazeConfigError(
                f"Configuration file name '{file_name}' do not exist"
                f", or the file is inaccessible")
        with open(file_name, "r") as file:
            full_data: str = file.read()
            lines: list[str] = full_data.split("\n")
            for i, line in enumerate(lines, 1):
                self.line_parser(line, i)
        self.keys_validation()
        self.data_validation()

    def line_parser(self, line: str, i: int) -> None:
        if line == "" or line[0] == "#":
            return
        try:
            data: list[str] | str = line.split("=")
            self.config.update({data[0]: data[1]})
        except Exception:
            raise MazeConfigError(f"line '{i}' not correclty set: {data}"
                                  "\nformat: SETTING_NAME=VALUE")

    def keys_validation(self) -> None:
        trace: str = ""
        valid_data = {
            "WIDTH", "HEIGHT", "ENTRY",
            "EXIT", "OUTPUT_FILE", "OUTPUT_FILE_OVERRIDE",
            "PERFECT", "SEED", "SHAPE"
            }
        for elem in self.config:
            if elem not in valid_data:
                trace += "unknow key in the config file : "\
                    + str(elem) + "\n"

        if "WIDTH" not in self.config:
            trace += "WIDTH not set\n"
        if "HEIGHT" not in self.config:
            trace += "HEIGHT not set\n"
        if "ENTRY" not in self.config:
            trace += "ENTRY not set\n"
        if "EXIT" not in self.config:
            trace += "EXIT not set\n"
        if "OUTPUT_FILE" not in self.config:
            trace += "OUTPUT_FILE not set\n"
        if "PERFECT" not in self.config:
            trace += "PERFECT not set\n"
        if "SEED" not in self.config:
            trace += "SEED not set\n"
        if trace:
            raise MazeConfigError(f"\n{trace[:len(trace) - 1]}")

    @staticmethod
    def value_check(data: str, name: str) -> int:
        try:
            data: int = int(data)
            if data < 0:
                raise
        except Exception:
            raise MazeConfigError(
                f"invalid value {name}, need to be a positive integer")
        return data

    def coordinates_check(self, data_str: str) -> None:

        ex: str = ""
        ey: str = ""
        entry: list[str] = self()[data_str].split(",")
        try:
            x: int = MazeInit.value_check(entry[0], data_str + "_X")
            if x > self()["WIDTH"]:
                raise MazeConfigError(f"{data_str}_X need to be <= WIDTH")
        except Exception as e:
            ex = e
        try:
            y: int = MazeInit.value_check(entry[1], data_str + "_Y")
            if y > self()["HEIGHT"]:
                raise MazeConfigError(f"{data_str}_Y need to be <= HEIGHT")
        except Exception as e:
            ey = e
        if ex or ey:
            raise MazeConfigError(f"{ex} | {ey}")
        self().update({data_str: (x, y)})

    def file_check(self) -> None:
        if self().get("OUTPUT_FILE_OVERRIDE"):
            match self()["OUTPUT_FILE_OVERRIDE"]:
                case "True":
                    self().update({"OUTPUT_FILE_OVERRIDE": True})
                case "False":
                    self().update({"OUTPUT_FILE_OVERRIDE": False})
                case _:
                    raise MazeConfigError("OUTPUT_FILE_OVERRIDE unknow value")
        else:
            self().update({"OUTPUT_FILE_OVERRIDE": False})

        if not self()["OUTPUT_FILE"]:
            raise MazeConfigError("please set a output name file")

        if exists(self()["OUTPUT_FILE"]):
            if not self()["OUTPUT_FILE_OVERRIDE"]:
                raise MazeConfigError(
                    "please set a different output name file or set "
                    "OUTPUT_FILE_OVERRIDE=True, this one already exist")

    def data_validation(self) -> None:
        self()["WIDTH"] = self.value_check(self()["WIDTH"], "WIDTH")
        self()["HEIGHT"] = self.value_check(self()["HEIGHT"], "HEIGHT")
        self.coordinates_check("ENTRY")
        self.coordinates_check("EXIT")
        self.file_check()
        match self()["PERFECT"]:
            case "True":
                self()["PERFECT"] = True
            case "False":
                self()["PERFECT"] = False
            case _:
                raise MazeConfigError("PERFECT unknow value")
        if self()["SEED"] != "Random":
            self()["SEED"] = self.value_check(
                self()["SEED"],
                "SEED need to set as 'Random', or"
            )
        if self()["WIDTH"] < 11:
            raise MazeConfigError("width can't be lower than 11")
        if self()["HEIGHT"] < 9:
            raise MazeConfigError("height can't be lower than 9")
        if self()["SHAPE"] not in {"Classic", "Circle", "Square"}:
            raise MazeConfigError("SHAPE unknow type, possibilities : Classic ; Circle ; Square")



