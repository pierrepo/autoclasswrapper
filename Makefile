init:
	pip install pipenv

install: init
	pipenv install --dev --skip-lock

deploy: init
	pipenv install --dev

test:
	pipenv run py.test tests

test-coverage:
	pipenv run py.test --cov-config .coveragerc --cov=autoclasswrapper

compile:
	#pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel

upload-to-pypi: compile
	pipenv run twine upload dist/*
	# clean compiled
	rm -f dist/*.tar.gz
