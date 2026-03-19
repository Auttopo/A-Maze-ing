import random
from typing import Any

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
        self.rows: int = dic['HEIGHT']
        self.columns: int = dic['WIDTH']
        x_entry, y_entry = dic['ENTRY']
        x_exit, y_exit = dic['EXIT']
        self.output: str = dic['OUTPUT_FILE']
        self.path: str = ''
        self.cells: list[list[Cell]] = []
        for x in range(0, self.rows):
            self.cells.append([])
            for y in range(0, self.columns):
                self.cells[x].append(Cell(x, y, 15))
        self.forty_two()
        self.build_maze()
        self.no_cell_visited()
        self.entry = self.cells[x_entry][y_entry]
        self.exit = self.cells[x_exit][y_exit]
        self.find_path(self.entry, self.exit)

    def forty_two (self) -> None:
        """Initialize each cells of the 42 symbol"""
        x:int = int(self.rows / 2)
        y:int = int(self.columns / 2)
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

    def build_maze(self) -> None:
        """Create the maze according to Prim's algorithm"""

        cells_visited: list[Cell] = []
        x:int = int(self.rows / 2)
        y:int = int(self.columns / 2 - 1)
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
                    # case du dessous
                    active.value -= 1
                    target.value -= 4
                elif active.x - target.x == -1:
                    # case du dessus
                    active.value -= 4
                    target.value -= 1
                elif active.y - target.y == 1:
                    # case de gauche
                    active.value -= 8
                    target.value -= 2
                elif active.y - target.y == -1:
                    # case de droite
                    active.value -= 2
                    target.value -= 8
            else:
                cells_visited.remove(active)

    def no_cell_visited(self) -> None:
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                self.cells[x][y].visited = False
        self.forty_two

    def find_path(self, entry: Cell, exit: Cell) -> None:
        """Find the path from entry to exit"""
        entry.visited = True
        direction: str = ''
        while not(entry.x == exit.x and entry.y == exit.y):
            if (entry.value & 1 == 0
                and not self.cells[entry.x - 1][entry.y].visited):
                    direction = 'N'
                    print(direction)
                    self.find_path(self.cells[entry.x - 1][entry.y], exit)
            elif (entry.value & 2 == 0
                  and not self.cells[entry.x][entry.y + 1].visited):
                    direction = 'E'
                    print(direction)
                    self.find_path(self.cells[entry.x][entry.y + 1], exit)
            elif (entry.value & 4 == 0 
                  and not self.cells[entry.x + 1][entry.y].visited):
                    direction = 'S'
                    print(direction)
                    self.find_path(self.cells[entry.x + 1][entry.y], exit)
            elif (entry.value & 8 == 0 
                  and not self.cells[entry.x][entry.y - 1].visited):
                    direction = 'W'
                    print(direction)
                    self.find_path(self.cells[entry.x][entry.y - 1], exit)
            else:
                break
            self.path += direction

    def display(self) -> None:
    
        for x in range(0, self.rows):
            top = ""
            for y in range(0, self.columns):
                top += "+" + ("   " if not self.cells[x][y].value & 1 else "---")
            print(top + "+")
            
            # Ligne du milieu
            mid = ""
            for y in range(self.columns):
                mid += ("|" if self.cells[x][y].value & 8 else " ")
                mid += "   "
            print(mid + "|")
        
        # Ligne du bas
        print("+" + "---+" * self.columns)