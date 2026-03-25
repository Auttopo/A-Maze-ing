
from datetime import datetime
import random
from typing import Any
import functools
from os.path import exists
import math

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
            
            if config["SEED"] != "Random":
                random.seed(config["SEED"])
                print(config["SEED"])
            else:
                seed = random.randint(0, 10**4000)
                random.seed(seed)
                print(seed)

            for i in range(config["HEIGHT"]):
                self.prime_list[i][-1] = False

                self.array.append([0b0] * (config["WIDTH"]))
                self.array[i][0] += 0b1000
                self.array[i][config["WIDTH"] - 1] += 0b0010

            for i in range(config["WIDTH"]):
                self.prime_list[-1][i] = False

                self.array[0][i] += 0b0001
                self.array[config["HEIGHT"] - 1][i] += 0b0100
       

            self.generate("UNPERFECT")
         #   self.generate("CIRCLE")

            self.show()

            road: str = ""
            try:
                road = self.resolve()
            except Exception as e:
                print(e)
            print("time exec", self.tt.total_seconds())
            self.show_pretty()
            if road:
                print("SUCCESS !:")
                print(road)
        # self.create_file()

        def create_file(self) -> None:
                
            with open(self.config["OUTPUT_FILE"], "w") as file:
                file.write(self.create_string())



        def create_string(self) -> str:
            out: str = ""
            for elem in self.array:
                for num in elem:
                    out += str("{0:x}".format(num)).capitalize()
                out+= "\n"
            return out



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
                
        def draw_cube(self) -> None:
            self.prime_list[self.pos_y][self.pos_x] = False
            self.draw_x()
            self.draw_x(0, -1)
            self.draw_y()
            self.draw_y(-1, 0)

        def set_42_walls(self) -> None:
            # set: up left point
            self.pos_x = int(self.config["WIDTH"] / 2) - 3
            self.pos_y = int(self.config["HEIGHT"] / 2) - 2
            for i in range(2):
                self.draw_cube()
                self.pos_y += 1
            for i in range(2):
                self.draw_cube()
                self.pos_x += 1
            for i in range(2):
                self.draw_cube()
                self.pos_y += 1
            self.draw_cube()
            self.pos_x += 2
            self.pos_y -= 4
            for i in range(2):
                self.draw_cube()
                self.pos_x += 1
            for i in range(2):
                self.draw_cube()
                self.pos_y += 1
            for i in range(2):
                self.draw_cube()
                self.pos_x -= 1
            for i in range(2):
                self.draw_cube()
                self.pos_y += 1
            for i in range(2):
                self.draw_cube()
                self.pos_x += 1
            self.draw_cube()
            

        
        def get_north(self, shift_x: int = 0, shift_y: int = 0) -> str:
            #return bin(self.array[self.pos_y + shift_y][self.pos_x + shift_x] & 1 << 0)
            return bin(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x]  % 2))

        def get_east(self, shift_x: int = 0, shift_y: int = 0) -> str:
            #return bin(self.array[self.pos_y + shift_y][self.pos_x + shift_x] & 1 << 0)
            return bin(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) % 2)

        def get_south(self, shift_x: int = 0, shift_y: int = 0) -> str:
            #return bin(self.array[self.pos_y + shift_y][self.pos_x + shift_x] & 1 << 0)
            return bin(int(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) / 2) % 2)

        def get_west(self, shift_x: int = 0, shift_y: int = 0) -> str:
            #return bin(self.array[self.pos_y + shift_y][self.pos_x + shift_x] & 1 << 0)
            return bin(int(int(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) / 2) /2) % 2)
    
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


        def destroy_wall(self, targets: tuple[tuple[int, int], tuple[int, int]]) -> None:

            target, sender = targets
            target_x, target_y = target
            sender_x, sender_y = sender
            if target_x == sender_x:
                if target_y > sender_y:
                    # target at down
                    self.array[target_y][target_x] -= 0b0001
                    self.array[sender_y][sender_x] -= 0b0100
                else:
                    # target at up
                    self.array[target_y][target_x] -= 0b0100
                    self.array[sender_y][sender_x] -= 0b0001
            else:
                if target_x > sender_x:
                    # target at right
                    self.array[target_y][target_x] -= 0b1000
                    self.array[sender_y][sender_x] -= 0b0010
                else:
                    # target at left
                    self.array[target_y][target_x] -= 0b0010
                    self.array[sender_y][sender_x] -= 0b1000


        def resolve(self) -> str:

            agents: list[list[int]] = [[0 for _ in range(self.config["WIDTH"])] for _ in range(self.config["HEIGHT"])]

            tree: list[tuple[int, int]]
            dest_x: int
            dest_y: int

            self.pos_x, self.pos_y = self.config["ENTRY"]

            tree = [(self.pos_x, self.pos_y)]
            agents[self.pos_y][self.pos_x] = 1
            temp_i = 0
            while(tree):

                self.pos_x, self.pos_y = tree.pop(0)
                new_value = agents[self.pos_y][self.pos_x] + 1

                if self.get_north() == bin(0):
                    if new_value < agents[self.pos_y - 1][self.pos_x] or agents[self.pos_y - 1][self.pos_x] == 0:
                        agents[self.pos_y - 1][self.pos_x] = new_value
                        tree.append((self.pos_x, self.pos_y - 1))

                if self.get_east() == bin(0):
                    if new_value < agents[self.pos_y][self.pos_x + 1] or agents[self.pos_y][self.pos_x + 1] == 0:
                        agents[self.pos_y][self.pos_x + 1] = new_value
                        tree.append((self.pos_x + 1, self.pos_y))

                if self.get_south() == bin(0):
                    if new_value < agents[self.pos_y + 1][self.pos_x] or agents[self.pos_y + 1][self.pos_x] == 0:
                        agents[self.pos_y + 1][self.pos_x] = new_value
                        tree.append((self.pos_x, self.pos_y + 1))

                if self.get_west() == bin(0):
                    if new_value < agents[self.pos_y][self.pos_x - 1] or agents[self.pos_y][self.pos_x - 1] == 0:
                        agents[self.pos_y][self.pos_x - 1] = new_value
                        tree.append((self.pos_x - 1, self.pos_y))
                temp_i += 1


            self.pos_x, self.pos_y = self.config["EXIT"]

            temp_i = 0
            road: list[str] = []
            value: float = agents[self.pos_y][self.pos_x]
            while(value != 1):

                value = agents[self.pos_y][self.pos_x]
                shortest: str = ""

                if self.get_north() == bin(0):
                    if value > agents[self.pos_y - 1][self.pos_x]:
                        value = agents[self.pos_y - 1][self.pos_x]
                        shortest = "N"

                if self.get_east() == bin(0):
                    if value > agents[self.pos_y][self.pos_x + 1]:
                        value = agents[self.pos_y][self.pos_x + 1]
                        shortest = "E"

                if self.get_south() == bin(0):
                    if value > agents[self.pos_y + 1][self.pos_x]:
                        value = agents[self.pos_y + 1][self.pos_x]
                        shortest = "S"

                if self.get_west() == bin(0):
                    if value > agents[self.pos_y][self.pos_x - 1]:
                        value = agents[self.pos_y][self.pos_x - 1]
                        shortest = "W"

                match shortest:
                    case "N":
                        self.pos_y -= 1
                    case "E":
                        self.pos_x += 1
                    case "S":
                        self.pos_y += 1
                    case "W":
                        self.pos_x -= 1
                    case _:
                        for elem in agents:
                            print(elem)
                            self.agents = agents
                        raise Exception(f"Impossible road occured: {''.join(road)}")

                road.append(shortest)
            for elem in agents:
                print(elem)
            return "".join(road)

            for elem in agents:
                print(elem)
            #print(shortest)

        def area_visitor(self) -> None:
           
            visited: list[list[int]] = [[False for _ in range(self.config["WIDTH"])] for _ in range(self.config["HEIGHT"])]
            targets: dict[typle[int, int]] = {}
            wait_list: set[tuple[int, int]] = {(self.pos_x, self.pos_y)}
            tree: set[tuple[int, int]]

            while(wait_list):
               
                tree = {wait_list.pop()}
                
                while(tree):

                    new_branch = random.choice(list(tree))
                    tree.remove(new_branch)
                    self.pos_x, self.pos_y = new_branch
                    visited[self.pos_y][self.pos_x] = True


                    if new_branch in targets:
                        targets.pop(new_branch)

                    if self.prime_list[self.pos_y - 1][self.pos_x] and not visited[self.pos_y - 1][ self.pos_x]:
                        targets.update({(self.pos_x, self.pos_y - 1) : new_branch}) 
                        if self.get_north() == bin(0):
                            tree.add((self.pos_x, self.pos_y - 1))

                    if self.prime_list[self.pos_y][ self.pos_x + 1] and not visited[self.pos_y][ self.pos_x + 1]:
                        targets.update({(self.pos_x + 1, self.pos_y) : new_branch})
                        if self.get_east() == bin(0):
                            tree.add((self.pos_x + 1, self.pos_y))

                    if self.prime_list[self.pos_y + 1][ self.pos_x] and not visited[self.pos_y + 1][ self.pos_x]:
                        targets.update({(self.pos_x, self.pos_y + 1) : new_branch})
                        if self.get_south() == bin(0):
                            tree.add((self.pos_x, self.pos_y + 1))

                    if self.prime_list[self.pos_y][ self.pos_x - 1] and not visited[self.pos_y][ self.pos_x - 1]:
                        targets.update({(self.pos_x - 1, self.pos_y) : new_branch})
                        if self.get_west() == bin(0):
                            tree.add((self.pos_x - 1, self.pos_y))

                wait_list = {(x, y) for x, y in wait_list if not visited[y][x]}

                if len(wait_list) < 1:

                    if len(targets) > 1:
                        sample = random.sample(list(targets.items()), 2)
                        targets.pop(sample[0][0])
                        wait_list.update({sample[0][0]})
                        self.destroy_wall(sample[0])

                        targets.pop(sample[1][0])
                        wait_list.update({sample[1][0]})
                        self.destroy_wall(sample[1])
                    elif len(targets) == 1:
                        sample = random.sample(list(targets.items()), 1)

                        targets.pop(sample[0][0])
                        wait_list.update({sample[0][0]})
                        self.destroy_wall(sample[0])
            return
        
        

        def maze_explorator(self) -> None:
            self.pos_x = int(self.config["WIDTH"] / 2) - 3 + 5
            self.pos_y = int(self.config["HEIGHT"] / 2) - 2 + 1
            
            self.area_visitor()
            
        def generate_classic(self) -> None:
            for elem in self.array:
                i = 0
                while i < len(elem):
                    elem[i] = 0b1111
                    i += 1
           
        def generate_unperfect(self) -> None:

            for self.pos_y in range(self.config["HEIGHT"]):
                self.pos_x = 0
                while self.pos_x < self.config["WIDTH"]:
                    if self.pos_x % 2 == 0:
                        self.draw_y()
                    if self.pos_y % 2 == 0:
                        self.draw_x()
                    self.pos_x += 1
                print(self.pos_y)


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
                except Exception:
                    break

        
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

        def generate(self, indicator: str) -> None:
            match indicator:
                case "CIRCLE":
                    self.generate_circles()
                    self.draw_cross()
                case "CLASSIC":
                    self.generate_classic()
                case "UNPERFECT":
                    self.generate_unperfect()

            self.set_42_walls()
            start = datetime.now()
            self.maze_explorator()
            self.tt = datetime.now() - start

            
            


