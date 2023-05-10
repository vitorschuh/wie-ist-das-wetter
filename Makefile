.PHONY: lint

env:
	pip install -r requirements.txt
	
lint:
	isort src/
	black src/

extract:
	python3 src/extract.py