from growing_tree import GrowingTree, DisplayMaze
from typing import Any
from mlx import Mlx

def main() -> None:
    dic: dict[str, Any]={
        'WIDTH': 11, # max 220
        'HEIGHT': 10, # max 135
        'ENTRY': (0, 0),
        'EXIT': (9, 9),
        'OUTPUT_FILE': 'result.txt'
    }
    tree = GrowingTree(dic)
    entry = (tree.x_entry, tree.y_entry)
    exit = (tree.x_exit, tree.y_exit)
    # print(tree.get_the_list())
    screen = DisplayMaze(tree.get_the_list(), tree.path, entry, exit)
    screen.intialize_display_settings()



if __name__ == '__main__':
    main()