import random
from typing import Any
from mlx import Mlx
from mazeinit import MazeInit
from mazegeneration import MazeGenerator


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
        self.h_menu = 25
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

        while self.cell_size < 10 or self.wall < 2:
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
        if self.w_wdw < int(self.w * wdw_size):
            self.w_wdw = int(self.w * wdw_size)
        self.w_offset = int((self.w_wdw - self.w_img) / 2)
        self.h_offset = int((self.h_wdw - self.h_menu - self.h_img) / 2)

    def menu_settings(self) -> None:
        """Create and print the menu in the window"""
        single_char = 6
        h_menu = self.h_wdw - self.h_menu
        color = 0xFFFFFF
        options = [
            "1: Regenerate",
            "2: Path",
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
        for x in range(0, self.column):
            for y in range(0, self.rows):
                cell = self.cells[y][x]
                if cell & 1 == 1:
                    for i in range(0, self.cell_size + 2 * self.wall):
                        for j in range(0, self.wall):
                            offset = (
                                (x * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8) +
                                (y * (self.cell_size + self.wall) + j) *
                                self.size_line
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if cell & 8 == 8:
                    for i in range(0, self.wall):
                        for j in range(0, self.cell_size + self.wall):
                            offset = (
                                (x * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8) +
                                (y * (self.cell_size + self.wall) + j) *
                                self.size_line
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if x == self.column - 1:
                    for i in range(
                        self.cell_size + self.wall,
                        self.cell_size + (self.wall * 2)
                    ):
                        for j in range(0, self.wall + self.cell_size):
                            offset = (
                                (x * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8) +
                                (y * (self.cell_size + self.wall) + j) *
                                self.size_line
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if y == self.rows - 1:
                    for i in range(0, self.cell_size + 2 * self.wall):
                        for j in range(
                            self.cell_size + self.wall,
                            self.cell_size + (2 * self.wall)
                        ):
                            offset = (
                                (x * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8) +
                                (y * (self.cell_size + self.wall) + j) *
                                self.size_line
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
        cell = self.cells[y][x]
        for i in range(self.wall + 2, self.cell_size + self.wall - 2):
            for j in range(self.wall + 2, self.cell_size + self.wall - 2):
                offset = (
                    (x * (self.cell_size + self.wall) + i) *
                    (self.bit_per_pixel // 8) +
                    (y * (self.cell_size + self.wall) + j) * self.size_line
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
                self.color_a_case(x, y - 1, color)
                y -= 1
            elif i == "E":
                self.color_a_case(x + 1, y, color)
                x += 1
            elif i == "S":
                self.color_a_case(x, y + 1, color)
                y += 1
            elif i == "W":
                self.color_a_case(x - 1, y, color)
                x -= 1
        self.display(None)

    def clean_image(self) -> None:
        """Reintialize the image to a black backscreen"""
        color = (0, 0, 0, 255)
        for x in range(self.h_img):
            for y in range(self.w_img):
                offset = x * self.size_line + y * (self.bit_per_pixel // 8)
                for k in range(0, 4):
                    self.data[offset + k] = color[k]

    def guess_the_path(self) -> None:
        """Try to find the path to the exit"""
        if self.path_visible:
            self.draw_the_path(self.path_color)
        x = self.entry[0]
        y = self.entry[1]
        while not (x == self.exit[0] or self.exit[1]):
            pass

    def mymouse(self, button, x, y, mystuff: Any) -> None:
        """Manage operations related to mouse click in the window"""
        print(f"Got mouse event! button {button} at {x},{y}.")

    def mykey(self, keynum: int, mystuff: Any) -> None:
        """Manages some operations related to key activation"""

        if keynum == 32:
            self.m.mlx_mouse_hook(self.win_ptr, None, None)

        elif keynum == 65307 or keynum == 52 or keynum == 65430:
            self.m.mlx_loop_exit(self.mlx_ptr)

        elif keynum == 49 or keynum == 65436:
            self.regenerate = True
            self.m.mlx_loop_exit(self.mlx_ptr)

        elif keynum == 50 or keynum == 65433:
            self.draw_the_path(self.path_color)

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
            self.draw_walls(self.wall_color)
            if not (self.column < 11 or self.rows < 9):
                self.draw_forty_two(self.wall_color)
            self.display(None)

        elif keynum == 52 or keynum == 65433:
            self.guess_the_path()

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
        if not (self.column < 11 or self.rows < 9):
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
            init = MazeInit('config.txt')
            maze = MazeGenerator(init())
            self.initialize_maze_settings(
                maze.array, maze.road,
                init.config['ENTRY'], init.config['EXIT']
            )
            self.draw()
            return

        self.m.mlx_destroy_image(self.mlx_ptr, self.img)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_release(self.mlx_ptr)
