MLXDIR = src/mlx_CLXV

.PHONY: install run debug clean lint lint-strict package

install:
	pip install --upgrade pip
	pip install flake8 mypy build
	@ls mazegen-1.0.0-py3-none-any.whl > /dev/null 2>&1 || (python3 -m build && cp dist/mazegen-1.0.0-py3-none-any.whl .)
	pip install mazegen-1.0.0-py3-none-any.whl
	$(MAKE) -C $(MLXDIR)
	pip install $(MLXDIR)/mlx-2.2-py3-none-any.whl

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	$(MAKE) -C $(MLXDIR) clean
	rm -rf dist mazegen-1.0.0-py3-none-any.whl .mypy_cache src/mazegen.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

package:
	python3 -m build
