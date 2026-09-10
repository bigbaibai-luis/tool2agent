"""Command-line interface."""
from __future__ import annotations

import argparse

from .generate import run


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="tool2agent",
        description="Turn any Python tool/library into an agency-agents-style AI persona.",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--pypi", metavar="PKG", help="Python package name (fetch README from PyPI)")
    src.add_argument(
        "--url",
        metavar="URL",
        help="Docs page URL (plain fetch for .md/.txt/.rst, Scrapling for HTML)",
    )
    p.add_argument("--out-dir", default="agents", help="Output directory (default: agents)")
    p.add_argument("--model", help="LLM model (default: $TOOL2AGENT_MODEL or deepseek-chat)")
    p.add_argument(
        "--base-url",
        help="OpenAI-compatible base URL (default: $TOOL2AGENT_BASE_URL or DeepSeek)",
    )
    p.add_argument("--api-key", help="API key (default: $TOOL2AGENT_API_KEY)")
    p.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip LLM; write a persona skeleton from the docs only",
    )
    p.add_argument(
        "--max-chars",
        type=int,
        default=8000,
        help="Max docs chars sent to the LLM (default: 8000)",
    )
    args = p.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
