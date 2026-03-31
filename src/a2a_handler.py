"""A2A protocol handler for the greeting agent.

This implements the Agent-to-Agent (A2A) protocol for agent communication.
See: https://github.com/agentprotocol/a2a
"""

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from agent import GreetingAgent


class A2AMessage(BaseModel):
    """A2A message schema."""

    type: str
    content: dict[str, Any]


class A2AAgentCard(BaseModel):
    """Agent card describing this agent's capabilities."""

    name: str = "greeting-agent"
    description: str = "A friendly greeting agent powered by OpenAI Response API"
    version: str = "0.1.0"
    capabilities: dict[str, bool] = {
        "streaming": False,
        "pushNotifications": False,
    }


def create_a2a_routes(app: FastAPI, agent: GreetingAgent) -> None:
    """Add A2A protocol routes to the FastAPI app."""

    agent_card = A2AAgentCard()

    @app.get("/a2a")
    async def get_agent_card():
        """Return the agent card describing this agent."""
        return agent_card.model_dump()

    @app.post("/a2a")
    async def handle_a2a_message(request: Request):
        """Handle an A2A message and return a response."""
        body = await request.json()
        message_type = body.get("type", "")
        content = body.get("content", {})

        if message_type == "greeting":
            name = content.get("name", "World")
            style = content.get("style", "friendly")
            result = await agent.greet(name, style)
            return {
                "type": "greeting_response",
                "content": {"message": result.message, "style": result.style},
            }

        if message_type == "chat":
            text = content.get("text", "")
            response = await agent.handle_message(text)
            return {"type": "chat_response", "content": {"text": response}}

        raise HTTPException(status_code=400, detail=f"Unknown message type: {message_type}")

    @app.get("/a2a/schema")
    async def get_schema():
        """Return the A2A protocol schema supported by this agent."""
        return {
            "types": {
                "greeting": {
                    "input": {"name": "string", "style": "string"},
                    "output": {"message": "string", "style": "string"},
                },
                "chat": {"input": {"text": "string"}, "output": {"text": "string"}},
            }
        }


def mount_a2a_to_fastapi(app: FastAPI, agent: GreetingAgent) -> None:
    """Mount A2A endpoints onto an existing FastAPI app."""
    create_a2a_routes(app, agent)
