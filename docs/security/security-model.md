# Security Model — Initial Baseline

This service is local-development-only until authentication, authorization, rate limiting, secret management, audit logging, and approval enforcement are implemented.

Required future controls:

- Least-privilege service identities and credentials.
- Explicit allowlists for MCP tools and n8n workflows.
- Human approval for outbound messages, financial actions, publishing, repository writes, and destructive operations.
- Input validation and output schema validation at trust boundaries.
- Prompt-injection-aware handling of retrieved documents and tool output.
- Idempotency keys for retried side effects.
- Redaction of secrets and personal data from logs.
- Immutable audit events for consequential actions.
