.PHONY: clean-pyc clean-build docs clean release release-dev bump-release bump-patch bump-minor bump-major upload assert-nondirty

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
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "release:     package and upload the current version as a full release"
	@echo "release-dev: package and upload the current version as a developmental release"
	@echo "bump-major:  bump the major version number"
	@echo "bump-minor:  bump the minor version number"

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
	sphinx-build -b html docs docs/_build/html

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install

release: | test-all bump-release upload bump-patch
	git push --follow-tags

release-dev: | assert-nondirty upload
	git tag "v$(call current_version)"
	bumpversion --message "Bump development release number" dev
	git push --follow-tags

bump-major:
	$(call targetnext, major)

bump-minor:
	$(call targetnext, minor)

bump-patch:
	$(call targetnext, patch)

bump-release:
	bumpversion --tag --message "Release version {new_version}" release

upload:
	python setup.py sdist upload
	python setup.py sdist bdist_wheel upload

assert-nondirty:
	python -c "from bumpversion import Git; Git.assert_nondirty()"

current_version = `grep 'current_version\s*=' setup.cfg | cut -d "=" -f 2 | sed "s/\s//g"`
next_release = `bumpversion --dry-run --verbose $(1) 2>&1 | grep -E "New version will be" | sed -r "s/^.* '//" | sed -r "s/(\.dev[0-9]+)?'//"`
targetnext = bumpversion --message "Target version $(call next_release, $(1)) for next release" $(1)
