# NIP-86 Relay Management API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python client and CLI for managing Nostr relays using [NIP-86](https://nips.nostr.com/86) (Relay Management API).

## Features

- Full NIP-86 method support (ban/unban pubkeys, block IPs, manage event kinds, configure relay metadata)
- Python API with type hints
- CLI for quick management from terminal
- Built with `requests` and `nostr-tools` — no external crypto needed

## Installation

```bash
pip install nostr-relay-mgmt
```

## Usage

### Python API

```python
from nostr_relay_mgmt import NIP86Client

client = NIP86Client(
    relay_url="wss://relay.example.com",
    admin_privkey="your_32_byte_hex_private_key"
)

# Get supported methods
methods = client.get_supported_methods()

# List banned users
banned = client.list_banned_pubkeys()

# Ban a pubkey
client.ban_pubkey("pubkey_hex", "Spam behavior")
```

### CLI

```bash
export NIP86_RELAY_URL=wss://relay.example.com
export NIP86_ADMIN_KEY=your_32_byte_hex_private_key

nip86 status
nip86 list-banned
nip86 ban-pubkey <pubkey> --reason "reason"
```

## NIP-86 Methods

| Method | CLI | Status |
|--------|-----|--------|
| `supportedmethods` | `nip86 status` | ✅ |
| `banpubkey` | `nip86 ban-pubkey` | ✅ |
| `unbanpubkey` | `nip86 unban-pubkey` | ✅ |
| `listbannedpubkeys` | `nip86 list-banned` | ✅ |
| `allowpubkey` | `nip86 allow-pubkey` | ✅ |
| `unallowpubkey` | `nip86 unallow-pubkey` | ✅ |
| `listallowedpubkeys` | `nip86 list-allowed` | ✅ |
| `listeventsneedingmoderation` | `nip86 list-events-needing-moderation` | ✅ |
| `allowevent` | `nip86 allow-event` | ✅ |
| `banevent` | `nip86 ban-event` | ✅ |
| `listbannedevents` | `nip86 list-banned-events` | ✅ |
| `changerelayname` | `nip86 set-name` | ✅ |
| `changerelaydescription` | `nip86 set-description` | ✅ |
| `changerelayicon` | `nip86 set-icon` | ✅ |
| `allowkind` | `nip86 allow-kind` | ✅ |
| `disallowkind` | `nip86 disallow-kind` | ✅ |
| `listallowedkinds` | `nip86 list-allowed-kinds` | ✅ |
| `blockip` | `nip86 block-ip` | ✅ |
| `unblockip` | `nip86 unblock-ip` | ✅ |
| `listblockedips` | `nip86 list-blocked-ips` | ✅ |

## License

MIT