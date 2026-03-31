from displaymaze import DisplayMaze
from typing import Any
from mazegeneration import MazeGenerator
from mazeinit import MazeInit
from mlx import Mlx


def main() -> None:
    dic: dict[str, Any]={
        'WIDTH': 11, # max 220
        'HEIGHT': 10, # max 135
        'ENTRY': (0, 0),
        'EXIT': (9, 9),
        'OUTPUT_FILE': 'result.txt'
    }
    init = MazeInit('config.txt')
    maze = MazeGenerator.UnperfectMaze(init())

    screen = DisplayMaze(maze.array, maze.road, init.config['ENTRY'], init.config['EXIT'])
    screen.intialize_display_settings()


if __name__ == '__main__':
    main()