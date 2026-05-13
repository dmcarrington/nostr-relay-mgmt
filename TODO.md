NIP-86 Relay Management — Python Client

Initial commit with basic structure:
- Client: NIP86Client class with all 20+ NIP-86 methods
- CLI: nip86 command for ban/unban pubkeys, block IPs, configure relay
- Tests: Unit tests for core client methods
- Docs: README, CLI usage guide, TODO tracking

Status:
- NIP-86 spec is complete with all 20+ methods
- NIP-98 HTTP auth is fully implemented
- Tests pass
- CLI ready

Known gaps:
- Type hints could be richer (pydantic models for responses)
- CLI needs better error messages and examples

Next steps:
- Add pydantic models for typed responses
- Add integration tests with a real NIP-86 relay
