PYTHON ?= python

.PHONY: install install-dev lint type-check test requirements-check security run-api run-app docker-build docker-up docker-down docker-test ci

requirements-ci.txt:
	$(PYTHON) scripts/sanitize_requirements.py requirements.txt requirements-ci.txt --with-dev

requirements-runtime.txt:
	$(PYTHON) scripts/sanitize_requirements.py requirements.txt requirements-runtime.txt

install: requirements-runtime.txt
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements-runtime.txt

install-dev: requirements-ci.txt
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements-ci.txt

lint:
	$(PYTHON) -m flake8 api.py app.py tests --max-line-length=120 --extend-ignore=E203,W503 --exit-zero

type-check:
	$(PYTHON) -m mypy api.py --ignore-missing-imports

test:
	$(PYTHON) -m pytest tests -q --cov=api --cov-report=term --cov-report=xml

requirements-check:
	$(PYTHON) -m pip check

security:
	$(PYTHON) -m pip install pip-audit bandit
	pip-audit -r requirements-ci.txt || true
	bandit -r api.py app.py || true

run-api:
	uvicorn api:app --host 0.0.0.0 --port 8000

run-app:
	streamlit run app.py

docker-build:
	docker build --target backend -t oraclefmcg-backend:local .
	docker build --target frontend -t oraclefmcg-frontend:local .

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v

docker-test:
	curl -fsS http://localhost:8000/health
	curl -fsS http://localhost:8501 > /dev/null

ci: install-dev lint requirements-check test
