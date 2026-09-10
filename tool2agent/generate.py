"""Core pipeline: gather docs -> build prompt -> call LLM -> write persona."""
from __future__ import annotations

import os
import re

from . import fetch, llm, template


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower().strip())
    return s.strip("-") or "agent"


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text + "\n"


def _skeleton(meta: dict, docs: str) -> str:
    name = meta.get("name") or "Tool"
    return f"""---
name: {name} Engineer
description: TODO: one or two concrete sentences about what this engineer does.
color: teal
emoji: 🛠️
vibe: TODO: one-line personality.
---

# {name} Engineer

> Skeleton generated without an LLM. Fill in the sections using the docs below,
> or re-run without `--no-llm` after setting an API key.

## Identity & Memory
- Role: TODO
- Personality: TODO

## Core Mission
TODO

## Key API Reference
<!-- paste accurate API usage from the docs below -->

## Process
TODO

## Deliverables
TODO

## Compliance & Safety
TODO

---

## Source
{meta.get('home_page') or meta.get('docs_url') or ''}

## Docs
{docs[:6000]}
"""


def run(args) -> int:
    # --- gather docs & metadata ---
    if args.pypi:
        meta = fetch.fetch_pypi(args.pypi)
        docs = meta.get("description") or ""
        slug = slugify(meta.get("name") or args.pypi)
    elif args.url:
        url = args.url.rstrip("/")
        if url.endswith((".md", ".txt", ".rst")):
            docs = fetch.fetch_url(url)
        else:
            docs = fetch.fetch_with_scrapling(url)
        slug = slugify(url.split("/")[-1] or "tool")
        meta = {
            "name": slug.replace("-", " ").title(),
            "summary": "",
            "version": "",
            "home_page": url,
            "docs_url": url,
        }
    else:
        print("error: provide --pypi <package> or --url <docs-url>")
        return 2

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, f"{slug}.md")

    if args.no_llm:
        content = _skeleton(meta, docs)
    else:
        prompt = template.build_user_prompt(meta, docs[: args.max_chars])
        messages = [
            {"role": "system", "content": template.SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        raw = llm.chat(
            messages,
            model=args.model,
            base_url=args.base_url,
            api_key=args.api_key,
        )
        content = _strip_fences(raw)

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(content)

    print(f"Wrote persona -> {out_path}")
    return 0
