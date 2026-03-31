
from datetime import datetime
import random
from typing import Any, Callable
import functools
from os.path import exists
import functools

def func_timer(to_print: str) -> Callable[..., Any]:
    def timing(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def func_wrap(*args: Any, **kwargs: Any) -> Any:
            time_start = datetime.now()
            print(to_print, "start ...")
            res: Any = func(*args, **kwargs)
            time_end = datetime.now() - time_start
            print(to_print, "time:", time_end.total_seconds(), "s")
            return res
        return func_wrap
    return timing

class MazeGenerateError(Exception):
    pass

class MazeGenerator:

    class UnperfectMaze:


        def __init__(self, config: dict[str, str | int | bool]) -> None:

            self.config: dict[str, str | int | bool] = config
            self.array: list[list[int]] = []
            # self.memory: list[list[int]] = []
            self.pos_x = 0
            self.pos_y = 0
            self.config_width = config["WIDTH"]
            self.config_height = config["HEIGHT"]
            self.prime_list: list[list[int]] = [[True for _ in range(self.config["WIDTH"] + 1)] for _ in range(self.config["HEIGHT"] + 1)]

            #------------------------------------------ SEED SETUP

            if config["SEED"] != "Random":
                random.seed(config["SEED"])
                print(config["SEED"])
            else:
                seed = random.randint(0, 10**4000)
                random.seed(seed)
                print(seed)

            #------------------------------------------ PRIME LIST SETUP

            for i in range(config["HEIGHT"]):
                self.prime_list[i][-1] = False

                self.array.append([0b0] * (config["WIDTH"]))
                self.array[i][0] += 0b1000
                self.array[i][config["WIDTH"] - 1] += 0b0010

            for i in range(config["WIDTH"]):
                self.prime_list[-1][i] = False

                self.array[0][i] += 0b0001
                self.array[config["HEIGHT"] - 1][i] += 0b0100

            #------------------------------------------- GENERATE


            self.generate(self.config["SHAPE"])

            # VALUES ENTRY / EXIT NOT VERIFIED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            #self.show()

            self.road: str = ""
            try:
                self.road: str = self.resolve()
            except MazeGenerateError as e:
                print("RESOLVE FAILED", e)
            if self.road:
                print(end="MAZE RESOLVED : ")
                print(self.road)

            #self.show_pretty(True)
            #self.show_pretty(False)
            self.create_file(self.road)


        @func_timer("creating file")
        def create_file(self, road: str) -> None:

            with open(self.config["OUTPUT_FILE"], "w") as file:

                file.write(self.create_string())
                file.write("\n")

                x, y = self.config["ENTRY"]
                file.write(f"{x},{y}\n")
                x, y = self.config["EXIT"]
                file.write(f"{x},{y}\n")

                file.write(self.road)

        def create_string(self) -> str:
            out: list[str] = []
            for elem in self.array:
                for num in elem:
                    out.append(str("{0:x}".format(num)).capitalize())
                out.append("\n")
            return "".join(out)

        def set_road_show(self) -> None:
            agents: list[list[int]] = [["x" for _ in range(self.config["HEIGHT"])] for _ in range(self.config["WIDTH"])]
            pos_x, pos_y = self.config["ENTRY"]
            agents[pos_y][pos_x] = 5
            for elem in self.road:
                match elem:
                    case "S":
                        pos_y += 1
                    case "W":
                        pos_x -= 1
                    case "N":
                        pos_y -= 1
                    case "E":
                        pos_x += 1
                try:
                    agents[pos_y][pos_x] = 0
                except Exception:
                    break
            pos_x, pos_y = self.config["EXIT"]
            agents[pos_y][pos_x] = 3
            self.agents = agents

        def show(self) -> None:
            for elem in self.array:
                for num in elem:
                    print(str("{0:x}".format(num)).capitalize(), end=" ")
                print("")

        def show_pretty(self, values: bool = False) -> None:

            i: int
            j: int = 0
            for elem in self.array:
                line1 = ""
                line2 = ""
                line3 = ""
                i = 0
                for num in elem:
                    s1 = [" ", " ", " ", " "]
                    s2 = [" ", " ", " ", " "]
                    s3 = [" ", " ", " ", " "]

                    if bin(num % 2) == bin(1):
                        s1 = ["o", "-", "-", "o"]
                    num = int(num / 2)
                    if bin(num % 2) == bin(1):
                        s1[3] = "o"
                        s2[3] = "|"
                        s3[3] = "o"
                    num = int(num / 2)
                    if bin(num % 2) == bin(1):
                        s3 = ["o", "-", "-", "o"]
                    num = int(num / 2)
                    if bin(num % 2) == bin(1):
                        s1[0] = "o"
                        s2[0] = "|"
                        s3[0] = "o"
                    num = int(num / 2)
                    if bin(num % 2) == bin(1):
                        s2[1] = "X"
                        s2[2] = "X"

                    if values:
                        s2[2] = str(self.agents[j][i] % 10)
                        s2[1] = str(self.agents[j][i] // 10 % 10)

                    def list_in_str(data: list[str]) -> str:
                        out = ""
                        for elem in data:
                            out += elem
                        return out

                    line1 += list_in_str(s1)
                    line2 += list_in_str(s2)
                    line3 += list_in_str(s3)
                    i += 1
                print(line1)
                print(line2)
                print(line3)
                j += 1


        def get_north(self, shift_x: int = 0, shift_y: int = 0) -> str:
            return bin(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x]  % 2))

        def get_east(self, shift_x: int = 0, shift_y: int = 0) -> str:
            return bin(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) % 2)

        def get_south(self, shift_x: int = 0, shift_y: int = 0) -> str:
            return bin(int(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) / 2) % 2)

        def get_west(self, shift_x: int = 0, shift_y: int = 0) -> str:
            return bin(int(int(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) / 2) /2) % 2)

        @staticmethod
        def fast_get_north(array: list[int, int], shift_x: int = 0, shift_y: int = 0) -> str:
            return bin((array[shift_y][shift_x]) >> 0 & 1)

        @staticmethod
        def fast_get_east(array: list[int, int], shift_x: int = 0, shift_y: int = 0) -> str:
            return bin((array[shift_y][shift_x]) >> 1 & 1)

        @staticmethod
        def fast_get_south(array: list[int, int], shift_x: int = 0, shift_y: int = 0) -> str:
            return bin((array[shift_y][shift_x]) >> 2 & 1)

        @staticmethod
        def fast_get_west(array: list[int, int], shift_x: int = 0, shift_y: int = 0) -> str:
            return bin((array[shift_y][shift_x]) >> 3 & 1)


        @func_timer("resolving")
        def resolve(self) -> str:

            agents: list[list[int]] = [[0 for _ in range(self.config["HEIGHT"])] for _ in range(self.config["WIDTH"])]

            tree: list[tuple[int, int]]
            dest_x: int
            dest_y: int

            get_north = MazeGenerator.UnperfectMaze.fast_get_north
            get_east = MazeGenerator.UnperfectMaze.fast_get_east
            get_south = MazeGenerator.UnperfectMaze.fast_get_south
            get_west = MazeGenerator.UnperfectMaze.fast_get_west
            array = self.array

            pos_x, pos_y = self.config["ENTRY"]

            tree = [(pos_x, pos_y)]
            agents[pos_y][pos_x] = 1
            temp_i = 0
            while(tree):

                pos_x, pos_y = tree.pop(0)
                new_value = agents[pos_y][pos_x] + 1

                if get_north(array, pos_x, pos_y) == bin(0):
                    if new_value < agents[pos_y - 1][pos_x] or agents[pos_y - 1][pos_x] == 0:
                        agents[pos_y - 1][pos_x] = new_value
                        tree.append((pos_x, pos_y - 1))

                if get_east(array, pos_x, pos_y) == bin(0):
                    if new_value < agents[pos_y][pos_x + 1] or agents[pos_y][pos_x + 1] == 0:
                        agents[pos_y][pos_x + 1] = new_value
                        tree.append((pos_x + 1, pos_y))

                if get_south(array, pos_x, pos_y) == bin(0):
                    if new_value < agents[pos_y + 1][pos_x] or agents[pos_y + 1][pos_x] == 0:
                        agents[pos_y + 1][pos_x] = new_value
                        tree.append((pos_x, pos_y + 1))

                if get_west(array, pos_x, pos_y) == bin(0):
                    if new_value < agents[pos_y][pos_x - 1] or agents[pos_y][pos_x - 1] == 0:
                        agents[pos_y][pos_x - 1] = new_value
                        tree.append((pos_x - 1, pos_y))
                temp_i += 1


            pos_x, pos_y = self.config["EXIT"]

            temp_i = 0
            road: list[str] = []
            value: float = agents[pos_y][pos_x]
            while(value != 1):

                value = agents[pos_y][pos_x]
                shortest: str = ""

                if get_north(array, pos_x, pos_y) == bin(0):
                    if value > agents[pos_y - 1][pos_x]:
                        value = agents[pos_y - 1][pos_x]
                        shortest = "S"

                if get_east(array, pos_x, pos_y) == bin(0):
                    if value > agents[pos_y][pos_x + 1]:
                        value = agents[pos_y][pos_x + 1]
                        shortest = "W"

                if get_south(array, pos_x, pos_y) == bin(0):
                    if value > agents[pos_y + 1][pos_x]:
                        value = agents[pos_y + 1][pos_x]
                        shortest = "N"

                if get_west(array, pos_x, pos_y) == bin(0):
                    if value > agents[pos_y][pos_x - 1]:
                        value = agents[pos_y][pos_x - 1]
                        shortest = "E"

                match shortest:
                    case "S":
                        pos_y -= 1
                    case "W":
                        pos_x += 1
                    case "N":
                        pos_y += 1
                    case "E":
                        pos_x -= 1
                    case _:
                        self.agents = agents
                        raise MazeGenerateError(f"Impossible road occured: {''.join(road)}")

                road.append(shortest)
            return "".join(road[::-1])

        @staticmethod
        def destroy_wall(array: list[list[int]], targets: tuple[tuple[int, int], tuple[int, int]]) -> None:

            target, sender = targets
            target_x, target_y = target
            sender_x, sender_y = sender
            if target_x == sender_x:
                if target_y > sender_y:
                    # target at down
                    array[target_y][target_x] -= 0b0001
                    array[sender_y][sender_x] -= 0b0100
                else:
                    # target at up
                    array[target_y][target_x] -= 0b0100
                    array[sender_y][sender_x] -= 0b0001
            else:
                if target_x > sender_x:
                    # target at right
                    array[target_y][target_x] -= 0b1000
                    array[sender_y][sender_x] -= 0b0010
                else:
                    # target at left
                    array[target_y][target_x] -= 0b0010
                    array[sender_y][sender_x] -= 0b1000


        def setup_agents(self, nbr: int) -> list[list[int]]:
            agents: list[list[int]] = [[0 for _ in range(self.config["WIDTH"])] for _ in range(self.config["HEIGHT"])]

            possibles: list[typle[int, int]] = [
                    (0,0),
                    (self.config["WIDTH"] - 1, 0),
                    (0, self.config["HEIGHT"] - 1),
                    (self.config["WIDTH"] - 1, self.config["HEIGHT"] - 1),
                    (int(self.config["WIDTH"] / 2) - 3 + 5,
                    (int(self.config["HEIGHT"] / 2) - 2 + 1))
                    ]
            random.shuffle(possibles)
            start: set[tuples[int, int]] = set()
            for i,( x, y) in enumerate(possibles, start = 1):
                agents[y][x] = i
                start.add((x, y))
                if i == nbr:
                    break
            return (agents, start)

        @func_timer("generating")
        def maze_explore_and_merge(self, max_pairs: int) -> None:

            if not 0 < max_pairs < 6:
                raise Exception("Agents in the maze is max 5, min 1")

            visited: list[list[bool]]
            agents: list[list[int]]
            targets: dict[typle[int, int]]
            tree: set[tuple[int, int]]
            pair_end: int
            pairs: set[set[int]]

            get_north = MazeGenerator.UnperfectMaze.fast_get_north
            get_east = MazeGenerator.UnperfectMaze.fast_get_east
            get_south = MazeGenerator.UnperfectMaze.fast_get_south
            get_west = MazeGenerator.UnperfectMaze.fast_get_west
            destroy_wall = MazeGenerator.UnperfectMaze.destroy_wall

            while(1):

                targets = {}
                agents, tree = self.setup_agents(max_pairs)
                prime_list = self.prime_list
                array = self.array
                pair_end = max_pairs
                pairs = set()

                while(tree):

                    while(tree):

                        new_branch = random.choice(list(tree))
                        tree.remove(new_branch)
                        pos_x, pos_y = new_branch

                        if new_branch in targets:
                            targets.pop(new_branch)

                        agent_value = agents[pos_y][pos_x]

                        if prime_list[pos_y - 1][pos_x]:
                            if pair_end and {target_value := agents[pos_y - 1][pos_x], agent_value} not in pairs:
                                if target_value and target_value != agent_value:
                                    if get_north(array, pos_x, pos_y) == bin(1):
                                        destroy_wall(array, ((pos_x, pos_y - 1) , new_branch))
                                    if (pos_x, pos_y - 1) in targets.keys():
                                        targets.pop((pos_x, pos_y - 1))
                                    pairs.add(frozenset({agent_value, target_value}))
                                    pair_end -= 1

                            if not agents[pos_y - 1][ pos_x]:
                                targets.update({(pos_x, pos_y - 1) : new_branch})
                                if get_north(array, pos_x, pos_y) == bin(0):
                                    agents[pos_y - 1][pos_x] = agent_value
                                    tree.add((pos_x, pos_y - 1))

                        if prime_list[pos_y][ pos_x + 1]:
                            if pair_end and {target_value := agents[pos_y][pos_x + 1], agent_value} not in pairs:
                                if target_value and target_value != agent_value:
                                    if get_east(array, pos_x, pos_y) == bin(1):
                                        destroy_wall(array, ((pos_x + 1, pos_y) , new_branch))
                                    if (pos_x + 1, pos_y) in targets.keys():
                                        targets.pop((pos_x + 1, pos_y))
                                    pairs.add(frozenset({agent_value, target_value}))
                                    pair_end -= 1

                            if not agents[pos_y][ pos_x + 1]:
                                targets.update({(pos_x + 1, pos_y) : new_branch})
                                if get_east(array, pos_x, pos_y) == bin(0):
                                    agents[pos_y][pos_x + 1] = agent_value
                                    tree.add((pos_x + 1, pos_y))

                        if prime_list[pos_y + 1][ pos_x]:
                            if pair_end and {target_value := agents[pos_y + 1][pos_x], agent_value} not in pairs:
                                if target_value and target_value != agent_value:
                                    if get_south(array, pos_x, pos_y) == bin(1):
                                        destroy_wall(array, ((pos_x, pos_y + 1) , new_branch))
                                    if (pos_x, pos_y + 1) in targets.keys():
                                        targets.pop((pos_x, pos_y + 1))
                                    pairs.add(frozenset({agent_value, target_value}))
                                    pair_end -= 1

                            if not agents[pos_y + 1][ pos_x]:
                                targets.update({(pos_x, pos_y + 1) : new_branch})
                                if get_south(array, pos_x, pos_y) == bin(0):
                                    agents[pos_y + 1][pos_x] = agent_value
                                    tree.add((pos_x, pos_y + 1))

                        if prime_list[pos_y][ pos_x - 1]:
                            if pair_end and {target_value := agents[pos_y][pos_x - 1], agent_value} not in pairs:
                                if target_value and target_value != agent_value:
                                    if get_west(array, pos_x, pos_y) == bin(1):
                                        destroy_wall(array, ((pos_x - 1, pos_y) , new_branch))
                                    if (pos_x - 1, pos_y) in targets.keys():
                                        targets.pop((pos_x - 1, pos_y))
                                    pairs.add(frozenset({agent_value, target_value}))
                                    pair_end -= 1

                            if not visited[pos_y][ pos_x - 1]:
                                targets.update({(pos_x - 1, pos_y) : new_branch})
                                if get_west(array, pos_x, pos_y) == bin(0):
                                    agents[pos_y][pos_x - 1] = agent_value
                                    tree.add((pos_x - 1, pos_y))

                    if len(targets) > 0:
                        sample = random.sample(list(targets.items()), 1)[0]
                        targets.pop(sample[0])
                        tree = {sample[0]}
                        agents[sample[0][1]][sample[0][0]] = agents[sample[1][1]][sample[1][0]]
                        destroy_wall(array, sample)
                if self.config["PERFECT"] or pair_end == 0:
                    break
            return

        def draw_x(self, shift_x:int = 0, shift_y: int = 0) -> None:
            if self.pos_x + shift_x < 0 or self.pos_y + shift_y < 0:
                return

            try:
                if self.get_north(shift_x, shift_y + 1) != bin(1) and  self.get_south(shift_x, shift_y) != bin(1):
                    self.array[self.pos_y + shift_y ][self.pos_x + shift_x] += 0b0100
                    self.array[self.pos_y + shift_y + 1][self.pos_x + shift_x] += 0b001
            except Exception:
                return

        def draw_y(self, shift_x: int = 0, shift_y: int = 0) -> None:
            if self.pos_x + shift_x < 0 or self.pos_y + shift_y < 0:
                return

            try:
                if self.get_east(shift_x, shift_y) != bin(1) and self.get_west(shift_x + 1, shift_y) != bin(1):
                    self.array[self.pos_y + shift_y][self.pos_x + shift_x] += 0b0010
                    self.array[self.pos_y + shift_y][self.pos_x + 1 + shift_x] += 0b1000
            except Exception:
                return


        def get_circle_len(self, size_x:int = 0, size_y: int = 0, stairs:int = 0) -> dict[str, int]:

            len_x: int = ((stairs - 2) * 2) + size_x + 0
            len_y: int = ((stairs - 2) * 2) + size_y + 0

            return {"x": len_x, "y": len_y}


        def draw_circle(self, size_x:int = 0, size_y: int = 0, stairs: int = 0) -> bool:

            lenth: dict[str, int] = self.get_circle_len(size_x, size_y, stairs)
            self.pos_x -= int(lenth["x"] / 2) + 3
            self.pos_y -= int(lenth["y"] / 2) + 3
            self.pos_x += stairs + 1
            if self.pos_x <= 0 and self.pos_y <= 0:
                return False

            for i in range(size_x):
                self.draw_x()
                self.pos_x += 1
            for i in range(stairs):
                self.draw_x()
                self.draw_y(0, 1)
                self.pos_x += 1
                self.pos_y += 1
            self.draw_x()
            for i in range(size_y):
                self.draw_y(0, 1)
                self.pos_y += 1
            self.draw_x()
            self.pos_x -= 1
            self.pos_y += 1
            for i in range(stairs):
                self.draw_y()
                self.draw_x()
                self.pos_x -= 1
                self.pos_y += 1
            self.pos_y -= 1
            for i in range(size_x):
                self.draw_x()
                self.pos_x -= 1
            for i in range(stairs):
                self.pos_y -= 1
                self.draw_y(0, 1)
                self.draw_x()
                self.pos_x -= 1
            self.pos_y += 1
            for i in range(size_y):
                self.pos_y -= 1
                self.draw_y()
            self.pos_x += 1
            self.pos_y -= 1

            for i in range(stairs):
                self.draw_y()
                self.draw_x()
                self.pos_y -= 1
                self.pos_x += 1
            return True


        def generate_circles(self) -> None:

            start_x: int = int(self.config["WIDTH"] / 2)
            start_y: int = int(self.config["HEIGHT"] / 2)

            self.pos_x = start_x
            self.pos_y = start_y
            check = self.draw_circle(2, 4, 3)
            jump_x = 1 # random.randint(1, 2)
            jump_y = 1 # random.randint(1, 2)
            jump_stairs = 1 # random.randint(1, 2)
            c_x = 4
            c_y = 6
            c_stairs = 3
            check = True
            while (check):
                try:
                    self.pos_x = start_x
                    self.pos_y = start_y
                    check = self.draw_circle(c_x, c_y, c_stairs)
                    c_stairs += jump_stairs
                    c_x += jump_x
                    c_y += jump_y
                except MazeGenerateError:
                    break


        def generate_cells(self) -> None:

            self.pos_x = 0
            self.pos_y = 0

            for elem in self.array:
                i = 0
                while i < len(elem):
                    elem[i] = 0b1111
                    i += 1

        def generate_squares(self) -> None:

            self.pos_x = 0
            self.pos_y = 0

            for self.pos_y in range(self.config["HEIGHT"]):
                self.pos_x = 0
                while self.pos_x < self.config["WIDTH"]:
                    if self.pos_x % 2 == 0:
                        self.draw_y()
                    if self.pos_y % 2 == 0:
                        self.draw_x()
                    self.pos_x += 1
                print(self.pos_y)

        def draw_cross(self) -> None:

            self.pos_x = 0
            self.pos_y = 0

            i = 0
            self.pos_y = int(self.config["HEIGHT"] / 2)
            self.pos_x = 0
            while i < self.config["WIDTH"]:
                self.draw_x()
                self.pos_x += 1
                i += 1
            i = 0
            self.pos_x = int(self.config["WIDTH"] / 2)
            self.pos_y = 0
            while i < self.config["HEIGHT"]:
                self.draw_y()
                self.pos_y += 1
                i += 1

            i = 0
            self.pos_x = 0
            self.pos_y = 0
            while i < self.config["HEIGHT"]:
                self.draw_y(-1)
                self.draw_x()
                self.draw_y(self.config["WIDTH"] - i * 2 - 1)
                self.draw_x(self.config["WIDTH"] - i * 2 - 1)
                self.pos_x += 1
                self.pos_y += 1
                i += 1

        def draw_cube(self) -> None:
            self.prime_list[self.pos_y][self.pos_x] = False
            self.draw_x()
            self.draw_x(0, -1)
            self.draw_y()
            self.draw_y(-1, 0)

        def set_42_walls(self) -> None:
            # set: up left point
            from mazeinit import get_42_pos

            positions = get_42_pos(self.config["WIDTH"], self.config["HEIGHT"])

            for self.pos_x, self.pos_y in positions:
                self.draw_cube()

        def generate(self, indicator: str) -> None:
            entries = 5
            if self.config["PERFECT"]:
                entries = 1

            match indicator:
                case "Circle":
                    self.generate_circles()
                    self.draw_cross()
                case "Classic":
                    self.generate_cells()
                case "Square":
                    self.generate_squares()
                case _:
                    raise MazeGenerateError("unknow maze type")
            self.set_42_walls()
            self.maze_explorator(entries)





