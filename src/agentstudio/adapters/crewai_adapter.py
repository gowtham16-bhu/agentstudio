from __future__ import annotations

from typing import Any, Callable


def wrap_crewai(crew: Any) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Return a run_fn(payload) -> dict that calls crew.kickoff(inputs=...).

    `crew` is a `crewai.Crew` instance, built however a project normally
    builds one. agentstudio never touches its agents, tasks, or process
    type -- it only calls `.kickoff()` and forwards a JSON-serializable
    view of the result across the HTTP boundary.
    """

    def run(payload: dict[str, Any]) -> dict[str, Any]:
        result = crew.kickoff(inputs=payload)
        token_usage = getattr(result, "token_usage", None)
        return {
            "raw": getattr(result, "raw", str(result)),
            "token_usage": dict(token_usage) if token_usage else None,
        }

    return run
