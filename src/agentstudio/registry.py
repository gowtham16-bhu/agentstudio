from __future__ import annotations

import json
from pathlib import Path

from .models import AgentCard


class Registry:
    """A minimal agent registry, backed by a single JSON file.

    A real OASF deployment runs a schema server; this is deliberately
    the smallest thing that works so a demo or a small internal mesh
    needs zero extra infrastructure. Swap this class for one backed by
    a database or the real OASF server without changing anything else
    in agentstudio -- callers only ever see AgentCard objects.
    """

    def __init__(self, path: str | Path = "agent_registry.json"):
        self.path = Path(path)
        if not self.path.exists():
            self.path.write_text("{}")

    def _read(self) -> dict:
        raw = self.path.read_text().strip()
        return json.loads(raw) if raw else {}

    def _write(self, data: dict) -> None:
        self.path.write_text(json.dumps(data, indent=2))

    def register(self, card: AgentCard) -> None:
        data = self._read()
        data[card.id] = card.model_dump()
        self._write(data)

    def get(self, agent_id: str) -> AgentCard | None:
        raw = self._read().get(agent_id)
        return AgentCard(**raw) if raw else None

    def list(self) -> list[AgentCard]:
        return [AgentCard(**v) for v in self._read().values()]

    def find_by_skill(self, skill: str) -> list[AgentCard]:
        return [card for card in self.list() if skill in card.skills]
