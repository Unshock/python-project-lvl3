#Makefile

install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

package-uninstall:
	python3 -m pip uninstall hexlet-code

package-reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

test:
	poetry run pytest

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests