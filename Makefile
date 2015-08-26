.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - make a new release, upload it to PyPI and push to Git"
	@echo "devrelease - upload a development release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "bumpminor - increment the minor version number of the next release"
	@echo "bumpmajor - increment the major version number of the next release"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 configloader tests

test:
	py.test

test-all:
	tox --skip-missing-interpreters

coverage:
	py.test --cov configloader

docs:
	sphinx-build -b html docs docs/_build

release: clean test-all
	bumpversion release
	python setup.py bdist_wheel upload
	python setup.py sdist upload
	bumpversion --no-tag patch
	git push
	git push --tags

devrelease: clean test-all
	python setup.py bdist_wheel upload
	python setup.py sdist upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install

bumpminor:
	bumpversion --no-tag minor

bumpmajor:
	bumpversion --no-tag major
