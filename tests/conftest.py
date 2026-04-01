"""Pytest configuration and fixtures for DeepEval testing."""

import os
import pytest
from dotenv import load_dotenv

# Load env vars from .env for local testing
load_dotenv()

# Configure LiteLLM for DeepEval
os.environ.setdefault("USE_LITELLM", "true")
os.environ.setdefault("LITELLM_PROXY_API_BASE", "http://labs.walfa.my.id:4000")
os.environ.setdefault("LITELLM_PROXY_API_KEY", "sk-qsL5RlIGHSvuJtmNLUjeCA")
os.environ.setdefault("LITELLM_MODEL_NAME", "MiniMax-M2.7")

# Configure PyRIT for red teaming
os.environ.setdefault("OPENAI_CHAT_ENDPOINT", "http://labs.walfa.my.id:4000")
os.environ.setdefault("OPENAI_CHAT_KEY", "sk-qsL5RlIGHSvuJtmNLUjeCA")
os.environ.setdefault("OPENAI_CHAT_MODEL", "qwen3.5-plus")


@pytest.fixture(scope="session")
def openai_api_key():
    """Fetch OPENAI_API_KEY from environment for the agent."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set")
    return key


@pytest.fixture(scope="session")
def deepeval_api_key():
    """Fetch LITELLM_PROXY_API_KEY from environment for DeepEval."""
    key = os.getenv("LITELLM_PROXY_API_KEY")
    if not key:
        pytest.skip("LITELLM_PROXY_API_KEY not set")
    return key


@pytest.fixture(scope="session")
def agent():
    """Create a GreetingAgent instance for testing."""
    from agent import GreetingAgent
    return GreetingAgent()
