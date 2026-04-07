
import random
from typing import Any, Callable, TypedDict, TypeAlias
from mazegen.mazeinit import get_42_pos


class MazeGenerator:
    """ main class for generation """

    class MazeGenerateError(Exception):
        """ precise exception for generation debug """
        pass

    class MazeDict(TypedDict):
        """ typing helper, contain all keys for generation """

        WIDTH: int
        HEIGHT: int
        ENTRY: tuple[int, int]
        EXIT: tuple[int, int]
        OUTPUT_FILE: str
        PERFECT: bool
        SEED: int | str
        SHAPE: str
        OUTPUT_FILE_OVERRIDE: bool

    def __init__(
            self, config: dict[str, Any], *, no_gen: bool = False) -> None:
        """ init of generation utilities and generate in same time """

        MazeDict: TypeAlias = dict[str, Any]

        self.config: MazeDict = config
        self.array: list[list[int]] = []
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.road: str = ""
        self.prime_list: list[list[bool]] = [
            [True for _ in range(self.config["WIDTH"] + 1)]
            for _ in range(self.config["HEIGHT"] + 1)
        ]

        # ------------------------------------------ SEED SETUP

        self.seed: int
        if not config.get("SEED"):
            config.update({"SEED": "Random"})
        if config["SEED"] != "Random":
            random.seed(config["SEED"])
            seed = config["SEED"]
        else:
            seed = random.randint(0, 10**4000)
            random.seed(seed)

        # ------------------------------------------ PRIME LIST SETUP

        i: int
        for i in range(config["HEIGHT"]):
            self.prime_list[i][-1] = False

            self.array.append([0b0] * (config["WIDTH"]))
            self.array[i][0] += 0b1000
            self.array[i][config["WIDTH"] - 1] += 0b0010

        for i in range(config["WIDTH"]):
            self.prime_list[-1][i] = False

            self.array[0][i] += 0b0001
            self.array[config["HEIGHT"] - 1][i] += 0b0100

        # ------------------------------------------- GENERATE

        print("Seed used :", seed)
        print("Shape used :", config["SHAPE"])
        print("Is perfect :", config["PERFECT"])
        print("Entry :", config["ENTRY"])
        print("Exit :", config["EXIT"])

        if not no_gen:
            self.generate(self.config["SHAPE"])

    def get_maze(self) -> list[list[int]]:
        return self.array

    def update_config(self, new_data: dict[str, Any]) -> None:
        self.config.update(new_data)

    def create_file(self) -> None:
        """ create the file with maze, road to exit, entry and exit pos """

        with open(self.config["OUTPUT_FILE"], "w") as file:
            file.write(self.create_string())
            file.write("\n")

            x: int
            y: int
            if self.config.get("ENTRY"):
                x, y = self.config["ENTRY"]
                file.write(f"{x},{y}\n")
            if self.config.get("EXIT"):
                x, y = self.config["EXIT"]
                file.write(f"{x},{y}\n")

            file.write(self.road)

    def create_string(self) -> str:
        """ create the hexadecimal maze string """
        out: list[str] = []
        elem: list[int]
        num: int
        for elem in self.array:
            for num in elem:
                out.append(str("{0:x}".format(num)).capitalize())
            out.append("\n")
        return "".join(out)

    def get_north(self, shift_x: int = 0, shift_y: int = 0) -> str:
        """ get the north wall bit. with few parameters """
        return bin(
                (self.array[self.pos_y + shift_y][self.pos_x + shift_x]
                 ) >> 0 & 1)

    def get_east(self, shift_x: int = 0, shift_y: int = 0) -> str:
        """ get the east wall bit. with few parameters """
        return bin(
                (self.array[self.pos_y + shift_y][self.pos_x + shift_x]
                 ) >> 1 & 1)

    def get_south(self, shift_x: int = 0, shift_y: int = 0) -> str:
        """ get the north wall bit. with few parameters """
        return bin(
                (self.array[self.pos_y + shift_y][self.pos_x + shift_x]
                 ) >> 2 & 1)

    def get_west(self, shift_x: int = 0, shift_y: int = 0) -> str:
        """ get the north wall bit. with few parameters """
        return bin(
                (self.array[self.pos_y + shift_y][self.pos_x + shift_x]
                 ) >> 3 & 1)

    @staticmethod
    def fast_get_north(
        array: list[list[int]], shift_x: int = 0, shift_y: int = 0
    ) -> int:
        """ get the north wall bit """
        """ optimised for local binding and no lookup """
        return ((array[shift_y][shift_x]) >> 0 & 1)

    @staticmethod
    def fast_get_east(
        array: list[list[int]], shift_x: int = 0, shift_y: int = 0
    ) -> int:
        """ get the east wall bit """
        """ optimised for local binding and no lookup """
        return ((array[shift_y][shift_x]) >> 1 & 1)

    @staticmethod
    def fast_get_south(
        array: list[list[int]], shift_x: int = 0, shift_y: int = 0
    ) -> int:
        """ get the south wall bit """
        """ optimised for local binding and no lookup """
        return ((array[shift_y][shift_x]) >> 2 & 1)

    @staticmethod
    def fast_get_west(
        array: list[list[int]], shift_x: int = 0, shift_y: int = 0
    ) -> int:
        """ get the west wall bit """
        """ optimised for local binding and no lookup """
        return ((array[shift_y][shift_x]) >> 3 & 1)

    def resolve(self) -> str:
        """ resolve the maze with agents communication """
        """Usage: each agent give the distance beetwin him and the start"""
        """ if an agent have differents possibility
        he keep the shortest way """

        agents: list[list[int]] = [
            [0 for _ in range(self.config["WIDTH"])]
            for _ in range(self.config["HEIGHT"])
        ]

        tree: list[tuple[int, int]]

        get_north: Callable[..., int] = MazeGenerator.fast_get_north
        get_east: Callable[..., int] = MazeGenerator.fast_get_east
        get_south: Callable[..., int] = MazeGenerator.fast_get_south
        get_west: Callable[..., int] = MazeGenerator.fast_get_west
        array: list[list[int]] = self.array

        pos_x: int
        pos_y: int
        pos_x, pos_y = self.config["ENTRY"]
        tree = [(pos_x, pos_y)]
        agents[pos_y][pos_x] = 1

        # create the distances map
        while tree:
            pos_x, pos_y = tree.pop(0)
            new_value: int = agents[pos_y][pos_x] + 1

            if not get_north(array, pos_x, pos_y):
                if (
                    new_value < agents[pos_y - 1][pos_x]
                    or agents[pos_y - 1][pos_x] == 0
                ):
                    agents[pos_y - 1][pos_x] = new_value
                    tree.append((pos_x, pos_y - 1))

            if not get_east(array, pos_x, pos_y):
                if (
                    new_value < agents[pos_y][pos_x + 1]
                    or agents[pos_y][pos_x + 1] == 0
                ):
                    agents[pos_y][pos_x + 1] = new_value
                    tree.append((pos_x + 1, pos_y))

            if not get_south(array, pos_x, pos_y):
                if (
                    new_value < agents[pos_y + 1][pos_x]
                    or agents[pos_y + 1][pos_x] == 0
                ):
                    agents[pos_y + 1][pos_x] = new_value
                    tree.append((pos_x, pos_y + 1))

            if not get_west(array, pos_x, pos_y):
                if (
                    new_value < agents[pos_y][pos_x - 1]
                    or agents[pos_y][pos_x - 1] == 0
                ):
                    agents[pos_y][pos_x - 1] = new_value
                    tree.append((pos_x - 1, pos_y))

        pos_x, pos_y = self.config["EXIT"]

        road: list[str] = []
        value: int = agents[pos_y][pos_x]
        # create the exit path from the en
        while value != 1:
            value = agents[pos_y][pos_x]
            shortest: str = ""

            if not get_north(array, pos_x, pos_y):
                if value > agents[pos_y - 1][pos_x]:
                    value = agents[pos_y - 1][pos_x]
                    shortest = "S"

            if not get_east(array, pos_x, pos_y):
                if value > agents[pos_y][pos_x + 1]:
                    value = agents[pos_y][pos_x + 1]
                    shortest = "W"

            if not get_south(array, pos_x, pos_y):
                if value > agents[pos_y + 1][pos_x]:
                    value = agents[pos_y + 1][pos_x]
                    shortest = "N"

            if not get_west(array, pos_x, pos_y):
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
                    raise self.MazeGenerateError(
                        f"Impossible road occured: {''.join(road)}"
                    )

            road.append(shortest)

        self.road = "".join(road[::-1])
        return "".join(road[::-1])

    @staticmethod
    def create_wall(
        array: list[list[int]],
        targets: tuple[tuple[int, int], tuple[int, int]]
    ) -> None:
        """ create a wall beetwin two position """
        """ Usage: assure the unperfect maze easily,
            in case of same start area for end/start,
            all junction beetwin start and end area are stored
            and a passage is created at end """

        target: tuple[int, int]
        sender: tuple[int, int]
        target_x: int
        target_y: int
        sender_x: int
        sender_y: int
        target, sender = targets
        target_x, target_y = target
        sender_x, sender_y = sender
        if target_x == sender_x:
            if target_y > sender_y:
                # target at down
                array[target_y][target_x] += 0b0001
                array[sender_y][sender_x] += 0b0100
            else:
                # target at up
                array[target_y][target_x] += 0b0100
                array[sender_y][sender_x] += 0b0001
        else:
            if target_x > sender_x:
                # target at right
                array[target_y][target_x] += 0b1000
                array[sender_y][sender_x] += 0b0010
            else:
                # target at left
                array[target_y][target_x] += 0b0010
                array[sender_y][sender_x] += 0b1000

    @staticmethod
    def destroy_wall(
        array: list[list[int]],
        targets: tuple[tuple[int, int], tuple[int, int]]
    ) -> None:
        """ destoy a wall beetwin two position """

        target: tuple[int, int]
        sender: tuple[int, int]
        target_x: int
        target_y: int
        sender_x: int
        sender_y: int
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

    def setup_agents(
            self, start_agents: set[tuple[int, int]]
            ) -> list[list[int]]:
        """ setup agents for the exploration """
        """ Usage: here agents just communicate common origin """

        agents: list[list[int]] = [
            [0 for _ in range(self.config["WIDTH"])]
            for _ in range(self.config["HEIGHT"])
        ]

        x: int
        y: int
        i: int
        elem: tuple[int, int]
        for i, elem in enumerate(start_agents, start=1):
            x, y = elem
            agents[y][x] = i

        return agents

    @staticmethod
    def check_process(
                    wall_check: Callable[..., int],
                    array: list[list[int]],
                    pos_x: int,
                    pos_y: int,
                    branch: tuple[int, int],

                    prime_list: list[list[bool]],
                    targets: dict[tuple[int, int], tuple[int, int]],
                    agent_value: int,

                    agents: list[list[int]],
                    tree: set[tuple[int, int]],
                    common: set[frozenset[tuple[int, int]]],
                    create_wall: Callable[..., None]
                ) -> None:
        """ all the cheking process for the generation """

        if prime_list[pos_y][pos_x]:
            target_value: int = agents[pos_y][pos_x]
        # -------------------------- CHECKS FOR UNPERFECT

            if target_value and target_value != agent_value:
                if wall_check(array, *branch):
                    common.add(frozenset({(pos_x, pos_y), branch}))
                else:
                    common.add(frozenset({(pos_x, pos_y), branch}))
                    create_wall(
                            array, ((pos_x, pos_y), branch)
                           )
                if (pos_x, pos_y) in targets.keys():
                    targets.pop((pos_x, pos_y))

        # -------------------------- CHECKS FOR EXPLORATION
            if not target_value:
                targets.update({(pos_x, pos_y): branch})
                if not wall_check(array, *branch):
                    agents[pos_y][pos_x] = agent_value
                    tree.add((pos_x, pos_y))

    def maze_explore_and_merge(
        self,
        start_agents: set[tuple[int, int]],
        gen_tuning: Callable[
            [list[list[int]],
             set[tuple[int, int]],
             list[list[int]],
             dict[tuple[int, int], tuple[int, int]],
             set[frozenset[tuple[int, int]]]], bool
            ] = lambda *args: True

                               ) -> None:
        """ main generation function
        explore area, create a passage, and do it again """
        """ can generate perfect or not maze with the settings """

        agents: list[list[int]]
        targets: dict[tuple[int, int], tuple[int, int]]
        tree: set[tuple[int, int]]
        common: set[frozenset[tuple[int, int]]] = set()

        get_north: Callable[..., int] = MazeGenerator.fast_get_north
        get_east: Callable[..., int] = MazeGenerator.fast_get_east
        get_south: Callable[..., int] = MazeGenerator.fast_get_south
        get_west: Callable[..., int] = MazeGenerator.fast_get_west
        destroy_wall: Callable[..., None] = MazeGenerator.destroy_wall
        create_wall: Callable[..., None] = MazeGenerator.create_wall
        check_process: Callable[..., None] = self.check_process

        targets = {}
        agents = self.setup_agents(start_agents)
        tree = start_agents
        prime_list: list[list[bool]] = self.prime_list
        array: list[list[int]] = self.array

        # - ALL AREAS WHILE
        while tree:
            # - AREA EXPLORATION WHILE
            while tree:
                new_branch: tuple[int, int] = random.choice(list(tree))
                tree.remove(new_branch)
                pos_x: int
                pos_y: int
                pos_x, pos_y = new_branch

                if new_branch in targets:
                    targets.pop(new_branch)

                agent_value: int = agents[pos_y][pos_x]

                check_process(
                        get_north,
                        array,
                        pos_x,
                        pos_y - 1,
                        new_branch,

                        prime_list,
                        targets,
                        agent_value,

                        agents,
                        tree,
                        common,
                        create_wall
                        )
                check_process(
                        get_east,
                        array,
                        pos_x + 1,
                        pos_y,
                        new_branch,

                        prime_list,
                        targets,
                        agent_value,

                        agents,
                        tree,
                        common,
                        create_wall
                        )
                check_process(
                        get_south,
                        array,
                        pos_x,
                        pos_y + 1,
                        new_branch,

                        prime_list,
                        targets,
                        agent_value,

                        agents,
                        tree,
                        common,
                        create_wall
                        )
                check_process(
                        get_west,
                        array,
                        pos_x - 1,
                        pos_y,
                        new_branch,

                        prime_list,
                        targets,
                        agent_value,

                        agents,
                        tree,
                        common,
                        create_wall
                        )

            if gen_tuning(array, tree, agents, targets, common) \
                    and len(targets) > 0:
                target: tuple[int, int]
                sender: tuple[int, int]
                target, sender = random.choice(list(targets.items()))
                targets.pop(target)
                tree = {target}
                agents[target[1]][target[0]] = \
                    agents[sender[1]][sender[0]]
                destroy_wall(array, (target, sender))

        if not self.config["PERFECT"]:
            common_list: list[frozenset[tuple[int, int]]] = list(common)
            sample: frozenset[tuple[int, int]] = random.choice(common_list)
            common_list.remove(sample)
            tar: tuple[int, int]
            src: tuple[int, int]
            tar, src = sample
            destroy_wall(array, (tar, src))

            sample = random.choice(common_list)
            tar, src = sample
            destroy_wall(array, (tar, src))

        return

    def draw_x(self, shift_x: int = 0, shift_y: int = 0) -> None:
        """ draw a horizontal line """
        if self.pos_x + shift_x < 0 or self.pos_y + shift_y < 0:
            return

        try:
            if self.get_north(
                    shift_x, shift_y + 1) != bin(1) and self.get_south(
                shift_x, shift_y
            ) != bin(1):
                self.array[
                        self.pos_y + shift_y][
                                self.pos_x + shift_x] += 0b0100
                self.array[
                        self.pos_y + shift_y + 1][
                                self.pos_x + shift_x] += 0b001
        except Exception:
            return

    def draw_y(self, shift_x: int = 0, shift_y: int = 0) -> None:
        """ draw a vertical line """
        if self.pos_x + shift_x < 0 or self.pos_y + shift_y < 0:
            return

        try:
            if self.get_east(shift_x, shift_y) != bin(1) and self.get_west(
                shift_x + 1, shift_y
            ) != bin(1):
                self.array[self.pos_y + shift_y][
                        self.pos_x + shift_x] += 0b0010
                self.array[self.pos_y + shift_y][
                        self.pos_x + 1 + shift_x] += 0b1000
        except Exception:
            return

    def get_circle_len(
        self, size_x: int = 0, size_y: int = 0, stairs: int = 0
    ) -> dict[str, int]:
        """ get circle len for drawing calculation """

        len_x: int = ((stairs - 2) * 2) + size_x
        len_y: int = ((stairs - 2) * 2) + size_y

        return {"x": len_x, "y": len_y}

    def draw_circle(
        self, size_x: int = 0, size_y: int = 0, stairs: int = 0
    ) -> bool:
        """ draw one circle with ajustable parameters """

        lenth: dict[str, int] = self.get_circle_len(size_x, size_y, stairs)
        self.pos_x -= int(lenth["x"] / 2) + 3
        self.pos_y -= int(lenth["y"] / 2) + 3
        self.pos_x += stairs + 1
        if self.pos_x <= -10 and self.pos_y <= -10:
            return False

        i: int
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
        """ draw the maximum circles in the maze area """

        start_x: int = int(self.config["WIDTH"] / 2)
        start_y: int = int(self.config["HEIGHT"] / 2)

        self.pos_x = start_x
        self.pos_y = start_y
        self.draw_circle(2, 4, 3)
        jump_x: int = 1
        jump_y: int = 1
        jump_stairs: int = 1
        c_x: int = 4
        c_y: int = 6
        c_stairs: int = 3
        check: bool = True
        if self.config["WIDTH"] < 11 or self.config["HEIGHT"] < 9:
            self.pos_x = start_x
            self.pos_y = start_y
            check = self.draw_circle(2, 1, 1)
            self.pos_x = start_x
            self.pos_y = start_y
            check = self.draw_circle(2, 2, 2)
        while check:
            self.pos_x = start_x
            self.pos_y = start_y
            check = self.draw_circle(c_x, c_y, c_stairs)
            c_stairs += jump_stairs
            c_x += jump_x
            c_y += jump_y

    def generate_cells(self) -> None:
        """ create a full wall maze area """

        self.pos_x = 0
        self.pos_y = 0

        elem: list[int]
        for elem in self.array:
            i: int = 0
            while i < len(elem):
                elem[i] = 0b1111
                i += 1

    def generate_squares(self) -> None:
        """ create larger squares than generate_cells funcion """

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

    def draw_cross(self) -> None:
        """ draw two centered cross in the maze area,
        one is horizontal/vertical
        the second is rotated to 45° from the first one """

        self.pos_x = 0
        self.pos_y = 0

        i: int = 0
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
        self.pos_x = int(self.config["WIDTH"] / 2)
        self.pos_y = int(self.config["HEIGHT"] / 2)
        while i < self.config["HEIGHT"] / 2 + 1:
            self.draw_y(-1)
            self.draw_x()
            self.draw_y(i * -2)
            self.draw_x(i * -2)
            self.pos_x += 1
            self.pos_y += 1
            i += 1
        i = 0
        self.pos_x = int(self.config["WIDTH"] / 2)
        self.pos_y = int(self.config["HEIGHT"] / 2)
        while i < self.config["HEIGHT"] / 2 + 1:
            self.draw_y(-1)
            self.draw_x()
            self.draw_y(i * 2)
            self.draw_x(i * 2)
            self.pos_x -= 1
            self.pos_y -= 1
            i += 1

    def draw_cube(self) -> None:
        """ draw a cube on the maze area in the current location """
        self.prime_list[self.pos_y][self.pos_x] = False
        self.draw_x()
        self.draw_x(0, -1)
        self.draw_y()
        self.draw_y(-1, 0)

    def set_42_walls(self) -> None:
        """ set the 42 sympol at the center of the screen """

        positions: list[tuple[int, int]]
        positions = get_42_pos(self.config["WIDTH"], self.config["HEIGHT"])

        for self.pos_x, self.pos_y in positions:
            self.draw_cube()

    def generate(self, indicator: str) -> None:
        """ generate the maze dependingly of the key-str used """

        if self.config["WIDTH"] == 1 or self.config["HEIGHT"] == 1:
            self.config["PERFECT"] = True
            indicator = "Line"

        match indicator:
            case "Circle":
                self.generate_circles()
                self.draw_cross()
            case "Classic":
                self.generate_cells()
            case "Square":
                self.generate_squares()
            case "Line":
                return
            case _:
                raise self.MazeGenerateError("unknow maze type")
        self.set_42_walls()

        start: set[tuple[int, int]]
        if self.config["PERFECT"]:
            possibles: list[tuple[int, int]] = [
                    (x, y) for y in range(self.config["HEIGHT"])
                    for x in range(self.config["WIDTH"])
                    if self.prime_list[y][x]]
            start = {random.choice(possibles)}
        else:
            entry_x: int
            entry_y: int
            entry_x, entry_y = self.config["ENTRY"]
            start = {self.config["ENTRY"]}
            exit_x: int
            exit_y: int
            exit_x, exit_y = self.config["EXIT"]
            start.update({self.config["EXIT"]})
        self.maze_explore_and_merge(start)
