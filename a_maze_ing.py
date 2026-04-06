
import sys
import traceback
from mazegen import MazeInit, MazeConfigError
from mazegen import MazeGenerator
from typing import Any
from displaymaze import DisplayMaze


def main() -> None:

    try:
        if len(sys.argv) < 2:
            raise MazeConfigError("Use as first argument a configuration file")
        init: dict[str, Any] = MazeInit(sys.argv[1])()
        maze = MazeGenerator(init)
        maze.resolve()
        screen = DisplayMaze(
                maze.array, maze.road, init['ENTRY'], init['EXIT'])
        screen.intialize_display_settings()
        maze.create_file()
    except Exception as e:
        print("An error occured :", e, file=sys.stderr)
        if len(sys.argv) > 2 and sys.argv[2] == "traceback":
            traceback.print_exc()


if __name__ == "__main__":
    main()
