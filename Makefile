init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run py.test autoclasswrapper

test-coverage:
	pipenv run py.test --cov-config .coveragerc --cov=autoclasswrapper autoclasswrapper
