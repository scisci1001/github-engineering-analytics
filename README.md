# GitHub Engineering Analytics

Initial FastAPI bootstrap for the GitHub Engineering Analytics project.

## Run locally

```bash
uv sync
uv run uvicorn github_analytics.main:app --reload
```

Open:

- http://localhost:8000/docs
- http://localhost:8000/health

## Run tests

```bash
uv run pytest
```

## Quality checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

## Branding

The application serves the project favicon at:

- http://localhost:8000/favicon.ico
