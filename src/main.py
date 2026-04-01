"""FastAPI application with OpenAI Response API greeting agent and A2A support."""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import GreetingAgent, create_agent
from a2a_handler import mount_a2a_to_fastapi

# Load environment variables
load_dotenv()


class GreetRequest(BaseModel):
    """Request body for the greet endpoint."""

    name: str
    style: str = "friendly"


class GreetResponse(BaseModel):
    """Response body for the greet endpoint."""

    message: str
    style: str


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    message: str


class ChatResponse(BaseModel):
    """Response body for the chat endpoint."""

    response: str


# Global agent instance
_agent: GreetingAgent | None = None


def get_agent() -> GreetingAgent:
    """Get or create the agent instance."""
    global _agent
    if _agent is None:
        _agent = create_agent()
    return _agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    agent = get_agent()
    mount_a2a_to_fastapi(app, agent)
    yield
    # Shutdown
    global _agent
    _agent = None


app = FastAPI(
    title="Greeting Agent",
    description="OpenAI Response API agent with A2A compatibility",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Greeting Agent is running",
        "a2a_endpoint": "/a2a",
        "greet_endpoint": "/greet",
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/greet", response_model=GreetResponse)
async def greet(request: GreetRequest):
    """Generate a greeting message."""
    agent = get_agent()

    if request.style not in ["formal", "casual", "friendly"]:
        raise HTTPException(
            status_code=400,
            detail="Style must be one of: formal, casual, friendly",
        )

    result = await agent.greet(request.name, request.style)
    return GreetResponse(message=result.message, style=result.style)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the agent."""
    agent = get_agent()
    response = await agent.handle_message(request.message)
    return ChatResponse(response=response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
