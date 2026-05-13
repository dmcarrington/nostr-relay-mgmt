"""NIP-86 relay management client."""

import json
import time
import requests
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from .nip98 import nip98_authorization_header


class NIP86Client:
    """Client for NIP-86 Relay Management API.

    Args:
        relay_url: WebSocket URL of the relay (e.g., wss://relay.example.com)
        admin_privkey: 32-byte hex private key for admin operations

    NIP-86 spec: https://nips.nostr.com/86
    NIP-98 auth: https://nips.nostr.com/98
    """

    def __init__(self, relay_url: str, admin_privkey: str):
        self.relay_url = relay_url.rstrip("/")
        self.http_url = self.relay_url.replace("wss://", "https://").replace("ws://", "http://")
        self.admin_privkey = admin_privkey

    def _make_rpc_call(self, method: str, params: List[Any]) -> Dict[str, Any]:
        """Make a NIP-86 JSON-RPC call to the relay.

        Args:
            method: The NIP-86 method name (e.g., 'banpubkey')
            params: List of method parameters

        Returns:
            The JSON-RPC response dict with 'result' and optional 'error' keys

        Raises:
            requests.HTTPError: If the HTTP request fails
            ValueError: If the response lacks required fields
        """
        # Build the JSON-RPC request
        request_body = {
            "method": method,
            "params": params,
        }

        # NIP-98: Create HTTP auth event with the relay URL as the u tag
        auth_header = nip98_authorization_header(
            method="POST",
            url=self.http_url,
            private_key=self.admin_privkey,
            payload=json.dumps(request_body),
        )

        headers = {
            "Content-Type": "application/nostr+json+rpc",
            "Authorization": auth_header,
        }

        # Make the HTTP POST request
        response = requests.post(
            self.http_url,
            json=request_body,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()

        if "error" in result:
            raise ValueError(f"NIP-86 error: {result['error']}")

        return result

    def get_supported_methods(self) -> List[str]:
        """Get list of supported NIP-86 methods.

        Returns:
            List of method names supported by this relay
        """
        response = self._make_rpc_call("supportedmethods", [])
        return response.get("result", [])

    def ban_pubkey(self, pubkey: str, reason: str) -> bool:
        """Ban a public key from the relay.

        Args:
            pubkey: The 64-character hex pubkey to ban
            reason: Reason for the ban

        Returns:
            True if successful
        """
        response = self._make_rpc_call("banpubkey", [pubkey, reason])
        return response.get("result") is True

    def unban_pubkey(self, pubkey: str, reason: str) -> bool:
        """Unban a public key.

        Args:
            pubkey: The 64-character hex pubkey to unban
            reason: Reason for unbanning

        Returns:
            True if successful
        """
        response = self._make_rpc_call("unbanpubkey", [pubkey, reason])
        return response.get("result") is True

    def list_banned_pubkeys(self) -> List[Dict[str, str]]:
        """List all banned pubkeys.

        Returns:
            List of dicts with 'pubkey' and 'reason' keys
        """
        response = self._make_rpc_call("listbannedpubkeys", [])
        return response.get("result", [])

    def allow_pubkey(self, pubkey: str, reason: str) -> bool:
        """Add a pubkey to the allowlist.

        Args:
            pubkey: The 64-character hex pubkey to allow
            reason: Reason for allowing

        Returns:
            True if successful
        """
        response = self._make_rpc_call("allowpubkey", [pubkey, reason])
        return response.get("result") is True

    def unallow_pubkey(self, pubkey: str, reason: str) -> bool:
        """Remove a pubkey from the allowlist.

        Args:
            pubkey: The 64-character hex pubkey to unallow
            reason: Reason for removal

        Returns:
            True if successful
        """
        response = self._make_rpc_call("unallowpubkey", [pubkey, reason])
        return response.get("result") is True

    def list_allowed_pubkeys(self) -> List[Dict[str, str]]:
        """List all allowed pubkeys.

        Returns:
            List of dicts with 'pubkey' and 'reason' keys
        """
        response = self._make_rpc_call("listallowedpubkeys", [])
        return response.get("result", [])

    def list_events_needing_moderation(self) -> List[Dict[str, str]]:
        """List events pending moderation.

        Returns:
            List of dicts with 'id' and 'reason' keys
        """
        response = self._make_rpc_call("listeventsneedingmoderation", [])
        return response.get("result", [])

    def allow_event(self, event_id: str, reason: str) -> bool:
        """Allow an event that was flagged.

        Args:
            event_id: The 64-character hex event ID
            reason: Reason for allowing

        Returns:
            True if successful
        """
        response = self._make_rpc_call("allowevent", [event_id, reason])
        return response.get("result") is True

    def ban_event(self, event_id: str, reason: str) -> bool:
        """Ban an event.

        Args:
            event_id: The 64-character hex event ID
            reason: Reason for banning

        Returns:
            True if successful
        """
        response = self._make_rpc_call("banevent", [event_id, reason])
        return response.get("result") is True

    def list_banned_events(self) -> List[Dict[str, str]]:
        """List all banned events.

        Returns:
            List of dicts with 'id' and 'reason' keys
        """
        response = self._make_rpc_call("listbannedevents", [])
        return response.get("result", [])

    def list_allowed_events(self) -> List[Dict[str, str]]:
        """List all allowed events.

        Returns:
            List of dicts with 'id' and 'reason' keys
        """
        response = self._make_rpc_call("listallowedevents", [])
        return response.get("result", [])

    def change_relay_name(self, new_name: str) -> bool:
        """Update the relay's name.

        Args:
            new_name: The new relay name

        Returns:
            True if successful
        """
        response = self._make_rpc_call("changerelayname", [new_name])
        return response.get("result") is True

    def change_relay_description(self, new_description: str) -> bool:
        """Update the relay's description.

        Args:
            new_description: The new relay description

        Returns:
            True if successful
        """
        response = self._make_rpc_call("changerelaydescription", [new_description])
        return response.get("result") is True

    def change_relay_icon(self, new_icon_url: str) -> bool:
        """Update the relay's icon URL.

        Args:
            new_icon_url: URL to the new icon image

        Returns:
            True if successful
        """
        response = self._make_rpc_call("changerelayicon", [new_icon_url])
        return response.get("result") is True

    def allow_kind(self, kind: int) -> bool:
        """Add a kind to the allowed list.

        Args:
            kind: The event kind number

        Returns:
            True if successful
        """
        response = self._make_rpc_call("allowkind", [kind])
        return response.get("result") is True

    def disallow_kind(self, kind: int) -> bool:
        """Remove a kind from the allowed list.

        Args:
            kind: The event kind number

        Returns:
            True if successful
        """
        response = self._make_rpc_call("disallowkind", [kind])
        return response.get("result") is True

    def list_allowed_kinds(self) -> List[int]:
        """List all allowed event kinds.

        Returns:
            List of kind numbers
        """
        response = self._make_rpc_call("listallowedkinds", [])
        return response.get("result", [])

    def block_ip(self, ip: str, reason: str) -> bool:
        """Block an IP address.

        Args:
            ip: The IP address to block
            reason: Reason for blocking

        Returns:
            True if successful
        """
        response = self._make_rpc_call("blockip", [ip, reason])
        return response.get("result") is True

    def unblock_ip(self, ip: str) -> bool:
        """Unblock an IP address.

        Args:
            ip: The IP address to unblock

        Returns:
            True if successful
        """
        response = self._make_rpc_call("unblockip", [ip])
        return response.get("result") is True

    def list_blocked_ips(self) -> List[Dict[str, str]]:
        """List all blocked IP addresses.

        Returns:
            List of dicts with 'ip' and 'reason' keys
        """
        response = self._make_rpc_call("listblockedips", [])
        return response.get("result", [])

    def get_relay_info(self) -> Dict[str, Any]:
        """Get relay info via NIP-11.

        Returns:
            Relay information dict
        """
        response = requests.get(self.http_url, timeout=10)
        response.raise_for_status()
        return response.json()
