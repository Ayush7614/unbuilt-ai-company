# System Overview

## Current implementation

The current foundation is a synchronous FastAPI service backed by SQLAlchemy. It owns task identity, task status, input, result, error summary, and timestamps. SQLite is the local default; a PostgreSQL SQLAlchemy URL can be supplied for shared environments.

## Planned integration topology

- Hermes Agent: agent runtime and tool-using execution interface.
- n8n: workflow triggers, orchestration, and integrations.
- Python API: validated business logic and canonical task lifecycle.
- MCP: tool discovery and invocation boundary.
- PostgreSQL: durable shared state.
- Human operator: approval authority for consequential side effects.

The integrations above are architectural targets, not current capabilities of this repository.

## Ownership boundaries

The Python service is the source of truth for task state. n8n coordinates workflow steps. Hermes plans and invokes permitted tools. MCP standardizes tool interaction but does not replace authentication or authorization. Human approval is required before consequential external actions.
