import random
from typing import Any
from mlx import Mlx


class Cell:
    """Specific class for defining each cell of the maze"""

    def __init__(self, x: int, y: int, value: int) -> None:
        self.value = value
        self.visited = False
        self.symbol = False
        self.x = x
        self.y = y


class GrowingTree:
    """Class for creating a perfect maze"""

    def __init__(self, dic: dict[str, Any]) -> None:
        """Allow you to have the output file directly"""
        self.rows: int = dic["HEIGHT"]
        self.columns: int = dic["WIDTH"]
        self.x_entry: int
        self.y_entry: int
        self.x_exit: int
        self.y_exit: int
        self.x_entry, self.y_entry = dic["ENTRY"]
        self.x_exit, self.y_exit = dic["EXIT"]
        self.output: str = dic["OUTPUT_FILE"]
        self.path: str = ""
        self.cells: list[list[Cell]] = []
        for x in range(0, self.rows):
            self.cells.append([])
            for y in range(0, self.columns):
                self.cells[x].append(Cell(x, y, 15))
        self.forty_two()
        self.build_maze()
        self.no_cell_visited()
        self.entry = self.cells[self.x_entry][self.y_entry]
        self.exit = self.cells[self.x_exit][self.y_exit]
        self.find_path(self.entry, self.exit)
        self.fill_the_file()

    def forty_two(self) -> None:
        """Initialize each cells of the 42 symbol"""
        x: int = int(self.rows / 2)
        y: int = int(self.columns / 2)
        for i in range(1, 4):
            self.cells[x][y + i].visited = True
            self.cells[x][y + i].symbol = True
            self.cells[x][y - i].visited = True
            self.cells[x][y - i].symbol = True
            self.cells[x - 2][y + i].visited = True
            self.cells[x - 2][y + i].symbol = True
            self.cells[x + 2][y + i].visited = True
            self.cells[x + 2][y + i].symbol = True

        for i in range(0, 3):
            self.cells[x - i][y - 3].visited = True
            self.cells[x - i][y - 3].symbol = True
            self.cells[x + i][y - 1].visited = True
            self.cells[x + i][y - 1].symbol = True

        self.cells[x - 1][y + 3].visited = True
        self.cells[x - 1][y + 3].symbol = True
        self.cells[x + 1][y + 1].visited = True
        self.cells[x + 1][y + 1].symbol = True

        self.cells[x - 2][y - 1].visited = True
        self.cells[x - 2][y - 1].symbol = True
        self.cells[x - 1][y - 1].visited = True
        self.cells[x - 1][y - 1].symbol = True

    def build_maze(self) -> None:
        """Create the maze according to Prim's algorithm"""

        cells_visited: list[Cell] = []
        x: int = int(self.rows / 2)
        y: int = int(self.columns / 2 - 1)
        active: Cell = self.cells[x][y]

        while active.symbol:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.columns - 1)
            active = self.cells[x][y]
            if not active.symbol:
                active.visited = True
                cells_visited.append(active)

        while cells_visited:
            active = random.choice(cells_visited)
            border: list[Cell] = []
            if not active.x == 0:
                target = self.cells[active.x - 1][active.y]
                if not target.symbol and not target.visited:
                    border.append(target)
            if not active.x == self.rows - 1:
                target = self.cells[active.x + 1][active.y]
                if not target.symbol and not target.visited:
                    border.append(target)
            if not active.y == 0:
                target = self.cells[active.x][active.y - 1]
                if not target.symbol and not target.visited:
                    border.append(target)
            if not active.y == self.columns - 1:
                target = self.cells[active.x][active.y + 1]
                if not target.symbol and not target.visited:
                    border.append(target)

            if border:
                target = border[random.randint(0, len(border) - 1)]
                target.visited = True
                cells_visited.append(target)
                if active.x - target.x == 1:
                    active.value -= 1
                    target.value -= 4
                elif active.x - target.x == -1:
                    active.value -= 4
                    target.value -= 1
                elif active.y - target.y == 1:
                    active.value -= 8
                    target.value -= 2
                elif active.y - target.y == -1:
                    active.value -= 2
                    target.value -= 8
            else:
                cells_visited.remove(active)

    def no_cell_visited(self) -> None:
        """Put every cells as no visited except 42 symbol"""
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                self.cells[x][y].visited = False
        self.forty_two()

    def find_path(self, entry: Cell, exit: Cell) -> bool:
        """Find the path from entry to exit"""
        entry.visited = True
        direction: str = ""
        if entry.x == exit.x and entry.y == exit.y:
            return True

        if (
            entry.value & 1 == 0 and not
            self.cells[entry.x - 1][entry.y].visited
             ):
            direction = "N"
            self.path += direction
            if self.find_path(self.cells[entry.x - 1][entry.y], exit):
                return True

        if (
            entry.value & 2 == 0 and not
            self.cells[entry.x][entry.y + 1].visited
             ):
            direction = "E"
            self.path += direction
            if self.find_path(self.cells[entry.x][entry.y + 1], exit):
                return True

        if (
            entry.value & 4 == 0 and not
            self.cells[entry.x + 1][entry.y].visited
             ):
            direction = "S"
            self.path += direction
            if self.find_path(self.cells[entry.x + 1][entry.y], exit):
                return True

        if (
            entry.value & 8 == 0 and not
            self.cells[entry.x][entry.y - 1].visited
             ):
            direction = "W"
            self.path += direction
            if self.find_path(self.cells[entry.x][entry.y - 1], exit):
                return True

        self.path = self.path[:-1]
        return False

    def fill_the_file(self) -> None:
        """Fill the output file"""
        text = open(self.output, "w")
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                text.write(
                    str(hex(self.cells[x][y].value).lstrip("0x").upper())
                    )
            text.write("\n")

        text.write(f"\n{self.entry.x},{self.entry.y}\n")
        text.write(f"{self.exit.x},{self.exit.y}\n")
        text.write(self.path)
        text.close()

    def display(self) -> None:
        """display a provisory maze"""
        for x in range(0, self.rows):
            top = ""
            for y in range(0, self.columns):
                top += "+" + ("   " if not self.cells[x][y].value & 1 else "---")
            print(top + "+")

            # Ligne du milieu
            mid = ""
            for y in range(self.columns):
                mid += "|" if self.cells[x][y].value & 8 else " "
                mid += "   "
            print(mid + "|")

        # Ligne du bas
        print("+" + "---+" * self.columns)

    def get_the_list(self) -> list[list[int]]:
        list_int: list[list[int]] = []
        list_int = [
            [self.cells[x][y].value for y in range(self.columns)]
            for x in range(self.rows)
        ]
        return list_int


