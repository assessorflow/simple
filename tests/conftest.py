"""Pytest configuration and fixtures for DeepEval testing."""

import os
import pytest
from dotenv import load_dotenv

# Load env vars from .env for local testing
load_dotenv()


@pytest.fixture(scope="session")
def openai_api_key():
    """Fetch OPENAI_API_KEY from environment for the agent."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set")
    return key


@pytest.fixture(scope="session")
def deepeval_api_key():
    """Fetch DEEPEVAL_OPENAI_API_KEY from environment for the judge."""
    key = os.getenv("DEEPEVAL_OPENAI_API_KEY")
    if not key:
        pytest.skip("DEEPEVAL_OPENAI_API_KEY not set")
    return key


@pytest.fixture(scope="session")
def agent():
    """Create a GreetingAgent instance for testing."""
    from src.agent import GreetingAgent
    return GreetingAgent()
