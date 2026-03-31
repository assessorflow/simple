"""DeepEval quality tests for the greeting workflow."""

import pytest
from deepeval import assert_output
from deepeval.assertion import Assertor, Criterion
from deepeval.metrics import GEval

from src.agent import GreetingAgent


class TestGreetingQuality:
    """Test suite for greeting quality using DeepEval assertions."""

    @pytest.mark.asyncio
    @pytest.mark.deepeval
    async def test_friendly_greeting_contains_name(self, agent: GreetingAgent):
        """Assert friendly greeting includes the person's name."""
        result = await agent.greet(name="Alice", style="friendly")

        assert_output(
            input="Greet Alice with style=friendly",
            actual_output=result.message,
            assertor=Assertor(
                criteria=[
                    Criterion(
                        name="contains_name",
                        expected="Alice",
                        operator="contains",
                    ),
                    Criterion(
                        name="is_friendly_tone",
                        expected=["hello", "hi", "hey", "greetings"],
                        operator="contains_any",
                    ),
                ]
            ),
        )

    @pytest.mark.asyncio
    @pytest.mark.deepeval
    async def test_formal_greeting_no_slang(self, agent: GreetingAgent):
        """Assert formal greeting avoids casual/slang language."""
        result = await agent.greet(name="Dr. Smith", style="formal")

        formal_tone_metric = GEval(
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

        await formal_tone_metric.measure(input="Dr. Smith", actual_output=result.message)
        assert formal_tone_metric.score >= 0.7, f"Formal tone score: {formal_tone_metric.score}"

    @pytest.mark.asyncio
    @pytest.mark.deepeval
    async def test_casual_greeting_appropriateness(self, agent: GreetingAgent):
        """Assert casual greeting has relaxed, informal tone."""
        result = await agent.greet(name="Bob", style="casual")

        casual_tone_metric = GEval(
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

        await casual_tone_metric.measure(actual_output=result.message)
        assert casual_tone_metric.score >= 0.6

    @pytest.mark.asyncio
    @pytest.mark.deepeval
    async def test_greeting_minimum_length(self, agent: GreetingAgent):
        """Assert greeting has sufficient content (not too short)."""
        result = await agent.greet(name="Charlie", style="friendly")

        assert_output(
            input="Greet Charlie",
            actual_output=result.message,
            assertor=Assertor(
                criteria=[
                    Criterion(
                        name="minimum_length",
                        expected=10,
                        operator="length_gte",
                    ),
                ]
            ),
        )
