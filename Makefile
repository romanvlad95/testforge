PYTHON = $(CURDIR)/.venv/bin/python3
PIP = $(PYTHON) -m pip
POETRY = poetry

.PHONY: all build install clean test lint

all: install test lint

build:
	$(PYTHON) -m build

install:
	$(PIP) install -e .[dev]

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f .coverage
	rm -rf htmlcov/

test:
	$(PIP) install -e .[dev]
	PYTHONUNBUFFERED=1 PYTHONPATH=./src $(PYTHON) -m pytest

lint:
	$(PIP) install -e .[dev]
	$(PYTHON) -m ruff check .
	$(PYTHON) -m black --check .
	PYTHONPATH=./src $(PYTHON) -m mypy src/
