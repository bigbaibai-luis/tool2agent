"""Prompt template for persona generation."""

SYSTEM_PROMPT = (
    "You are an expert at writing AI agent personas in the agency-agents style: "
    "a Markdown file with YAML frontmatter (name, description, color, emoji, vibe) "
    "followed by a system prompt. You are accurate, practical, and safety-conscious."
)


def build_user_prompt(meta: dict, docs: str) -> str:
    return f"""Generate an agency-agents-style agent persona for the tool/library below.

Hard rules:
1. Only use APIs, flags, and facts that appear in the provided docs. NEVER invent anything.
2. If the docs are incomplete, write "verify in the official docs" instead of guessing.
3. Include a "Compliance & Safety" section covering the tool's license and usage boundaries
   (e.g. scraping must respect robots.txt and privacy law; no unauthorized access).
4. Frontmatter must contain exactly: name, description, color, emoji, vibe.
   - name: Title Case, human-readable (e.g. "Pandas Data Analyst"), NOT snake_case.
   - color: a snake_case color name (e.g. indigo, teal).
   - emoji: a single relevant emoji.

Structure (use ## headings):
## Identity & Memory
## Core Mission
## Key API Reference
## Process
## Deliverables
## Compliance & Safety
## Communication Style

Tool metadata:
- name: {meta.get('name')}
- summary: {meta.get('summary')}
- version: {meta.get('version')}
- homepage: {meta.get('home_page')}
- docs: {meta.get('docs_url')}

Documentation (may be truncated):
---
{docs}
---

Output ONLY the Markdown persona. No extra commentary before or after.
"""
