"""Greeting agent using OpenAI Response API."""

import os
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field


class GreetingInput(BaseModel):
    """Input schema for the greeting agent."""

    name: str = Field(description="The name of the person to greet")
    style: Literal["formal", "casual", "friendly"] = Field(
        default="friendly",
        description="The greeting style",
    )


class GreetingOutput(BaseModel):
    """Output schema for the greeting agent."""

    message: str = Field(description="The generated greeting message")
    style: str = Field(description="The style used for the greeting")


class GreetingAgent:
    """A simple greeting agent powered by OpenAI Response API."""

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    async def greet(self, name: str, style: str = "friendly") -> GreetingOutput:
        """Generate a greeting message."""
        style_prompts = {
            "formal": f"Write a formal greeting for {name}.",
            "casual": f"Write a casual, relaxed greeting for {name}.",
            "friendly": f"Write a warm, friendly greeting for {name}.",
        }

        prompt = style_prompts.get(style, style_prompts["friendly"])

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            text={"format": {"type": "text"}},
        )

        return GreetingOutput(
            message=response.output_text,
            style=style,
        )

    async def handle_message(self, message: str) -> str:
        """Handle an arbitrary message and respond appropriately."""
        response = self.client.responses.create(
            model=self.model,
            input=f"Respond to this message as a friendly greeting agent: {message}",
            text={"format": {"type": "text"}},
        )
        return response.output_text


def create_agent() -> GreetingAgent:
    """Factory function to create a GreetingAgent instance."""
    return GreetingAgent()
