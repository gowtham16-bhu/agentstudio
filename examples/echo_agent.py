"""Minimal example agent with zero framework dependencies.

Run it to see agentstudio's HTTP surface without installing LangGraph
or CrewAI:

    uvicorn examples.echo_agent:app --port 8001

Then, from another terminal:

    agentstudio call http://localhost:8001 --input '{"hello": "world"}'
"""

from agentstudio.models import AgentCard
from agentstudio.server import create_agent_server


def run(payload: dict) -> dict:
    return {"echo": payload}


card = AgentCard(
    id="echo-agent",
    name="Echo agent",
    framework="custom",
    description="Returns whatever it's given. Useful for testing the mesh.",
    skills=["echo"],
    endpoint="http://localhost:8001",
)

app = create_agent_server(card, run)
