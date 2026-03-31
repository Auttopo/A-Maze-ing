from displaymaze import DisplayMaze
from typing import Any
from mazegeneration import MazeGenerator
from mazeinit import MazeInit
from mlx import Mlx


def main() -> None:
    init = MazeInit('config.txt')
    maze = MazeGenerator.UnperfectMaze(init())

    screen = DisplayMaze(maze.array, maze.road, init.config['ENTRY'], init.config['EXIT'])
    screen.intialize_display_settings()




if __name__ == '__main__':
    main()