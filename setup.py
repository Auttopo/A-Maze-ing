from typing import Any


class MazeConfigError(Exception):
    pass


class MazeInit:

    def __init__(self, file_name: str) -> None:
        self.config: dict[str, Any] = {}
        try:
            open(file_name, "r")
        except Exception:
            raise MazeConfigError(
                f"Configuration file name '{file_name}' do not exist"
                f", or the file is inaccessible")
        with open(file_name, "r") as file:
            data: str | list[str] = file.read()
            data = data.split("\n")
            for line in data:
                self.line_parser(line)
        self.keys_validation()

    def line_parser(self, data: list[str]) -> None:
        try:
            data = data.split("=")
            self.config.update({data[0]: data[1]})
        except Exception:
            raise MazeConfigError(f"line not correclty set: {data}"
                                  "\nformat: SETTING_NAME=VALUE")

    def keys_validation(self) -> None:
        trace: str = ""
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
            raise MazeConfigError(f"{trace[:len(trace) - 1]}")
