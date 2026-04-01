"""DeepEval quality tests for the greeting workflow."""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval

from agent import GreetingAgent


class TestGreetingQuality:
    """Test suite for greeting quality using DeepEval assertions."""

    @pytest.mark.asyncio
    @pytest.mark.deepeval
    async def test_friendly_greeting_contains_name(self, agent: GreetingAgent):
        """Assert friendly greeting includes the person's name."""
        result = await agent.greet(name="Alice", style="friendly")

        test_case = LLMTestCase(
            input="Greet Alice with style=friendly",
            actual_output=result.message,
        )

        metric = GEval(
            name="Contains Name",
            criteria="The greeting should include the name 'Alice' and have a friendly tone",
            evaluation_steps=[
                "Check if the greeting includes 'Alice'",
                "Check if the greeting sounds friendly (hello, hi, hey, greetings)",
            ],
            evaluation_params=[
                ("input", "The original request"),
                ("actual_output", "The generated greeting"),
            ],
        )

        await assert_test(test_case, metrics=[metric])

    @pytest.mark.asyncio
    @pytest.mark.deepeval
    async def test_formal_greeting_no_slang(self, agent: GreetingAgent):
        """Assert formal greeting avoids casual/slang language."""
        result = await agent.greet(name="Dr. Smith", style="formal")

        test_case = LLMTestCase(
            input="Greet Dr. Smith with style=formal",
            actual_output=result.message,
        )

        metric = GEval(
            name="Formal Tone",
            criteria=(
                "The greeting should sound professional and formal, "
                "avoiding slang, contractions, or casual expressions."
            ),
            evaluation_steps=[
                "Check if the greeting uses formal language",
                "Check if the greeting avoids 'hey', 'hiya', 'sup', etc.",
                "Verify proper titles are used when applicable",
            ],
            evaluation_params=[
                ("input", "The original name"),
                ("actual_output", "The generated greeting"),
            ],
        )

        await assert_test(test_case, metrics=[metric])

    @pytest.mark.asyncio
    @pytest.mark.deepeval
    async def test_casual_greeting_appropriateness(self, agent: GreetingAgent):
        """Assert casual greeting has relaxed, informal tone."""
        result = await agent.greet(name="Bob", style="casual")

        test_case = LLMTestCase(
            input="Greet Bob with style=casual",
            actual_output=result.message,
        )

        metric = GEval(
            name="Casual Tone",
            criteria=(
                "The greeting should sound relaxed and informal. "
                "May include casual expressions but should not be rude."
            ),
            evaluation_steps=[
                "Check if the greeting sounds casual",
                "Ensure it does not sound overly formal or stiff",
            ],
            evaluation_params=[("actual_output", "The generated greeting")],
        )

        await assert_test(test_case, metrics=[metric])

    @pytest.mark.asyncio
    @pytest.mark.deepeval
    async def test_greeting_minimum_length(self, agent: GreetingAgent):
        """Assert greeting has sufficient content (not too short)."""
        result = await agent.greet(name="Charlie", style="friendly")

        test_case = LLMTestCase(
            input="Greet Charlie",
            actual_output=result.message,
        )

        metric = GEval(
            name="Minimum Length",
            criteria="The greeting should be at least 10 characters long",
            evaluation_steps=[
                "Check if the greeting has at least 10 characters",
            ],
            evaluation_params=[("actual_output", "The generated greeting")],
        )

        await assert_test(test_case, metrics=[metric])
