from growing_tree import GrowingTree, DisplayMaze
from typing import Any
from mlx import Mlx

def main() -> None:
    dic: dict[str, Any]={
        'WIDTH': 20, # max 220
        'HEIGHT': 20, # max 135
        'ENTRY': (48, 48),
        'EXIT': (18, 18),
        'OUTPUT_FILE': 'result.txt'
    }
    tree = GrowingTree(dic)
    # tree.display()
    # print(tree.path)
    entry = (tree.x_entry, tree.y_entry)
    exit = (tree.x_exit, tree.y_exit)
    screen = DisplayMaze(tree.get_the_list(), tree.path, entry, exit)
    screen.intialize_display_settings()
    
 

if __name__ == '__main__':
    main()