.PHONY: setup test lint run build clean

setup:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	flake8 domain/ presentation/ core/ --max-line-length=100

run:
	python main.py

build:
	buildozer android debug

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .buildozer bin