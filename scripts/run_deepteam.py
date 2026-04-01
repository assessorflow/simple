#!/usr/bin/env python3
"""DeepTeam red teaming runner for the Greeting Agent.

Usage:
    python scripts/run_deepteam.py
"""

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Configure LiteLLM
os.environ["OPENAI_API_KEY"] = os.getenv("LITELLM_PROXY_API_KEY", "sk-qsL5RlIGHSvuJtmNLUjeCA")
os.environ["OPENAI_API_BASE"] = os.getenv("LITELLM_PROXY_API_BASE", "http://labs.walfa.my.id:4000")

from deepteam import red_team
from deepteam.vulnerabilities import (
    Bias,
    PIILeakage,
    Toxicity,
    Safety,
    Agentic,
)


def main():
    # Define vulnerabilities to test
    vulnerabilities = [
        Bias(types=["gender", "religion", "race"]),
        PIILeakage(types=["api_and_database_access", "session_leak"]),
        Toxicity(types=["insults"]),
        Safety(types=["illegal_activity", "graphic_content"]),
        Agentic(types=["goal_theft", "recursive_hijacking", "excessive_agency"]),
    ]

    model = os.getenv("LITELLM_MODEL_NAME", "qwen3.5-plus")
    print(f"Running DeepTeam red team scan against {model}...")

    result = red_team(
        model_callback=f"openai/{model}",
        vulnerabilities=vulnerabilities,
    )

    print("\n=== Risk Assessment Overview ===")
    print(result.overview)

    output_dir = Path("deepteam_results")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    result.save(output_dir / timestamp)
    print(f"\nResults saved to {output_dir / timestamp}")

    try:
        result.overview.to_df().to_csv(output_dir / f"overview_{timestamp}.csv", index=False)
        result.test_cases.to_df().to_csv(output_dir / f"test_cases_{timestamp}.csv", index=False)
        print(f"CSV exports saved")
    except Exception as e:
        print(f"Could not export CSVs: {e}")


if __name__ == "__main__":
    main()
