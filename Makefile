.PHONY: build run clean

build:
	python3 -m venv env && \
	. env/bin/activate && \
	pip install -r requirements.txt && \
	deactivate

run:
	. env/bin/activate && \
	python3 src/main.py && \
	deactivate

clean:
	rm -rf env src/__pycache__