default: help

init: ## Install pipenv
	#this fix a temporary bug (09/10/2018) with pip 18.1
	#https://github.com/pypa/pipenv/issues/2924
	pip install pip==18.0
	pip install pipenv
.PHONY: init

install: init ## Install dependencies
	pipenv install --dev --skip-lock
.PHONY: install

install-dev: init ## Install dependencies for development
	pipenv install --dev
.PHONY: install-dev

test: ## Run tests
	pipenv run py.test tests
.PHONY: test

test-coverage: ## Run tests with coverage
	pipenv run py.test --cov-config .coveragerc --cov=autoclasswrapper --cov-report term-missing
.PHONY: test-coverage

lint: ## Lint code
	pipenv run pycodestyle autoclasswrapper \
	&& pipenv run pydocstyle autoclasswrapper \
	&& pipenv run pylint autoclasswrapper
.PHONY: lint

compile: ## Compile for PyPI
	#pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel
.PHONY: compile

upload-to-pypi: ## Upload to PyPI
	pipenv run twine upload dist/*
	# clean compiled
	rm -f dist/*.tar.gz dist/*.whl dist/*.egg
.PHONY: upload-to-pypi

install-autoclass: init ## Install AutoClass C
	# https://ti.arc.nasa.gov/tech/rse/synthesis-projects-applications/autoclass/autoclass-c/
	wget https://ti.arc.nasa.gov/m/project/autoclass/autoclass-c-3-3-6.tar.gz
	tar zxvf autoclass-c-3-3-6.tar.gz
	rm -f autoclass-c-3-3-6.tar.gz
.PHONY: install-autoclass

doc: doc/source ## Build documentation
	cd doc && pipenv run make html
.PHONY: doc

clean-demo: ## Clean demo files
	rm -f demo/autoclass*
	rm -f demo/nohup.out
	rm -f demo/*.tsv
.PHONY: clean-demo

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
