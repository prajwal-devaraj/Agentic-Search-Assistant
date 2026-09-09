# Contributing

1. Create a focused branch.
2. Add or update tests for behavior changes.
3. Keep provider-specific logic behind adapters.
4. Do not expose model chain-of-thought; use operational traces only.
5. Never commit API keys or user data.
6. Run `make test` and `make lint` before opening a pull request.
