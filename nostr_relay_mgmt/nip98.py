"""NIP-98 HTTP Authentication helpers for NIP-86.

NIP-98 spec: https://nips.nostr.com/98
NIP-86 spec: https://nips.nostr.com/86

NIP-98 defines a JWT-style authorization header for Nostr:
- Authorization: Nostr <base64(header)>.<base64(event)>.<sig>
- The event is kind 27235 with tags [u, url], [method, GET/POST/...]
- The sig is a BIP-340 Schnorr signature of the event ID
"""

import base64
import json
import time
from typing import Dict, Any

from nostr_tools import Event, EventTemplate, verify_event, finalize_event, get_private_key


def create_nip98_event(
    method: str,
    url: str,
    private_key_hex: str,
    payload: str = "",
    nonce: str = "",
    created_at: int = None,
) -> Dict[str, Any]:
    """Create a NIP-98 event for HTTP authentication.

    Args:
        method: HTTP method (GET, POST, etc.)
        url: Full URL being accessed
        private_key_hex: 32-byte hex private key
        payload: Optional payload (for POST/PUT requests)
        nonce: Optional nonce to prevent replay attacks
        created_at: Optional timestamp (defaults to now)

    Returns:
        The signed event dict ready for the Authorization header
    """
    if created_at is None:
        created_at = int(time.time())

    # Build the event
    template: EventTemplate = {
        "kind": 27235,
        "created_at": created_at,
        "tags": [
            ["u", url],  # The URL being accessed
            ["method", method],  # HTTP method
        ],
        "content": "",
    }

    # Add optional tags if provided
    if payload:
        template["tags"].append(["payload", payload])
    if nonce:
        template["tags"].append(["nonce", nonce])

    # Sign the event
    event = finalize_event(template, private_key_hex)

    return event


def nip98_header(event: Dict[str, Any]) -> str:
    """Convert a NIP-98 event to an Authorization header value.

    Args:
        event: The signed NIP-98 event dict

    Returns:
        The Authorization header string: "Nostr eyJ0eXAi..."
    """
    # NIP-98 uses JWT format with "Nostr" prefix
    # Header: {"typ": "JWT", "alg": "nostr"}
    header = {"typ": "JWT", "alg": "nostr"}
    header_b64 = base64.urlsafe_b64encode(
        json.dumps(header, separators=(",", ":")).encode()
    ).rstrip(b"=").decode()

    # Payload (the event)
    payload_b64 = base64.urlsafe_b64encode(
        json.dumps(event, separators=(",", ":")).encode()
    ).rstrip(b"=").decode()

    # Signature (the sig tag from the event)
    sig = event.get("sig", "")
    if not sig:
        raise ValueError("Event missing 'sig' field - not a valid NIP-98 event")

    sig_b64 = base64.urlsafe_b64encode(sig.encode()).rstrip(b"=").decode()

    return f"Nostr {header_b64}.{payload_b64}.{sig_b64}"


def nip98_authorization_header(
    method: str,
    url: str,
    private_key_hex: str,
    payload: str = "",
) -> str:
    """Create a complete NIP-98 Authorization header.

    Args:
        method: HTTP method
        url: Full URL
        private_key_hex: 32-byte hex private key
        payload: Optional request body (for POST/PUT)

    Returns:
        Authorization header value
    """
    event = create_nip98_event(method, url, private_key_hex, payload)
    return nip98_header(event)


# For backward compatibility, also expose the low-level functions
__all__ = [
    "create_nip98_event",
    "nip98_header",
    "nip98_authorization_header",
]
