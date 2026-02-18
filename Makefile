MLXDIR = src/mlx_CLXV

.PHONY: install run debug clean lint lint-strict package

setting:
	cd /tmp
	apt download libxcb-keysyms1-dev libxcb-keysyms1 
	mkdir -p extracted_libs 
	dpkg -x libxcb-keysyms1-dev_*.deb ./extracted_libs && dpkg -x libxcb-keysyms1_*.deb ./extracted_libs && \
	cp -r ./extracted_libs/usr/include/* $$VIRTUAL_ENV/include/ && cp -P ./extracted_libs/usr/lib/x86_64-linux-gnu/libxcb-keysyms* $$VIRTUAL_ENV/lib/
	export C_INCLUDE_PATH="$$VIRTUAL_ENV/include:$$C_INCLUDE_PATH" && export LIBRARY_PATH="$$VIRTUAL_ENV/lib:$$LIBRARY_PATH" && export LD_LIBRARY_PATH="$$VIRTUAL_ENV/lib:$$LD_LIBRARY_PATH" && export PKG_CONFIG_PATH="$$VIRTUAL_ENV/lib/pkgconfig:$$PKG_CONFIG_PATH"

	cd src/mlx_CLXV
	./configure.sh CFLAGS="-I$$VIRTUAL_ENV/include" LDFLAGS="-L$$VIRTUAL_ENV/lib -Wl,-rpath,$$VIRTUAL_ENV/lib"

install:
	pip install --upgrade pip
	pip install flake8 mypy build
	@ls mazegen-1.0.0-py3-none-any.whl > /dev/null 2>&1 || (python3 -m build && cp dist/mazegen-1.0.0-py3-none-any.whl .)
	pip install --force-reinstall mazegen-1.0.0-py3-none-any.whl
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
	cp dist/mazegen-1.0.0-py3-none-any.whl .
	pip install --force-reinstall mazegen-1.0.0-py3-none-any.whl
