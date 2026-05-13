# NIP-86 Relay Management API — Python Client

A Python library and CLI for managing Nostr relays using NIP-86 (Relay Management API).

## Installation

### From PyPI (when published)

```bash
pip install nostr-relay-mgmt
```

### From GitHub (current development)

```bash
pip install git+https://github.com/dmcarrington/nostr-relay-mgmt.git
```

### From local source (for development)

```bash
git clone https://github.com/dmcarrington/nostr-relay-mgmt.git
cd nostr-relay-mgmt
pip install -e .
```

The `-e` flag installs in "editable" mode, so code changes are immediately available without reinstalling.

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
print(f"Available methods: {methods}")

# List banned users
banned = client.list_banned_pubkeys()
for user in banned:
    print(f"{user.pubkey}: {user.reason}")

# Ban a pubkey
client.ban_pubkey(
    pubkey="abc123...",
    reason="Spam behavior"
)

# Allow a pubkey
client.allow_pubkey(
    pubkey="abc123...",
    reason="Appealed and approved"
)

# Configure relay metadata
client.change_relay_name("My Awesome Relay")
client.change_relay_description("Fast, reliable Nostr relay")
client.change_relay_icon("https://example.com/icon.png")

# Manage event kinds
client.allow_kind(kind=9735)  # Allow zaps
client.disallow_kind(kind=4)  # Disallow encrypted DMs
allowed_kinds = client.list_allowed_kinds()
print(f"Allowed kinds: {allowed_kinds}")
```

### CLI

```bash
# Configure (store admin private key)
$ nip86 configure --relay wss://relay.example.com

# Status
$ nip86 status
Relay: wss://relay.example.com
NIP-86 supported: yes
Methods: supportedmethods, banpubkey, unbanpubkey, listbannedpubkeys, ...

# Ban a pubkey
$ nip86 ban-pubkey abc123def456... --reason "Spam behavior"

# List banned
$ nip86 list-banned
pubkey                                    reason
abc123def456...                           Spam behavior

# Allow a pubkey
$ nip86 allow-pubkey abc123def456... --reason "Appealed"

# Configure relay metadata
$ nip86 set-name "My Awesome Relay"
$ nip86 set-description "Fast, reliable Nostr relay"
$ nip86 set-icon https://example.com/icon.png

# Manage event kinds
$ nip86 allow-kind 9735
$ nip86 disallow-kind 4
$ nip86 list-allowed-kinds

# IP management
$ nip86 block-ip 192.168.1.100 --reason "DoS attack"
$ nip86 list-blocked-ips
```

## Implementation Notes

- Uses NIP-98 for HTTP authentication
- All requests use `Content-Type: application/nostr+json+rpc`
- Error handling returns human-readable messages + structured error codes
- Built with `nostr-tools` and `requests` — no external crypto needed

## NIP-86 Methods Supported

| Method | Status |
|--------|--------|
| `supportedmethods` | ✅ |
| `banpubkey` | ✅ |
| `unbanpubkey` | ✅ |
| `listbannedpubkeys` | ✅ |
| `allowpubkey` | ✅ |
| `unallowpubkey` | ✅ |
| `listallowedpubkeys` | ✅ |
| `listeventsneedingmoderation` | ✅ |
| `allowevent` | ✅ |
| `banevent` | ✅ |
| `listbannedevents` | ✅ |
| `changerelayname` | ✅ |
| `changerelaydescription` | ✅ |
| `changerelayicon` | ✅ |
| `allowkind` | ✅ |
| `disallowkind` | ✅ |
| `listallowedkinds` | ✅ |
| `blockip` | ✅ |
| `unblockip` | ✅ |
| `listblockedips` | ✅ |

## License

MIT
