"""Minimal OpenAI-compatible chat client (stdlib only).

Works with any OpenAI-compatible endpoint: DeepSeek, Kimi (Moonshot),
Qwen (DashScope), SiliconFlow, OpenAI, and more.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"


def _env(*names, default=None):
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return default


def chat(
    messages,
    model=None,
    base_url=None,
    api_key=None,
    temperature=0.3,
    max_tokens=4096,
) -> str:
    model = model or _env("TOOL2AGENT_MODEL", "OPENAI_MODEL", default=DEFAULT_MODEL)
    base_url = (
        base_url or _env("TOOL2AGENT_BASE_URL", "OPENAI_BASE_URL", default=DEFAULT_BASE_URL)
    ).rstrip("/")
    api_key = api_key or _env("TOOL2AGENT_API_KEY", "OPENAI_API_KEY", default="")

    if not api_key:
        raise RuntimeError(
            "No API key set. Set TOOL2AGENT_API_KEY (or OPENAI_API_KEY).\n"
            "PowerShell: $env:TOOL2AGENT_API_KEY='sk-...'\n"
            "macOS/Linux: export TOOL2AGENT_API_KEY=sk-..."
        )

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        base_url + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM API returned {exc.code}: {body[:600]}") from exc

    return data["choices"][0]["message"]["content"]
