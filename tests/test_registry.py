from agentstudio.models import AgentCard
from agentstudio.registry import Registry


def test_register_get_list_find(tmp_path):
    reg = Registry(tmp_path / "registry.json")
    card = AgentCard(
        id="a1",
        name="Agent one",
        framework="langgraph",
        skills=["research"],
        endpoint="http://localhost:9001",
    )
    reg.register(card)

    fetched = reg.get("a1")
    assert fetched is not None
    assert fetched.name == "Agent one"

    assert [c.id for c in reg.list()] == ["a1"]
    assert [c.id for c in reg.find_by_skill("research")] == ["a1"]
    assert reg.find_by_skill("nope") == []
    assert reg.get("missing") is None


def test_registry_persists_across_instances(tmp_path):
    path = tmp_path / "registry.json"
    Registry(path).register(
        AgentCard(id="a2", name="Agent two", framework="crewai", endpoint="http://x")
    )
    # a fresh Registry instance pointed at the same file should see it
    assert Registry(path).get("a2") is not None
