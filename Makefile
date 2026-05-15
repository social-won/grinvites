.PHONY: app server daemon build test test-scraper install

app:
	cd web && npm run dev

server:
	cd server && ../.venv312/bin/python -m uvicorn main:app --reload

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

test-scraper:
	cd server && ../.venv312/bin/python -m pytest -vv -s api/test_scraper.py
