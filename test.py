from growing_tree import GrowingTree, DisplayMaze
from typing import Any
from mlx import Mlx

def main() -> None:
    dic: dict[str, Any]={
        'WIDTH': 20,
        'HEIGHT': 20,
        'ENTRY': (0, 0),
        'EXIT': (18, 18),
        'OUTPUT_FILE': 'result.txt'
    }
    tree = GrowingTree(dic)
    screen = DisplayMaze(tree.get_the_list())
    
    # for element in tree.cells:
    #     row = [element[i].value for i in range(0, len(element))]
    #     print(f'{row}\n')
# def mymouse(button, x, y, mystuff):
#     print(f"Got mouse event! button {button} at {x},{y}.")

# def mykey(keynum, mystuff):
#     print(f"Got key {keynum}, and got my stuff back:")
#     print(mystuff)
#     if keynum == 32:
#         m.mlx_mouse_hook(win_ptr, None, None)
#     elif keynum == 65307:
#         m.mlx_release(mlx_ptr)
#         exit(0)

# m = Mlx()
# mlx_ptr = m.mlx_init()
# win_ptr = m.mlx_new_window(mlx_ptr, 200, 200, "toto")
# m.mlx_clear_window(mlx_ptr, win_ptr)
# m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
# (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
# print(f"Got screen size: {w} x {h} .")

# stuff = [1, 2]
# m.mlx_mouse_hook(win_ptr, mymouse, None)
# m.mlx_key_hook(win_ptr, mykey, stuff)

# m.mlx_loop(mlx_ptr)


    

if __name__ == '__main__':
    main()