class DisplayMaze:
    """Class for diplay the maze with mlx"""

    def __init__(
        self,
        cells: list[list[int]],
        path: str,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Initiliaze the maze's values, and defaults colors"""
        self.initialize_maze_settings(cells, path, entry, exit)
        self.wall_color = (255, 255, 255, 220)
        self.path_color = (100, 150, 110, 255)
        self.entry_color = (0, 215, 0, 200)
        self.exit_color = (0, 0, 215, 200)

        self.wall_size = 0.2
        self.wdw_percent = 0.4
        self.h_menu = 22
        self.printable = True

    def initialize_maze_settings(
        self,
        cells: list[list[int]],
        path: str,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Initialize maze's settings"""
        self.cells = cells
        self.rows = len(cells)
        self.column = len(cells[0])
        self.entry = entry
        self.exit = exit
        self.path = path
        self.path_visible = False

    def intialize_display_settings(self) -> None:
        """Initialize mlx and window's settings"""
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        self.calculate_img_values()

        try:
            if not self.printable:
                raise Exception(
                    "The maze can't be displayed, not readable or too big"
                    )
            self.win_ptr = self.m.mlx_new_window(
                self.mlx_ptr, self.w_wdw, self.h_wdw, "toto"
            )
            self.img = self.m.mlx_new_image(
                self.mlx_ptr,
                self.w_img,
                self.h_img
                )
            self.data, self.bit_per_pixel, self.size_line, the_format = (
                self.m.mlx_get_data_addr(self.img)
            )
            self.menu_settings()
            self.draw()
        except Exception as e:
            print(e)

    def calculate_img_values(self) -> None:
        """Calculate the value of a cell and of a wall in pixel"""
        ret, self.w, self.h = self.m.mlx_get_screen_size(self.mlx_ptr)
        self.cell_size = 0
        self.wall = 0
        wdw_size = self.wdw_percent

        while self.cell_size < 5 or self.wall < 1:
            self.w_wdw = int(self.w * wdw_size)
            self.h_wdw = int(self.h * wdw_size)

            w_cell = int(
                self.w_wdw /
                (self.column + ((self.column + 1) * self.wall_size))
            )
            h_cell = int(
                (self.h_wdw - self.h_menu) /
                (self.rows + ((self.rows + 1) * self.wall_size))
            )

            if w_cell > h_cell:
                self.cell_size = h_cell
            else:
                self.cell_size = w_cell

            self.wall = int(self.cell_size * self.wall_size)
            wdw_size += 0.05

        if (wdw_size > 1):
            self.printable = False
            pass

        self.w_img = self.column * (self.cell_size + self.wall) + self.wall
        self.h_img = self.rows * (self.cell_size + self.wall) + self.wall
        self.w_wdw = self.w_img + 20
        self.h_wdw = self.h_img + 20 + self.h_menu
        self.w_offset = 10
        self.h_offset = 10

    def menu_settings(self) -> None:
        """Create and print the menu in the window"""
        single_char = 6
        h_menu = self.h_wdw - self.h_menu
        color = 0xFFFFFF
        options = [
            "1: Regenerate",
            "2: Show/Hide path",
            "3: Wall color",
            "4: Exit"
            ]
        space_menu = int(
            (self.w_wdw -
             (single_char * sum([len(element) for element in options]))) /
            (len(options) + 1)
        )
        for i in range(0, len(options)):
            if not i == 0:
                position = (i + 1) * space_menu + single_char * sum(
                    [len(element) for element in options[:i]]
                )
            else:
                position = space_menu
            self.m.mlx_string_put(
                self.mlx_ptr, self.win_ptr, position, h_menu, color, options[i]
            )

    def gere_close(self, _: Any):
        """For closing the window"""
        self.m.mlx_loop_exit(self.mlx_ptr)

    def draw_walls(self, color: tuple[int, int, int, int]) -> None:
        """Draw the walls of the maze"""
        for x in range(0, self.rows):
            for y in range(0, self.column):
                cell = self.cells[x][y]
                if cell & 1 == 1:
                    for i in range(0, self.cell_size + 2 * self.wall):
                        for j in range(0, self.wall):
                            offset = (
                                (x * (self.cell_size + self.wall) + j) *
                                self.size_line +
                                (y * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8)
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if cell & 8 == 8:
                    for i in range(0, self.wall):
                        for j in range(0, self.wall + self.cell_size):
                            offset = (
                                (x * (self.cell_size + self.wall) + j) *
                                self.size_line +
                                (y * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8)
                            )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if y == self.column - 1:
                    for i in range(
                        self.cell_size + self.wall, self.cell_size + (self.wall * 2)
                    ):
                        for j in range(0, self.wall + self.cell_size):
                            offset = (
                                (x * (self.cell_size + self.wall) + j) *
                                self.size_line +
                                (y * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8)
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if x == self.rows - 1:
                    for i in range(0, self.cell_size + 2 * self.wall):
                        for j in range(
                            self.cell_size + self.wall,
                            self.cell_size + (2 * self.wall)
                        ):
                            offset = (
                                (x * (self.cell_size + self.wall) + j) *
                                self.size_line +
                                (y * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8)
                            )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

    def color_forty_two(self,
                        x: int,
                        y: int,
                        color: tuple[int, int, int, int]) -> None:
        """Color forty-two's symbol to the same color of walls"""
        for i in range(self.wall, self.cell_size):
            for j in range(self.wall, self.cell_size):
                offset = (
                    (x * (self.cell_size + self.wall) + j) * self.size_line +
                    (y * (self.cell_size + self.wall) + i) *
                    (self.bit_per_pixel // 8)
                    )
                for k in range(0, 4):
                    self.data[offset + k] = color[k]

    def color_a_case(self,
                     x: int,
                     y: int,
                     color: tuple[int, int, int, int]) -> None:
        """Color the inside of a cell"""
        for i in range(self.wall, self.cell_size + self.wall):
            for j in range(self.wall, self.cell_size + self.wall):
                offset = (
                    (x * (self.cell_size + self.wall) + j) * self.size_line +
                    (y * (self.cell_size + self.wall) + i) *
                    (self.bit_per_pixel // 8)
                )
                for k in range(0, 4):
                    self.data[offset + k] = color[k]

    def draw_forty_two(self, color: tuple[int, int, int, int]) -> None:
        """Draw the forty-two symbol's walls"""
        x: int = int(self.rows / 2)
        y: int = int(self.column / 2)
        for i in range(1, 4):
            self.color_forty_two(x, y + i, color)
            self.color_forty_two(x - 2, y + i, color)
            self.color_forty_two(x + 2, y + i, color)
            self.color_forty_two(x, y - i, color)

        for i in range(0, 3):
            self.color_forty_two(x - i, y - 3, color)
            self.color_forty_two(x + i, y - 1, color)

        self.color_forty_two(x - 1, y + 3, color)
        self.color_forty_two(x + 1, y + 1, color)
        self.color_forty_two(x - 1, y - 1, color)
        self.color_forty_two(x - 2, y - 1, color)

    def draw_the_path(self, color: tuple[int, int, int, int]) -> None:
        """Draw or undraw the path between the entry to the exit"""
        x = self.entry[0]
        y = self.entry[1]
        if self.path_visible:
            color = (0, 0, 0, 255)
            self.path_visible = False
        else:
            self.path_visible = True

        for i in self.path[:-1]:
            if i == "N":
                self.color_a_case(x - 1, y, color)
                x -= 1
            elif i == "E":
                self.color_a_case(x, y + 1, color)
                y += 1
            elif i == "S":
                self.color_a_case(x + 1, y, color)
                x += 1
            elif i == "W":
                self.color_a_case(x, y - 1, color)
                y -= 1

    def clean_image(self) -> None:
        """Reintialize the image to a black backscreen"""
        color = (0, 0, 0, 255)
        for x in range(self.h_img):
            for y in range(self.w_img):
                offset = x * self.size_line + y * (self.bit_per_pixel // 8)
                for k in range(0, 4):
                    self.data[offset + k] = color[k]

    def mymouse(self, button, x, y, mystuff: Any) -> None:
        """Manage operations related to mouse click in the window"""
        print(f"Got mouse event! button {button} at {x},{y}.")

    def mykey(self, keynum: int, mystuff: Any) -> None:
        """Manages some operations related to key activation"""
        # print(f"Got key {keynum}, and got my stuff back:")
        # print(mystuff)
        if keynum == 32:
            self.m.mlx_mouse_hook(self.win_ptr, None, None)

        elif keynum == 65307 or keynum == 52 or keynum == 65430:
            self.m.mlx_loop_exit(self.mlx_ptr)

        elif keynum == 49 or keynum == 65436:
            self.regenerate = True
            self.m.mlx_loop_exit(self.mlx_ptr)

        elif keynum == 50 or keynum == 65433:
            self.draw_the_path(self.path_color)
            self.display(None)

        elif keynum == 51 or keynum == 65435:
            self.wall_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                255,
            )
            if self.path_visible:
                self.path_visible = False
            else:
                self.path_visible = True
            self.draw()

    def display(self, _: Any) -> None:
        """Display the image in the window"""
        self.m.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img, self.w_offset, self.h_offset
        )
        self.m.mlx_sync(self.mlx_ptr, 2, self.win_ptr)

    def draw(self) -> None:
        """Draw in image's buffer"""
        self.regenerate = False
        self.clean_image()
        self.draw_walls(self.wall_color)
        self.draw_forty_two(self.wall_color)
        self.color_a_case(self.entry[0], self.entry[1], self.entry_color)
        self.color_a_case(self.exit[0], self.exit[1], self.exit_color)
        self.draw_the_path(self.path_color)

        self.m.mlx_mouse_hook(self.win_ptr, self.mymouse, None)
        self.m.mlx_key_hook(self.win_ptr, self.mykey, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.gere_close, None)
        self.display(None)

        self.m.mlx_loop(self.mlx_ptr)

        if self.regenerate:
            self.m.mlx_destroy_image(self.mlx_ptr, self.img)
            self.img = self.m.mlx_new_image(
                self.mlx_ptr, self.w_img, self.h_img
                )
            self.data, self.bit_per_pixel, self.size_line, the_format = (
                self.m.mlx_get_data_addr(self.img)
            )
            dic: dict[str, Any] = {
                "WIDTH": self.column,
                "HEIGHT": self.rows,
                "ENTRY": self.entry,
                "EXIT": self.exit,
                "OUTPUT_FILE": "result.txt",
            }
            maze = GrowingTree(dic)
            self.initialize_maze_settings(
                maze.get_the_list(), maze.path, self.entry, self.exit
            )
            self.draw()
