"""CLI for NIP-86 Relay Management."""

import click
import os
from .client import NIP86Client


def get_relay_url() -> str:
    """Get relay URL from environment or config."""
    return os.environ.get("NIP86_RELAY_URL", "wss://relay.damus.io")


def get_admin_privkey() -> str:
    """Get admin private key from environment."""
    privkey = os.environ.get("NIP86_ADMIN_KEY")
    if not privkey:
        raise click.ClickException(
            "NIP86_ADMIN_KEY environment variable not set. "
            "Set it to your 32-byte hex private key for admin operations."
        )
    return privkey


def get_client() -> NIP86Client:
    """Create and return an NIP86Client."""
    return NIP86Client(get_relay_url(), get_admin_privkey())


@click.group()
def cli():
    """CLI for NIP-86 Relay Management API.

    Configure your relay URL and admin key:

        export NIP86_RELAY_URL=wss://relay.example.com
        export NIP86_ADMIN_KEY=your_32_byte_hex_private_key

    Then run commands:
        nip86 status
        nip86 list-banned
        nip86 ban-pubkey <pubkey> --reason "reason"
    """
    pass


@cli.command()
def status():
    """Check relay status and supported NIP-86 methods."""
    try:
        client = get_client()
        relay_info = client.get_relay_info()
        methods = client.get_supported_methods()

        click.echo(f"Relay: {get_relay_url()}")
        click.echo(f"Name: {relay_info.get('name', 'N/A')}")
        click.echo(f"Description: {relay_info.get('description', 'N/A')}")
        click.echo(f"NIP-86 supported: {'yes' if methods else 'no'}")
        if methods:
            click.echo(f"Methods: {', '.join(methods)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("pubkey")
@click.option("--reason", default="No reason provided", help="Reason for banning")
def ban_pubkey(pubkey: str, reason: str):
    """Ban a public key from the relay."""
    try:
        client = get_client()
        success = client.ban_pubkey(pubkey, reason)
        if success:
            click.echo(f"✅ Banned {pubkey}: {reason}")
        else:
            click.echo(f"❌ Failed to ban {pubkey}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("pubkey")
@click.option("--reason", default="No reason provided", help="Reason for unbanning")
def unban_pubkey(pubkey: str, reason: str):
    """Unban a public key."""
    try:
        client = get_client()
        success = client.unban_pubkey(pubkey, reason)
        if success:
            click.echo(f"✅ Unbanned {pubkey}")
        else:
            click.echo(f"❌ Failed to unban {pubkey}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command(name="list-banned")
def list_banned():
    """List all banned public keys."""
    try:
        client = get_client()
        banned = client.list_banned_pubkeys()
        if not banned:
            click.echo("No banned pubkeys.")
            return
        click.echo("pubkey                                    reason")
        click.echo("-" * 60)
        for entry in banned:
            click.echo(f"{entry['pubkey'][:16]}...{entry['pubkey'][-16:]}  {entry['reason']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("pubkey")
@click.option("--reason", default="No reason provided", help="Reason for allowing")
def allow_pubkey(pubkey: str, reason: str):
    """Add a pubkey to the allowlist."""
    try:
        client = get_client()
        success = client.allow_pubkey(pubkey, reason)
        if success:
            click.echo(f"✅ Allowed {pubkey}")
        else:
            click.echo(f"❌ Failed to allow {pubkey}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("pubkey")
@click.option("--reason", default="No reason provided", help="Reason for removing")
def unallow_pubkey(pubkey: str, reason: str):
    """Remove a pubkey from the allowlist."""
    try:
        client = get_client()
        success = client.unallow_pubkey(pubkey, reason)
        if success:
            click.echo(f"✅ Removed {pubkey} from allowlist")
        else:
            click.echo(f"❌ Failed to remove {pubkey}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command(name="list-allowed")
def list_allowed():
    """List all allowed public keys."""
    try:
        client = get_client()
        allowed = client.list_allowed_pubkeys()
        if not allowed:
            click.echo("No allowed pubkeys.")
            return
        click.echo("pubkey                                    reason")
        click.echo("-" * 60)
        for entry in allowed:
            click.echo(f"{entry['pubkey'][:16]}...{entry['pubkey'][-16:]}  {entry['reason']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command(name="list-events-needing-moderation")
def list_events_needing_moderation():
    """List events pending moderation."""
    try:
        client = get_client()
        events = client.list_events_needing_moderation()
        if not events:
            click.echo("No events needing moderation.")
            return
        click.echo("event_id                                  reason")
        click.echo("-" * 60)
        for entry in events:
            click.echo(f"{entry['id'][:16]}...{entry['id'][-16:]}  {entry['reason']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("event_id")
@click.option("--reason", default="No reason provided", help="Reason for allowing")
def allow_event(event_id: str, reason: str):
    """Allow an event that was flagged."""
    try:
        client = get_client()
        success = client.allow_event(event_id, reason)
        if success:
            click.echo(f"✅ Allowed event {event_id}")
        else:
            click.echo(f"❌ Failed to allow event {event_id}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("event_id")
@click.option("--reason", default="No reason provided", help="Reason for banning")
def ban_event(event_id: str, reason: str):
    """Ban an event."""
    try:
        client = get_client()
        success = client.ban_event(event_id, reason)
        if success:
            click.echo(f"✅ Banned event {event_id}")
        else:
            click.echo(f"❌ Failed to ban event {event_id}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command(name="list-banned-events")
def list_banned_events():
    """List all banned events."""
    try:
        client = get_client()
        banned = client.list_banned_events()
        if not banned:
            click.echo("No banned events.")
            return
        click.echo("event_id                                  reason")
        click.echo("-" * 60)
        for entry in banned:
            click.echo(f"{entry['id'][:16]}...{entry['id'][-16:]}  {entry['reason']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("new_name")
def set_name(new_name: str):
    """Update the relay's name."""
    try:
        client = get_client()
        success = client.change_relay_name(new_name)
        if success:
            click.echo(f"✅ Relay name updated to: {new_name}")
        else:
            click.echo("❌ Failed to update relay name")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("new_description")
def set_description(new_description: str):
    """Update the relay's description."""
    try:
        client = get_client()
        success = client.change_relay_description(new_description)
        if success:
            click.echo("✅ Relay description updated")
        else:
            click.echo("❌ Failed to update relay description")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("new_icon_url")
def set_icon(new_icon_url: str):
    """Update the relay's icon URL."""
    try:
        client = get_client()
        success = client.change_relay_icon(new_icon_url)
        if success:
            click.echo(f"✅ Relay icon updated to: {new_icon_url}")
        else:
            click.echo("❌ Failed to update relay icon")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("kind", type=int)
def allow_kind(kind: int):
    """Add an event kind to the allowed list."""
    try:
        client = get_client()
        success = client.allow_kind(kind)
        if success:
            click.echo(f"✅ Kind {kind} is now allowed")
        else:
            click.echo(f"❌ Failed to allow kind {kind}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("kind", type=int)
def disallow_kind(kind: int):
    """Remove an event kind from the allowed list."""
    try:
        client = get_client()
        success = client.disallow_kind(kind)
        if success:
            click.echo(f"✅ Kind {kind} is now disallowed")
        else:
            click.echo(f"❌ Failed to disallow kind {kind}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command(name="list-allowed-kinds")
def list_allowed_kinds():
    """List all allowed event kinds."""
    try:
        client = get_client()
        kinds = client.list_allowed_kinds()
        if not kinds:
            click.echo("No allowed kinds.")
            return
        click.echo(f"Allowed kinds: {', '.join(str(k) for k in kinds)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("ip")
@click.option("--reason", default="No reason provided", help="Reason for blocking")
def block_ip(ip: str, reason: str):
    """Block an IP address."""
    try:
        client = get_client()
        success = client.block_ip(ip, reason)
        if success:
            click.echo(f"✅ Blocked IP: {ip} ({reason})")
        else:
            click.echo(f"❌ Failed to block IP {ip}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("ip")
def unblock_ip(ip: str):
    """Unblock an IP address."""
    try:
        client = get_client()
        success = client.unblock_ip(ip)
        if success:
            click.echo(f"✅ Unblocked IP: {ip}")
        else:
            click.echo(f"❌ Failed to unblock IP {ip}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command(name="list-blocked-ips")
def list_blocked_ips():
    """List all blocked IP addresses."""
    try:
        client = get_client()
        blocked = client.list_blocked_ips()
        if not blocked:
            click.echo("No blocked IPs.")
            return
        click.echo("ip                reason")
        click.echo("-" * 50)
        for entry in blocked:
            click.echo(f"{entry['ip']:16}  {entry['reason']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
