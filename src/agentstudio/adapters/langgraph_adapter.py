from __future__ import annotations

from typing import Any, Callable


def wrap_langgraph(compiled_graph: Any) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Return a run_fn(payload) -> dict that calls compiled_graph.invoke().

    `compiled_graph` is whatever `StateGraph(...).compile()` returned.
    agentstudio never touches its nodes, edges, or state schema -- it
    only calls `.invoke()` and forwards the result.
    """

    def run(payload: dict[str, Any]) -> dict[str, Any]:
        result = compiled_graph.invoke(payload)
        # LangGraph state is typically already dict-like; `dict(...)`
        # keeps this honest if a project uses a custom state object.
        return dict(result)

    return run
