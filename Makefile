SHELL := /bin/bash

pep8:
	find . -name "*.py" -exec pep8 '-r' '--ignore=E501' '{}' ';'

test:
	python test.py

pyflakes:
	find . -name "*.py" -exec pyflakes '{}' ';'

pyc:
	find . -name "*.pyc" -exec rm '{}' ';'
