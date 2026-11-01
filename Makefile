.PHONY: install run build lint package-install

install:
	uv sync

run:
	uv run database

build:
	uv build

lint:
	uv run ruff check .

package-install:
	uv tool install dist/*.whl