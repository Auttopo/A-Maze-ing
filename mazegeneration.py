
import random
from typing import Any
import functools

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
            self.prime_list: set[tuple[int, int]] = set()
            
            if config["SEED"] != "Random":
                random.seed(config["SEED"])
                print(config["SEED"])
            else:
                seed = random.randint(0, 10**4000)
                random.seed(seed)
                print(seed)



        
            if config["WIDTH"] < config["HEIGHT"]:
                config["HEIGHT"] += 10
                config["WIDTH"] = config["HEIGHT"] + 10
            else:
                config["WIDTH"] += 10
                config["HEIGHT"] = config["WIDTH"] + 10


            for i in range(config["HEIGHT"]):
                self.array.append([0b0] * (config["WIDTH"]))
                self.array[i][0] += 0b1000
                self.array[i][config["WIDTH"] - 1] += 0b0010
            for i in range(config["WIDTH"]):
                self.array[0][i] += 0b0001
                self.array[config["HEIGHT"] - 1][i] += 0b0100
       
            self.prime_list.update((n, -1) for n in range(self.config_width))
            self.prime_list.update((n, self.config_height) for n in range(0, self.config_width))
            self.prime_list.update((-1, n) for n in range(self.config_height))
            self.prime_list.update((self.config_width, n) for n in range(0, self.config_height))



            self.generate()
            #print(self.prime_list)
            self.show()
            self.show_pretty()



        def show(self) -> None:
            for elem in self.array:
                for num in elem:
                    print(str("{0:x}".format(num)).capitalize(), end=" ")
                print("")

        def show_pretty(self) -> None:

            for elem in self.array:
                line1 = ""
                line2 = ""
                line3 = ""
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

                    def list_in_str(data: list[str]) -> str:
                        out = ""
                        for elem in data:
                            out += elem
                        return out

                    line1 += list_in_str(s1)
                    line2 += list_in_str(s2)
                    line3 += list_in_str(s3)
                print(line1)
                print(line2)
                print(line3)
                
        def draw_cube(self) -> None:
            self.prime_list.update({(self.pos_x, self.pos_y)})
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
            

        def step(self, choice: int) -> None:
            match choice:
                case 0:
                    self.pos_y -= 1
                case 1:
                    self.pos_x += 1
                case 2:
                    self.pos_y += 1
                case 3:
                    self.pos_x -= 1
            
        
        @functools.lru_cache()
        def choices(self, possible: int) -> list[int]:
            choice = []

            for i in range(4):
                if bin(possible % 2) == bin(0):
                    choice.append(i)
                possible = int(possible / 2)

            return choice
       
        
        def init_cube(self) -> None:
            r = random.randint(0, 3)

            print(r)
            match r:
                case 0:
                    self.array[self.pos_y][self.pos_x] += 0b0010
                    self.array[self.pos_y][self.pos_x + 1] += 0b1000
                case 1:
                    self.array[self.pos_y][self.pos_x + 1] += 0b0100
                    self.array[self.pos_y + 1][self.pos_x + 1] += 0b0001
                case 2:
                    self.array[self.pos_y + 1][self.pos_x] += 0b0010
                    self.array[self.pos_y + 1][self.pos_x + 1] += 0b1000
                case 3:
                    self.array[self.pos_y][self.pos_x] += 0b0100
                    self.array[self.pos_y + 1][self.pos_x] += 0b0001

        def get_north(self, shift_x: int = 0, shift_y: int = 0) -> str:
            return bin(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x]  % 2))

        def get_east(self, shift_x: int = 0, shift_y: int = 0) -> str:
            return bin(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) % 2)

        def get_south(self, shift_x: int = 0, shift_y: int = 0) -> str:
            return bin(int(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) / 2) % 2)

        def get_west(self, shift_x: int = 0, shift_y: int = 0) -> str:
            return bin(int(int(int(self.array[self.pos_y + shift_y][self.pos_x + shift_x] / 2) / 2) /2) % 2)
    
        def draw_x(self, shift_x:int = 0, shift_y: int = 0) -> None:
            if self.pos_x < 0 or self.pos_y < 0:
                return

            try:
                if  self.get_north(shift_x, shift_y + 1) != bin(1):

                    self.array[self.pos_y + shift_y ][self.pos_x + shift_x] += 0b0100
                    self.array[self.pos_y + shift_y + 1][self.pos_x + shift_x] += 0b001
            except Exception:
                return

        def draw_y(self, shift_x: int = 0, shift_y: int = 0) -> None:
            if self.pos_x < 0 or self.pos_y < 0:
                return

            try:
                if  self.get_east(shift_x, shift_y) != bin(1):
                    self.array[self.pos_y + shift_y][self.pos_x + shift_x] += 0b0010
                    self.array[self.pos_y + shift_y][self.pos_x + 1 + shift_x] += 0b1000  
            except Exception:
                return



        def get_circle_len(self, size_x:int = 0, size_y: int = 0, stairs:int = 0) -> dict[str, int]:

            len_x: int = ((stairs - 2) * 2) + size_x + 0
            len_y: int = ((stairs - 2) * 2) + size_y + 0

            return {"x": len_x, "y": len_y}
            

        def draw_circle(self, size_x:int = 0, size_y: int = 0, stairs: int = 0) -> bool:
           
            lenth = self.get_circle_len(size_x, size_y, stairs)
            print(lenth)
            if lenth["x"] > self.config["HEIGHT"] + 10 or lenth["y"] > self.config["WIDTH"] + 10:
                return False

            self.pos_x -= int(lenth["x"] / 2) + 4
            self.pos_y -= int(lenth["y"] / 2) + 3
            self.pos_x += stairs + 1

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

        def copy_maze(self) -> None:

            base_array = self.array
            self.array = []
            self.config["HEIGHT"] = self.config_height
            self.config["WIDTH"] = self.config_width
            for i in range(self.config["HEIGHT"]):
                self.array.append([0b0] * (self.config["WIDTH"]))
            e = 0
            start_e =  int(len(base_array) / 2 - len(self.array) / 2)
            start_i =  int(len(base_array[0]) / 2 - len(self.array[0]) / 2)
            while e < len(self.array):
                i = 0
                while i < len(self.array[e]):
                    self.array[e][i] = base_array[start_e + e][start_i + i]
                    i += 1
                e += 1
            self.pos_x = 0
            self.pos_y = 0
            for i in range(self.config["HEIGHT"]):
                if self.get_west(0, i) != bin(1):
                    self.array[i][0] += 0b1000
                if self.get_east(self.config["WIDTH"] - 1, i) != bin(1):
                    self.array[i][self.config["WIDTH"] - 1] += 0b0010
            for i in range(self.config["WIDTH"]):

                if self.get_north(i, 0) != bin(1):
                    self.array[0][i] += 0b0001
                if self.get_south(i, self.config["HEIGHT"] - 1) != bin(1):
                    self.array[self.config["HEIGHT"] - 1][i] += 0b0100
            self.set_42_walls()


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

        def area_visitor(self) -> None:
           
            visited: list[tuple[int, int]] = []
            targets: list[tuple[int, int]]
            neighbor: dict[typle[int, int]]
            tree: set[tuple[int, int]] = {(self.pos_x, self.pos_y)}
            
            air = (self.config_width + 1) * (self.config_height + 1)

            neighbor = {}
            while(1):
                
                targets = []
                while(tree):
                    new_branch = random.choice(list(tree))
                    self.pos_x, self.pos_y = new_branch
                    
                    for e1 in neighbor.keys():
                        if e1 == new_branch:
                            neighbor.pop(e1)
                            break

                    visited.append((self.pos_x, self.pos_y))
                    if self.get_north() == bin(0) and (self.pos_x, self.pos_y - 1) not in visited and (self.pos_x, self.pos_y - 1) not in self.prime_list:
                        tree.update({(self.pos_x, self.pos_y - 1)})
                    if self.get_east() == bin(0) and (self.pos_x + 1, self.pos_y) not in visited and (self.pos_x + 1, self.pos_y) not in self.prime_list:
                        tree.update({(self.pos_x + 1, self.pos_y)})
                    if self.get_south() == bin(0) and (self.pos_x, self.pos_y + 1) not in visited and (self.pos_x, self.pos_y + 1) not in self.prime_list:
                        tree.update({(self.pos_x, self.pos_y + 1)})
                    if self.get_west() == bin(0) and (self.pos_x - 1, self.pos_y) not in visited and (self.pos_x - 1, self.pos_y) not in self.prime_list:
                        tree.update({(self.pos_x - 1, self.pos_y)})

                    neighbor.update({(self.pos_x, self.pos_y - 1) : new_branch}) 
                    neighbor.update({(self.pos_x + 1, self.pos_y) : new_branch})
                    neighbor.update({(self.pos_x, self.pos_y + 1) : new_branch})
                    neighbor.update({(self.pos_x - 1, self.pos_y) : new_branch})

                    tree.remove(new_branch)
                print("WORINPROGRESS -----------------------") 
                for elem in neighbor.items():
                    if elem[0] not in visited and elem[0] not in self.prime_list:
                        targets.append(elem)

                
                if len(targets) == 0:
                    #for x, y in visited:
                    #    if bin(int(int(int(int(self.array[y][x] / 2) / 2) / 2) / 2) % 2) != bin(1):
                    #        self.array[y][x] += 0b10000
                    print(len(visited), air)
                    print("NO TERGET RETURN")
                    return
                target1 = random.choice(targets)
                targets.remove(target1)
                target2 = random.choice(targets)
                    

               # if bin(int(int(int(int(self.array[target[0][1]][target[0][0]] / 2) / 2) / 2) / 2) % 2) != bin(1):
               #     self.array[target[0][1]][target[0][0]] += 0b10000
               # print("t", target)
               # print(target[0][1], target[0][0])
                #if target1[0] != (0, 17):
                #    self.destroy_wall(target1)
                self.destroy_wall(target1)
                self.destroy_wall(target2)
                neighbor.pop(target2[0])
                tree = {target1[0]}
                print(target1[0])
                print("TARGETS", target1, target2)


            #for x, y in visited:
            #    if bin(int(int(int(int(self.array[y][x] / 2) / 2) / 2) / 2) % 2) != bin(1):
            #        self.array[y][x] += 0b10000


        
            print(len(visited), air)
        
            print("AIR COMPLETE RETURN")
            return
        
        

        def maze_explorator(self) -> None:
            self.pos_x = int(self.config["WIDTH"] / 2) - 3 + 5
            self.pos_y = int(self.config["HEIGHT"] / 2) - 2 + 1
            
            self.area_visitor()
            
            

        def generate(self) -> None:

            start_x: int = int(self.config["WIDTH"] / 2)
            start_y: int = int(self.config["HEIGHT"] / 2)
   
            self.pos_x = start_x
            self.pos_y = start_y
            check = self.draw_circle(2, 4, 3)
            c_x = 4
            c_y = 6
            c_stairs = 3
            check = True
            while (check):
                try:
                    self.pos_x = start_x
                    self.pos_y = start_y
                    check = self.draw_circle(c_x, c_y, c_stairs)
                    c_stairs += 1
                    c_x += 2
                    c_y += 2
                except Exception:
                    break

            ratio = self.config["WIDTH"] / self.config["HEIGHT"]
            print(ratio)
            
            self.copy_maze()
            self.maze_explorator()


            
            


