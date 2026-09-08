"""agentstudio -- a thin control plane for meshing agents across frameworks.

The idea: don't compile one workflow definition into every framework's
native format. Instead, let each agent stay in its native runtime
(LangGraph, CrewAI, or anything else), wrap it behind a small HTTP
surface modeled loosely on the A2A task lifecycle and OASF agent cards,
and let a lightweight client route work to it by URL.

Nothing here is a certified implementation of the A2A or OASF specs --
see the README for exactly what is and isn't covered.
"""

from .models import AgentCard, Task, TaskStatus
from .registry import Registry
from .server import create_agent_server
from .client import StudioClient

__version__ = "0.1.0"

__all__ = [
    "AgentCard",
    "Task",
    "TaskStatus",
    "Registry",
    "create_agent_server",
    "StudioClient",
]
