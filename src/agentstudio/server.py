from __future__ import annotations

from typing import Any, Callable

from fastapi import FastAPI, HTTPException

from .models import AgentCard, Task, TaskStatus

RunFn = Callable[[dict[str, Any]], dict[str, Any]]


def create_agent_server(card: AgentCard, run_fn: RunFn) -> FastAPI:
    """Wrap any callable behind a minimal, A2A-inspired HTTP surface.

    `run_fn` is the single seam where a framework's native call happens
    -- a LangGraph `.invoke(...)`, a CrewAI `.kickoff(...)`, or a plain
    function. Nothing about the framework leaks past this function;
    agentstudio only ever speaks the AgentCard/Task shapes over HTTP,
    which is what lets a client on the other side stay framework-blind.

    Exposes:
      GET  /.well-known/agent-card.json   -- who is this agent, what can it do
      POST /tasks                          -- submit a task, run it, return it
      GET  /tasks/{task_id}                -- look up a task by id

    This is intentionally synchronous for the MVP: POST /tasks blocks
    until run_fn returns. A longer-running agent would want an async
    queue and webhook/streaming callbacks -- the Task model already
    carries a status field so that upgrade doesn't require a schema
    change, only a different server implementation behind it.
    """
    app = FastAPI(title=f"agentstudio · {card.name}")
    tasks: dict[str, Task] = {}

    @app.get("/.well-known/agent-card.json", response_model=AgentCard)
    def get_agent_card() -> AgentCard:
        return card

    @app.post("/tasks", response_model=Task)
    def submit_task(payload: dict[str, Any]) -> Task:
        task = Task(input=payload, status=TaskStatus.IN_PROGRESS)
        tasks[task.id] = task
        try:
            task.output = run_fn(payload)
            task.status = TaskStatus.COMPLETED
        except Exception as exc:  # noqa: BLE001 -- surface any agent error to the caller
            task.status = TaskStatus.FAILED
            task.error = str(exc)
        tasks[task.id] = task
        return task

    @app.get("/tasks/{task_id}", response_model=Task)
    def get_task(task_id: str) -> Task:
        task = tasks.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="task not found")
        return task

    return app
