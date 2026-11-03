# Unbuilt AI Company

**Unbuilt Systems — Field Guide 001 companion repository**

A practical reference implementation for coordinating AI-assisted workflows with Python, n8n, Hermes Agent, and the Model Context Protocol (MCP).

> **Project status: early foundation / experimental.** This repository is under active development. The six business projects, Hermes integration, MCP integration, and production deployment are not implemented yet. Do not use this software to perform consequential actions or process sensitive production data.

## What exists now

- A FastAPI task API with explicit task states and validated state transitions.
- SQLAlchemy persistence, using SQLite by default for local development and PostgreSQL when `DATABASE_URL` is configured.
- Automated API and service tests.
- Initial architecture and security notes.

## Planned projects

1. Research Intelligence
2. Content Factory
3. Sales Intelligence
4. Customer Support
5. Developer Operations
6. Autonomous Company Orchestrator

These are planned, not yet implemented.

## Requirements

- Python 3.12 or newer
- `pip` or another Python package installer
- PostgreSQL for shared/deployed environments (optional for the initial local SQLite setup)

## Local setup

```bash
cd services/api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e '.[dev]'
uvicorn app.main:app --reload
```

The API defaults to `sqlite:///./unbuilt.db`. To use PostgreSQL, set `DATABASE_URL`, for example:

```bash
export DATABASE_URL='postgresql+psycopg://app:change-me@localhost:5432/unbuilt'
```

Never commit real credentials. Use a secrets manager for deployed environments.

## API quick start

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/tasks \\
  -H 'Content-Type: application/json' \\
  -d '{"task_type":"research","input":{"topic":"MCP authorization patterns"}}'
```

List tasks:

```bash
curl http://127.0.0.1:8000/tasks
```

Get a task:

```bash
curl http://127.0.0.1:8000/tasks/<task-id>
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Run tests

```bash
cd services/api
python -m pytest -q
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./unbuilt.db` | SQLAlchemy database URL |
| `APP_ENV` | `development` | Runtime environment label |
| `LOG_LEVEL` | `INFO` | Logging level |

## Development principles

- Treat agent and workflow outputs as untrusted input.
- Use least-privilege credentials.
- Require explicit human approval for external side effects.
- Persist task state outside the agent's conversational memory.
- Make retried operations idempotent where possible.
- Never claim a project is verified without recorded test evidence.

## License

The initial application code is intended to be released under the MIT License. Documentation licensing and third-party workflow/export licensing are being reviewed before a public release. See `LICENSE` and `docs/licensing.md` for the current status.
