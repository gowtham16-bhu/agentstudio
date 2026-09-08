from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentCard(BaseModel):
    """A lightweight, OASF-inspired description of an agent.

    This borrows the core idea from the Open Agentic Schema Framework --
    a machine-readable card describing what an agent is and where to
    reach it -- without implementing the full OASF schema. It's enough
    for agentstudio to discover and route to an agent without knowing
    anything about the framework that agent was built in.
    """

    id: str
    name: str
    framework: str  # e.g. "langgraph", "crewai", "custom"
    description: str = ""
    skills: list[str] = Field(default_factory=list)
    endpoint: str  # base URL where this agent's HTTP surface is reachable


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    """A unit of work sent to an agent, modeled loosely on the A2A task
    lifecycle (pending -> in-progress -> completed/failed).

    The MVP server in `server.py` runs tasks synchronously and returns
    the finished Task in one response -- there's no separate polling
    step yet. The status field is still tracked explicitly so a future
    async/streaming server can drop in without changing this shape.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input: dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    output: dict[str, Any] | None = None
    error: str | None = None
    created_at: float = Field(default_factory=time.time)
