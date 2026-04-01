
import sys
from typing import Any
from os.path import exists
import random


def get_42_pos(width: int, height: int) -> list[tuple[int, int]]:
    # set: up left point
    if width < 11 or height < 9:
        return [(-1, -1)]

    pos_list: list[tuple[int, int]] = []
    pos_x = int(width / 2) - 3
    pos_y = int(height / 2) - 2
    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_y += 1
    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_x += 1

    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_y -= 1
    pos_list.append((pos_x, pos_y))
    pos_y += 2
    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_y += 1
    pos_list.append((pos_x, pos_y))
    pos_x += 2
    pos_y -= 4
    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_x += 1
    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_y += 1
    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_x -= 1
    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_y += 1
    for i in range(2):
        pos_list.append((pos_x, pos_y))
        pos_x += 1
    pos_list.append((pos_x, pos_y))
    return pos_list


class MazeConfigError(Exception):
    pass


class MazeInit():

    def __call__(self) -> dict[str, Any]:
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
            if data[0] in self.config:
                raise MazeConfigError(
                        f"keys can't be present more than once, "
                        f"keep only one {data[0]}")
            self.config.update({data[0]: data[1]})
        except MazeConfigError:
            raise
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
            idata: int = int(data)
            if idata < 0:
                raise
        except Exception:
            raise MazeConfigError(
                f"invalid value {name}, need to be a positive integer")
        return idata

    def coordinates_check(self, data_str: str) -> None:

        ex: str = ""
        ey: str = ""

        str_data: str = str(self()[data_str])
        entry: list[str] = str_data.split(",")
        try:
            x: int = MazeInit.value_check(entry[0], data_str + "_X")
            if x >= int(self()["WIDTH"]):
                raise MazeConfigError(f"{data_str}_X need to be < WIDTH")
        except Exception as e:
            ex = str(e)
        try:
            y: int = MazeInit.value_check(entry[1], data_str + "_Y")
            if y >= int(self()["HEIGHT"]):
                raise MazeConfigError(f"{data_str}_Y need to be < HEIGHT")
        except Exception as e:
            ey = str(e)
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

        # ----------------------------------- SIZE CHECK
        self()["WIDTH"] = self.value_check(self()["WIDTH"], "WIDTH")
        self()["HEIGHT"] = self.value_check(self()["HEIGHT"], "HEIGHT")
        if self()["WIDTH"] * self()["HEIGHT"] < 2:
            raise MazeConfigError("maze air need to be > 1")

        # --------------------------------- POS CHECK
        if self.config["WIDTH"] < 11 or self.config["HEIGHT"] < 9:
            print("42 not drawed, width < 11 or height < 9", file=sys.stderr)
        illegal_pos = get_42_pos(self.config["WIDTH"], self.config["HEIGHT"])
        possibles: list[tuple[int, int]] = [
                (x, y) for y in range(self()["HEIGHT"])
                for x in range(self()["WIDTH"])
                if (x, y) not in illegal_pos]
        if self()["ENTRY"] == "Random":
            x, y = random.choice(possibles)
            self().update({"ENTRY": (x, y)})
        else:
            self.coordinates_check("ENTRY")
        if self()["EXIT"] == "Random":
            possibles.remove(self()["ENTRY"])
            x, y = random.choice(possibles)
            self().update({"EXIT": (x, y)})
        else:
            self.coordinates_check("EXIT")

        # -------------------------------- PERFECT CHECK
        self.file_check()
        match self()["PERFECT"]:
            case "True":
                self()["PERFECT"] = True
            case "False":
                self()["PERFECT"] = False
            case "Random":
                self()["PERFECT"] = random.choice([True, False])
            case _:
                raise MazeConfigError("PERFECT unknow value")

        # -------------------------------- SEED CHECK
        if self()["SEED"] != "Random":
            self()["SEED"] = self.value_check(
                self()["SEED"],
                "SEED need to set as 'Random', or"
            )

        # ---------------------------------- SHAPE CHECK
        if self().get("SHAPE"):
            if self()["SHAPE"] == "Random":
                self().update(
                        {"SHAPE": random.choice(["Classic", "Circle", "Square"
                                                 ])})
            elif self()["SHAPE"] not in {"Classic", "Circle", "Square"}:
                raise MazeConfigError(
                        "SHAPE unknow type, possibilities "
                        ": Classic ; Circle ; Square ; Random")
        else:
            self().update({"SHAPE": random.choice(
                ["Classic", "Circle", "Square"])})
