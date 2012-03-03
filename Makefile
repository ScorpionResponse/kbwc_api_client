SHELL := /bin/bash

pep8:
	find . -name "*.py" -exec pep8 '--ignore=E501' '{}' ';'

test:
	python test.py

pyflakes:
	pyflakes kbwc_api_client

pyc:
	find . -name "*.pyc" -exec rm '{}' ';'
