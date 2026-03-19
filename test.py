from growing_tree import GrowingTree
from typing import Any

def main() -> None:
    dic: dict[str, Any]={
        'WIDTH': 10,
        'HEIGHT': 10,
        'ENTRY': (0, 0),
        'EXIT': (9, 9),
        'OUTPUT_FILE': 'result.txt'
    }
    tree = GrowingTree(dic)
    
    for element in tree.cells:
        row = [element[i].value for i in range(0, len(element))]
        print(f'{row}\n')

    tree.display()
    print(tree.path)

if __name__ == '__main__':
    main()