from agentstudio.models import AgentCard, Task, TaskStatus


def test_agent_card_defaults():
    card = AgentCard(id="a1", name="Agent", framework="crewai", endpoint="http://x")
    assert card.skills == []
    assert card.description == ""


def test_task_defaults():
    task = Task(input={"x": 1})
    assert task.status == TaskStatus.PENDING
    assert task.output is None
    assert task.error is None
    assert task.id  # generated automatically
