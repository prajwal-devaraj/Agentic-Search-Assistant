# Security baseline

- Never commit API keys. Use environment variables or a secret manager.
- Restrict CORS in production.
- Add authentication before storing user histories.
- Treat retrieved web content as untrusted input.
- Do not allow retrieved pages to directly authorize tool actions.
- Use URL allow/deny policies for enterprise deployments.
- Sanitize rendered markdown and links.
- Rate-limit public endpoints.
- Keep tool permissions explicit and least-privilege.
- Separate user-visible framework traces from private model reasoning.
- Encrypt durable user data at rest and in transit.
- Add deletion/export workflows before launching account-based memory.

PRAJNA trust scores are heuristics and must not be presented as guarantees, especially for medical, legal, financial, or safety-critical decisions.
