# mazegen

A Python package of the wheel format for generating, solving, and exporting mazes with configurable shapes, sizes, and generation algorithms.

disponible modules importation:
`from mazegen import MazeGenerator`
`from mazegen import MazeInit`

---

## Table of Contents

- [MazeGenerator](#mazegenerator)
  - [Initialization](#initialization)
    - [Configuration Parameters for MazeGenerator](#configuration-parameters)
    - [MazeInit](#configuration-parameters)
  - [Maze Array Format](#maze-array-format)
  - [Output File Format](#output-file-format)
  - [Settings File Format](#settings-file-format)
- [Algorithm](#algorithm)

---

## MazeGenerator

### Initialization

> **Note:** No argument validation is performed by `MazeGenerator` directly. Use the `MazeInit` class for validated input.

### Configuration Parameters for MazeGenerator

The generator takes a dictionary as its parameter, containing the following keys:
`def __init__(self, config: dict[str, Any], *, no_gen: bool = False) -> None:`

#### Required — Core (init & generation)

| Key | Type | Description |
|---|---|---|
| `WIDTH` | `int` | Width of the maze |
| `HEIGHT` | `int` | Height of the maze |
| `PERFECT` | `bool` | Whether to generate a perfect maze |
| `SHAPE` | `str` | Shape of the maze: `"Classic"`, `"Square"`, or `"Circle"` |
| `ENTRY` | `tuple[int, int]` | Entry point coordinates |
| `EXIT` | `tuple[int, int]` | Exit point coordinates |
| `OUTPUT_FILE` | `str` | Path to the output file |

#### Optional — Generation

| Key | Type | Description |
|---|---|---|
| `SEED` | `int \| str` | Random seed; use an integer or `"Random"` |

---

### MazeInit

To parse datas use Mazinit(config.txt). The config.txt must be parse in this way :

#### Mandatory Fields

```
WIDTH=int
HEIGHT=int
ENTRY=int,int or Random
EXIT=int,int or Random
OUTPUT_FILE=maze.txt
PERFECT=bool or Random
SEED=int or Random
```

#### Optional Fields

```
OUTPUT_FILE_OVERRIDE=bool
SHAPE=Classic or Square or Circle or Random
```


When a `MazeGenerator` object is instantiated, a maze is generated immediately according to the chosen options.

example with MazeInit :

```python
import sys
import traceback
from mazegen import MazeInit, MazeConfigError
from mazegen import MazeGenerator
from typing import Any

def main() -> None:
    try:
        if len(sys.argv) < 2:
            raise MazeConfigError("Provide a configuration file as the first argument")
        init: dict[str, Any] = MazeInit(sys.argv[1])()
        maze = MazeGenerator(init)
        maze.resolve()
        maze.create_file()
    except Exception as e:
        print("An error occurred:", e, file=sys.stderr)
        if len(sys.argv) > 2 and sys.argv[2] == "traceback":
            traceback.print_exc()

if __name__ == "__main__":
    main()
```

---

### Maze Array Format

The array returned by `get_maze()` is of type `list[list[int]]`. Cells are accessed with `array[y][x]`.

Each cell is an integer where each bit represents the presence of a wall on one side:

| Bit | Direction | Value |
|---|---|---|
| 0 | North | LSB |
| 1 | East | |
| 2 | South | |
| 3 | West | MSB |

- `1` = wall present
- `0` = no wall

---

### Output File Format

The output file contains:

1. A hexadecimal representation of the maze
2. Entry position *(optional)*
3. Exit position *(optional)*
4. Path to exit *(optional)*

#### Example Output File

```
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
```

---

## Algorithm


This function is the core of the algorythme. Inside it the DFS method is used by default.
Takes a set of starting points as `(x, y)` tuples, and an optional tuning function described [below](#generation-tuning).

**How it works:**

Starting points are each assigned a unique identity (agent ID). The algorithm then expands each agent's identity by exploring the surrounding area. Once all agents have finished exploring their areas, a random wall is selected from the `targets` dictionary — which tracks all unvisited neighboring cells across all areas — and destroyed. The newly accessible cell becomes the start of a new exploration.

The `targets` dictionary is never reset; visited positions are removed from it. This feeds the generation until the maze is complete.

**Perfect mode:**\

 A single start point is used. Agents of different identities never meet.

**Imperfect mode:**\

 Two start points are used. All shared walls between different agents are kept in the `common` set. If no wall exists between two different agents, one is created and added to `common`. Once all cells are explored, two random walls from `common` are destroyed to ensure at least two possible paths between the entry and exit, regardless of the initial setup.

#### Example — Agent Representation During Generation

```
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 0, 4, 0, 4, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 0, 4, 0, 4, 4, 4, 0, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
[2, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3]
[2, 2, 4, 4, 1, 1, 1, 1, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3]
[2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3]
[2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3]
[2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3]
```

---
