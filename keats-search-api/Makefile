.PHONY: setup install run clean

VENV_NAME = keats-env

setup:
	@echo "Setting up environment..."
	@python3 -m venv $(VENV_NAME)
	@( \
		source $(VENV_NAME)/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements.txt \
	)
	@echo "Setup complete."


install:
	. $(VENV_NAME)/bin/activate && pip install -r requirements.txt

run:
	. $(VENV_NAME)/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000

clean:
	rm -rf $(VENV_NAME)
