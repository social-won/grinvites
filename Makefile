.PHONY: app server daemon build test install

app:
	cd web && npm run dev

server:
	cd server && uvicorn main:app --reload

daemon:
	python server/api/daemon.py

build:
	cd web && npm run build

VENV := server/api/.venv

install:
	$(VENV)/bin/pip install -r server/requirements.txt
	cd web && npm install

test:
	cd server && api/.venv/bin/python -m pytest
	cd web && npm test
