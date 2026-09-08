"""Wrap a two-node LangGraph graph as an agentstudio agent.

Requires:  pip install agentstudio[langgraph]
Run:       uvicorn examples.langgraph_example:app --port 8002
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agentstudio.adapters.langgraph_adapter import wrap_langgraph
from agentstudio.models import AgentCard
from agentstudio.server import create_agent_server


class State(TypedDict):
    text: str
    shout: str


def shout(state: State) -> dict:
    return {"shout": state["text"].upper() + "!"}


builder = StateGraph(State)
builder.add_node("shout", shout)
builder.add_edge(START, "shout")
builder.add_edge("shout", END)
compiled = builder.compile()

card = AgentCard(
    id="shout-agent",
    name="Shout agent (LangGraph)",
    framework="langgraph",
    description="A stateful graph agent, wrapped without modification.",
    skills=["text-transform"],
    endpoint="http://localhost:8002",
)

app = create_agent_server(card, wrap_langgraph(compiled))
