# A-Maze-ing

## Table of Contents

- [Description](#description)
- [Instructions](#instructions)
- [Configuration](#configuration)
- [Algorithm](#algorithm)
- [Reusable Components](#reusable-components)
- [Bonus](#bonus)
- [Team](#team)
- [Resources](#resources)

---

## Description

This project, created as part of the 42 curriculum by **abenabde** and **larchimb**, generates different types of mazes, either perfect or imperfect. Once generated, the maze is solved using a "Distract"-type algorithm and displayed using the **MLX** library.

The program:
- Parses settings from a `config.txt` file.
- Generates the maze in three possible shapes: single-cell, square, or circular.
- Outputs the maze, entry point, exit point, and shortest path to `maze.txt`.
- Visualizes the maze and solution using the MLX library.

The project is designed to be packaged as a `.whl` file for later use.

---

## Instructions

### Available Commands

| Command            | Description                                  |
|--------------------|----------------------------------------------|
| `make install`     | Install dependencies from `requirements.txt` |
| `make build`       | Build the `mazegen` pip package              |
| `make run`         | Generate and display the maze                |
| `make debug`       | Run with Python debugger (pdb)               |
| `make lint`        | Run `flake8` and `mypy`                      |
| `make lint-strict` | Run `flake8` and `mypy` in strict mode       |
| `make clean`       | Remove temporary files and caches            |

Recommended workflow:

```bash
make install
make run
````

To build the wheel (after installation):

```bash
make build
```

---

## Configuration

The configuration file uses a simple `KEY=VALUE` format. Lines starting with `#` are comments. The default configuration file is `config.txt`.

### Maze Settings

| Key                    | Type            | Description                        | Example                      |
| ---------------------- | --------------- | ---------------------------------- | ---------------------------- |
| `WIDTH`                | `int`           | Number of columns                  | `WIDTH=20`                   |
| `HEIGHT`               | `int`           | Number of rows                     | `HEIGHT=15`                  |
| `ENTRY`                | `x,y`           | Entry cell coordinates             | `ENTRY=0,0`                  |
| `EXIT`                 | `x,y`           | Exit cell coordinates              | `EXIT=19,14`                 |
| `OUTPUT_FILE`          | `string`        | File name for output               | `OUTPUT_FILE=maze.txt`       |
| `OUTPUT_FILE_OVERRIDE` | `bool`          | Allow overwriting existing files   | `OUTPUT_FILE_OVERRIDE=False` |
| `PERFECT`              | `bool`          | Generate a perfect maze (no loops) | `PERFECT=True`               |
| `SEED`                 | `int` or `None` | Random seed for reproducibility    | `SEED=42`                    |

### Example Configuration

```ini
# Maze dimensions
WIDTH=100
HEIGHT=100
ENTRY=1,1
EXIT=99,99
OUTPUT_FILE=maze.txt
OUTPUT_FILE_OVERRIDE=True
PERFECT=False
SHAPE=Random
SEED=Random
```

---

## Algorithm

### Maze Generation — Iterative Backtracker (DFS)

The maze is generated using an iterative depth-first search (DFS) with backtracking using an explicit stack.

### Maze Solving — BFS (Breadth-First Search)

The shortest path between the entry and exit points is found using breadth-first search (BFS).

---

## Reusable Components

All reusable elements are located in the `mazegen` folder, including the parsing and maze generation modules.

### Architecture

The package exposes two main classes.

### Building from Source

Run the following command to create the wheel:

```bash
make build
```

### Installation

To reuse the files, install the wheel with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic Usage

Example Python script to generate a maze and its solution:

```python
import sys
import traceback
from example import MazeInit, MazeConfigError
from example import MazeGenerator
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

## Team

### Roles

| Member       | Responsibilities              |
| ------------ | ----------------------------- |
| **abenabde** | MazeInit, MazeGenerator       |
| **larchimb** | DisplayMaze, Wheel generation |

### Planning

Initially, Amin worked on imperfect mazes and Luc on perfect mazes. Amin later rewrote the perfect maze algorithm, while Luc handled the MLX visualization. Work was split for the Makefile: Amin handled generation, Luc built the wheel.

### What Could Be Improved

* **Structural issue:** Two maze generators were implemented, but only one is used.
* **Repo management:** Development started on a single branch before moving to multiple branches.

### Successes

* **Collaborative work:** Programs were integrated without conflicts.
* **Communication:** Continuous collaboration throughout the project.

### Tools Used

| Tool          | Usage                  |
| ------------- | ---------------------- |
| **flake8**    | Code style enforcement |
| **mypy**      | Static type checking   |
| **pip/build** | Python packaging       |

---

## Resources

* [Maze Algorithms](https://info.blaisepascal.fr/nsi-labyrinthes/)
* [Maze Modeling](https://fr.wikipedia.org/wiki/Mod%C3%A9lisation_math%C3%A9matique_d%27un_labyrinthe)
* Claude and ChatGPT: for clarifying certain concepts

