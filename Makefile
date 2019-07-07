default: help

init: ## Install miniconda
	wget -q https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
	bash miniconda.sh -b -p ${HOME}/miniconda
	. ${HOME}/miniconda/etc/profile.d/conda.sh \
	&& bash -c 'hash -r' \
	&& conda init \
	&& conda config --set always_yes yes --set changeps1 no \
	&& conda update -q conda \
	&& conda info -a
.PHONY: init

install: init ## Install dependencies
	conda env create -f environment.yml
.PHONY: install

install-dev: init ## Install dependencies for development
	conda env create -f environment-dev.yml
.PHONY: install-dev

test: ## Run tests
	pytest tests
.PHONY: test

test-coverage: ## Run tests with coverage
	pytest --cov-config .coveragerc --cov=autoclasswrapper --cov-report term-missing
.PHONY: test-coverage

lint: ## Lint code
	pycodestyle autoclasswrapper \
	&& pydocstyle autoclasswrapper \
	&& pylint autoclasswrapper
.PHONY: lint

compile: ## Compile for PyPI
	python setup.py bdist_wheel
.PHONY: compile

upload-to-pypi: ## Upload to PyPI
	twine upload dist/*
	# clean compiled
	rm -f dist/*.tar.gz dist/*.whl dist/*.egg
.PHONY: upload-to-pypi

install-autoclass: ## Install AutoClass C
	# https://ti.arc.nasa.gov/tech/rse/synthesis-projects-applications/autoclass/autoclass-c/
	wget -q https://ti.arc.nasa.gov/m/project/autoclass/autoclass-c-3-3-6.tar.gz
	tar zxvf autoclass-c-3-3-6.tar.gz
	rm -f autoclass-c-3-3-6.tar.gz
.PHONY: install-autoclass

doc: doc/source ## Build documentation
	cd doc && make html
.PHONY: doc

clean-notebooks: ## Clean demo files
	rm -f notebooks/autoclass*
	rm -f notebooks/nohup.out
	rm -f notebooks/*.tsv
.PHONY: clean-demo

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
