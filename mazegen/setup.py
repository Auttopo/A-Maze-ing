from setuptools import setup, find_packages
# pip install setuptools 
# pyt setup.py bdist_wheel

setup(
        name="mazegen",
        version="1.0",
        author="larchimb, abenabde",
        packages = find_packages(),
        description="""

        The mazegen package contain the main class MazeGenerator.
        No real verifications on argument is done,
        for thie use the MazeInit class.

        MazeGeneraor
        The genrator need a dictionnary as unic paramater
        that contain the following keys:
            
            Core to init and generation:
            WIDTH: int
            HEIGHT: int
            PERFECT: bool
            SHAPE: str = "Classic" or "Square" or "Circle"

            Core to resolve and Optional for create file:
            ENTRY: tuple[int, int]
            EXIT: tuple[int, int]

            Core to create file:
            OUTPUT_FILE: str

            Optional for generation:
            SEED: int | str = integer or "Random"

        When an object of maze generator is inisialised.
        A maze is generate, following rules of the choosen options.
        'maze = MazeGenerator(dict[str, Any])'

        After this you can access the array of the maze with:
        maze.get_array() ; this method return the maze array.
        'array = maze.get_maze()'

        The array is of the following format : list[list[int]]
        , and cells can be access with : array[y][x]
        All cells are int of bits of the following representation:
        0 is the less significant bit
            Bit Direction
            0   North
            1   East
            2   South
            3   West
        1 signifie a wall presence
        0 signifie no wall presence

        After the inisialisation you can resolve the maze with:
        maze.resolve()
        this method return the directions to take from the entry,
        to get to the exit, in one string, using: North/East/South/West first letter.
        exemple : "NSSENWWNE" 

        If needed you can change data setings beetwin two calls with:
        maze.update_config(new_data: dict[str, Any])

        For more you can create a file of the maze, containing the exit path if generated with:
        maze.create_file()

        The output file is of the following format:

        Representation of the maze with hexadecimals values,
        entry position (Optional),
        exit postion (Optional),
        path to exit (Optional).

        Exemple output file:

            BD51555179557D55553B
            A938393810393911392A
            C0686C446C446C6C406A
            B8383939391111393812
            C0686C2C446C2C6C442E
            9010390139112939392B
            A86C686C6C6C2C44006A
            A8393839391101392812
            EC046C2C446C2C686C6E
            B92939053D3D4538113B
            C404686FAFAFFFC42C46
            B929103FEF857FB90113
            AC2C6C2FFFAFFFC06C6E
            A90139293FAFD5383913
            AC2C44446FAFFFC4286E
            8129111139013911283B
            AC6C68686C2C6C2C4442
            A939383839291129393A
            80446C6C04406C68446E
            A8393939291011383913
            EC4440406C6C2C6C046E
            9111383839390111013B
            E86C446844686C6C2C6A
            B839393839383939293A
            C46C4444446C446C4446

            8,18
            18,17
            EEESESSEEEENNWNEEEN%

        Finnaly a helper class can verify informations of a file, and parse it
        to get data ready for MazeGenerator.
        'data_dict = MazeInit("setting_file_name")'

        to access the dictionary call your object created
        'data_dict()'

        The file content is of the following format:
            
            Mandatory:
            WIDTH=int
            HEIGHT=int
            ENTRY=int,int or Random
            EXIT=int,int or Random
            OUTPUT_FILE=maze.txt
            PERFECT=bool or Random
            SEED=int or Random

            Optional:
            OUTPUT_FILE_OVERRIDE=bool
            SHAPE=Classic or Square or Circe or Random

        def tuning_exemple(obj: MazeGenerator) -> Callable[..., bool]:
            pairs: set[int] = set()
            save_agents: list[list[int]] = []
            save_targets: dict[tuple[int, int], tuple[int, int]] = dict()
            debug = 0

            def keep_data(
                tree: set[tuple[int, int]],
                agents: list[list[int]],
                targets: dict[tuple[int, int], tuple[int, int]],
                common: set[frozenset[tuple[int, int]]] = set()
                    ) -> bool:
                nonlocal save_agents
                nonlocal save_targets
                save_targets = targets
                save_agents = agents
                return False

            def random_dfs(
                tree: set[tuple[int, int]],
                agents: list[list[int]],
                targets: dict[tuple[int, int], tuple[int, int]],
                common: set[frozenset[tuple[int, int]]] = set()
                    ) -> bool:

                target, sender = random.sample(
                                    list(targets.items()), 1)[0]
                targets.pop(target)
                agents[target[1]][target[0]] = \
                    agents[sender[1]][sender[0]]
                MazeGenerator.destroy_wall(obj.array, (target, sender))

                obj.maze_explore_and_merge({target}, keep_data)
                targets.clear()
                targets.update(save_targets)
                agents.clear()
                agents.extend(save_agents.copy())

                possibles: list[tuple[int, int]] = [
                        (x, y) for y in range(obj.config["HEIGHT"])
                        for x in range(obj.config["WIDTH"])
                        if (x, y) not in obj.prime_list and agents[y][x] == 0]
                if possibles:
                    start = random.choice(possibles)
                    agents[start[1]][start[0]] = 1
                    tree.update({start})

                return False
            return random_dfs

        """,
    )
