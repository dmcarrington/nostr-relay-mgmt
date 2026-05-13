"""Tests for NIP-86 client."""

import unittest
from unittest.mock import patch, MagicMock
from nostr_relay_mgmt.client import NIP86Client


class TestNIP86Client(unittest.TestCase):
    """Test cases for NIP86Client."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = NIP86Client(
            relay_url="wss://relay.example.com",
            admin_privkey="a" * 64  # 64-char hex string
        )

    @patch("nostr_relay_mgmt.client.requests.post")
    def test_get_supported_methods(self, mock_post):
        """Test get_supported_methods returns method list."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": ["supportedmethods", "banpubkey", "listbannedpubkeys"]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        methods = self.client.get_supported_methods()

        self.assertEqual(methods, ["supportedmethods", "banpubkey", "listbannedpubkeys"])
        mock_post.assert_called_once()

    @patch("nostr_relay_mgmt.client.requests.post")
    def test_ban_pubkey(self, mock_post):
        """Test ban_pubkey works correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": True}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.client.ban_pubkey("a" * 64, "spam")

        self.assertTrue(result)

    @patch("nostr_relay_mgmt.client.requests.post")
    def test_ban_pubkey_error(self, mock_post):
        """Test ban_pubkey returns False on error."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "not found"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError):
            self.client.ban_pubkey("a" * 64, "spam")

    @patch("nostr_relay_mgmt.client.requests.get")
    def test_get_relay_info(self, mock_get):
        """Test get_relay_info fetches NIP-11 info."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "Test Relay",
            "description": "A test relay"
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        info = self.client.get_relay_info()

        self.assertEqual(info["name"], "Test Relay")
        mock_get.assert_called_once_with("https://relay.example.com", timeout=10)


if __name__ == "__main__":
    unittest.main()
