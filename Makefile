FILE=config.txt

install:
	python3 -m venv maze_env && \
	. maze_env/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt && \
	pip install mlx-2.2-py3-none-any.whl

run:
	. maze_env/bin/activate && \
	python3 -m a_maze_ing $(FILE)

debug:
	. maze_env/bin/activate && \
	python3 -m pdb a_maze_ing $(FILE)

clean:
	$(RM) -r __pycache__

lint:
	. maze_env/bin/activate && \
	python3 -m flake8 --exclude maze_env,mlx_files; \
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	. maze_env/bin/activate && \
	python3 -m flake8 --exclude maze_env,mlx_files; \
	python3 -m mypy . --strict
