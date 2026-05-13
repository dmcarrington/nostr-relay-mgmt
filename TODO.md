NIP-86 Relay Management — Python Client

Initial commit with basic structure:
- Client: NIP86Client class with all 20+ NIP-86 methods
- CLI: nip86 command with all management commands
- Tests: Unit tests for core methods
- Docs: README and CLI usage guide

Known gaps:
- NIP-98 auth not yet implemented — relays will reject unauthenticated requests
- Type hints could be richer (pydantic models for responses)
- CLI needs better error messages and examples

Next steps:
- Implement NIP-98 event signing for HTTP auth
- Add pydantic models for typed responses
- Document CLI usage with concrete examples
- Add integration tests with a real NIP-86 relay
