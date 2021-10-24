.PHONY: format isort black test

format: isort black

isort:
	python -m isort ableef/ tests/

black:
	python -m black ableef/ tests/

test:
	python -m pytest -v tests/
