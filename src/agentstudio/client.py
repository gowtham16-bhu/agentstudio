from __future__ import annotations

from typing import Any

import httpx

from .models import AgentCard, Task


class StudioClient(object):
    """The control-plane side of the mesh: given an agent's endpoint,
    fetch its card or send it a task -- without knowing or caring what
    framework is running behind that endpoint.

    This is the piece a real "Agent Studio" UI would sit on top of: for
    every AgentCard in a Registry, it can show what the agent can do
    (from the card) and route a task to it (over this client) purely by
    URL, regardless of whether that URL is a LangGraph graph, a CrewAI
    crew, or something else entirely.
    """

    def __init__(self, timeout: float = 30.0):
        self._timeout = timeout

    def get_agent_card(self, endpoint: str) -> AgentCard:
        resp = httpx.get(
            f"{endpoint.rstrip('/')}/.well-known/agent-card.json",
            timeout=self._timeout,
        )
        resp.raise_for_status()
        return AgentCard(**resp.json())

    def call(self, endpoint: str, payload: dict[str, Any]) -> Task:
        resp = httpx.post(
            f"{endpoint.rstrip('/')}/tasks",
            json=payload,
            timeout=self._timeout,
        )
        resp.raise_for_status()
        return Task(**resp.json())
