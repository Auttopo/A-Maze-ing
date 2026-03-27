from growing_tree import GrowingTree, DisplayMaze
from typing import Any
from mlx import Mlx

def main() -> None:
    dic: dict[str, Any]={
        'WIDTH': 20, # max 220
        'HEIGHT': 20, # max 135
        'ENTRY': (0, 0),
        'EXIT': (18, 18),
        'OUTPUT_FILE': 'result.txt'
    }
    tree = GrowingTree(dic)
    # tree.display()
    # print(tree.path)
    screen = DisplayMaze(tree.get_the_list(), tree.path)
    screen.intialize_display_settings()
    
 

if __name__ == '__main__':
    main()