from __future__ import annotations

import json

import click

from .client import StudioClient
from .registry import Registry


@click.group()
def main() -> None:
    """agentstudio -- a thin control plane for multi-framework agent meshes."""


@main.command(name="list")
@click.option("--registry", "registry_path", default="agent_registry.json", show_default=True)
def list_agents(registry_path: str) -> None:
    """List every agent registered in the mesh."""
    reg = Registry(registry_path)
    cards = reg.list()
    if not cards:
        click.echo(f"No agents registered in {registry_path} yet.")
        return
    for card in cards:
        click.echo(f"{card.id:<20} {card.framework:<10} {card.endpoint}  -- {card.name}")


@main.command(name="call")
@click.argument("endpoint")
@click.option("--input", "input_json", default="{}", show_default=True, help="JSON payload for the task")
def call_agent(endpoint: str, input_json: str) -> None:
    """Send a task to an agent at ENDPOINT, regardless of its framework."""
    client = StudioClient()
    task = client.call(endpoint, json.loads(input_json))
    click.echo(json.dumps(task.model_dump(), indent=2, default=str))


if __name__ == "__main__":
    main()
