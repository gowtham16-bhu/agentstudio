"""Framework adapters.

Each adapter wraps one framework's native "run" call behind the plain
`dict -> dict` signature `create_agent_server` expects, and does nothing
else -- no state translation, no schema flattening. That's the whole
point: the framework's own runtime keeps doing exactly what it does.

Import an adapter only if the underlying framework is installed:
    pip install agentstudio[langgraph]
    pip install agentstudio[crewai]
"""
