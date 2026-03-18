import random

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
    def __init__(self, dic: dict[str, int]) -> None:
        self.row = dic['HEIGHT']
        self.column = dic['WIDTH']
        self.cells: list[list[Cell]] = []
        for x in range(0, self.row):
            for y in range(0, self.column):
                self.cells[x].append(Cell(x, y, 15))
        self.forty_two()

    def forty_two (self) -> None:
        """Initialize each cells of the 42 symbol"""
        x:int = int(self.row / 2)
        y:int = int(self.column / 2)
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

    def build_maze(self) -> list[list[Cell]]:
        """Create the maze according to Prim's algorithm"""

        cells_visited: list[Cell] = []
        x:int = int(self.row / 2)
        y:int = int(self.column / 2 - 1)
        active: Cell = self.cells[x][y]

        while active.symbol:
            x = random.randint(0, self.row - 1)
            y = random.randint(0, self.column - 1)
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
            if not active.x == self.row - 1:
                target = self.cells[active.x + 1][active.y]
                if not target.symbol and not target.visited:
                    border.append(target)
            if not active.y == 0:
                target = self.cells[active.x][active.y - 1]
                if not target.symbol and not target.visited:
                    border.append(target)
            if not active.y == self.column - 1:
                target = self.cells[active.x][active.y + 1]
                if not target.symbol and not target.visited:
                    border.append(target)
            
            if border:
                target = border[random.randint(0, len(border) - 1)]
                cells_visited.append(target)
                if active.x - target.x == 1:
                    # case du dessous
                    active.value -= 4
                    target.value -= 1
                elif active.x - target.x == -1:
                    # case du dessus
                    active.value -= 1
                    target.value -= 4
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

        return self.cells    
    