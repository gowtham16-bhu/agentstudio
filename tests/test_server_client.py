import contextlib
import socket
import threading
import time

import uvicorn

from agentstudio.client import StudioClient
from agentstudio.models import AgentCard, TaskStatus
from agentstudio.server import create_agent_server


def _free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _ServerThread(threading.Thread):
    def __init__(self, app, port: int):
        super().__init__(daemon=True)
        config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
        self.server = uvicorn.Server(config)

    def run(self) -> None:
        self.server.run()

    def stop(self) -> None:
        self.server.should_exit = True


def test_end_to_end_echo_agent():
    """Spin up a real HTTP server for one agent and drive it entirely
    through StudioClient -- the same path a real control plane would
    take, regardless of what framework sits behind the endpoint."""
    port = _free_port()
    endpoint = f"http://127.0.0.1:{port}"

    card = AgentCard(
        id="echo-agent",
        name="Echo",
        framework="custom",
        skills=["echo"],
        endpoint=endpoint,
    )
    app = create_agent_server(card, lambda payload: {"echo": payload})

    thread = _ServerThread(app, port)
    thread.start()
    client = StudioClient(timeout=5.0)
    try:
        for _ in range(50):  # wait for the server to come up
            try:
                client.get_agent_card(endpoint)
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError("server did not start in time")

        fetched_card = client.get_agent_card(endpoint)
        assert fetched_card.id == "echo-agent"
        assert fetched_card.skills == ["echo"]

        task = client.call(endpoint, {"hello": "world"})
        assert task.status == TaskStatus.COMPLETED
        assert task.output == {"echo": {"hello": "world"}}
    finally:
        thread.stop()
        thread.join(timeout=2)
