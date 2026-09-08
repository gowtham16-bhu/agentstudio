"""Wrap a single-agent CrewAI crew as an agentstudio agent.

Requires:  pip install agentstudio[crewai]  (and an LLM API key configured
           for whichever model CrewAI is set up to use)
Run:       uvicorn examples.crewai_example:app --port 8003
"""

from crewai import Agent, Crew
from crewai import Task as CrewTask

from agentstudio.adapters.crewai_adapter import wrap_crewai
from agentstudio.models import AgentCard
from agentstudio.server import create_agent_server

writer = Agent(
    role="Writer",
    goal="Write a one-sentence summary of {topic}",
    backstory="A concise technical writer.",
)
summarize = CrewTask(
    description="Summarize {topic} in one sentence.",
    agent=writer,
    expected_output="One sentence.",
)
crew = Crew(agents=[writer], tasks=[summarize])

card = AgentCard(
    id="summary-agent",
    name="Summary agent (CrewAI)",
    framework="crewai",
    description="A sequential-pipeline agent, wrapped without modification.",
    skills=["summarization"],
    endpoint="http://localhost:8003",
)

app = create_agent_server(card, wrap_crewai(crew))
