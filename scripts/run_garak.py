#!/usr/bin/env python3
"""Garak red teaming runner for the Greeting Agent.

Usage:
    python scripts/run_garak.py --probes prompt_injection,jailbreak,refusal
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv()


def build_generator():
    """Build OpenAICompatible generator from environment."""
    from garak.generators.openai import OpenAICompatible

    api_key = os.getenv("GARAK_OPENAI_API_KEY")
    base_url = os.getenv("GARAK_OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("GARAK_OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        raise ValueError("GARAK_OPENAI_API_KEY environment variable not set")

    return OpenAICompatible(
        uri=base_url,
        api_key=api_key,
        model_name=model,
        config={
            "temperature": 0.7,
            "max_tokens": 500,
        },
    )


def main():
    parser = argparse.ArgumentParser(description="Run Garak red teaming scans")
    parser.add_argument(
        "--probes",
        default="prompt_injection,jailbreak,dan,refusal,leaktxt,amplification",
        help="Comma-separated list of probes to run",
    )
    parser.add_argument(
        "--output",
        default="garak-reports",
        help="Output directory for reports",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override model name",
    )
    args = parser.parse_args()

    os.environ["GARAK_OPENAI_MODEL"] = args.model or os.getenv("GARAK_OPENAI_MODEL", "gpt-4o-mini")

    from garak import garak

    sys.argv = [
        "garak",
        "--generator",
        "OpenAICompatible",
        "--model_name",
        os.environ["GARAK_OPENAI_MODEL"],
        "--probes",
        args.probes,
        "--output_dir",
        args.output,
        "--report_format",
        "sarif",
    ]

    garak.main()


if __name__ == "__main__":
    main()
