# 🛠️ tool2agent

[![CI](https://github.com/bigbaibai-luis/tool2agent/actions/workflows/ci.yml/badge.svg)](https://github.com/bigbaibai-luis/tool2agent/actions/workflows/ci.yml)

Turn any Python tool/library into an [agency-agents](https://github.com/msitarzewski/agency-agents)-style AI persona — automatically, from its real docs.

> [简体中文](README.zh-CN.md)

## What it is

`tool2agent` reads a package's documentation and uses an LLM to generate a ready-to-install **agent persona** (YAML frontmatter + system prompt) with accurate API references and compliance guardrails. No more hand-writing personas or hallucinated APIs.

## How it works

1. **Fetch** — pull the package README from PyPI, or a docs page via Scrapling.
2. **Generate** — an LLM writes the persona from the real docs (never invented).
3. **Write** — saves `agents/<slug>.md`, ready to drop into Claude Code / Cursor / Qwen Code.

## Install

Core is **stdlib-only** (no dependencies). Python 3.9+.

```bash
git clone https://github.com/bigbaibai-luis/tool2agent.git
cd tool2agent
pip install -e .            # installs the `tool2agent` command
```

Optional: Scrapling (only for `--url` on HTML pages):

```bash
pip install "scrapling[fetchers]"
```

## Configure an API key

Default provider is DeepSeek (cheap, OpenAI-compatible). Set:

```bash
# PowerShell
$env:TOOL2AGENT_API_KEY = "sk-..."
# macOS/Linux
export TOOL2AGENT_API_KEY=sk-...
```

Any OpenAI-compatible endpoint works — set `TOOL2AGENT_BASE_URL` + `TOOL2AGENT_MODEL`:

| Provider | Base URL | Model |
|---|---|---|
| DeepSeek (default) | https://api.deepseek.com | deepseek-chat |
| Kimi / Moonshot | https://api.moonshot.cn/v1 | moonshot-v1-8k |
| Qwen / DashScope | https://dashscope.aliyuncs.com/compatible-mode/v1 | qwen-plus |
| SiliconFlow | https://api.siliconflow.cn/v1 | deepseek-ai/DeepSeek-V3 |
| OpenAI | https://api.openai.com/v1 | gpt-4o-mini |

## Usage

```bash
# From a Python package
tool2agent --pypi scrapling
tool2agent --pypi pandas --out-dir agents

# From a docs page (Scrapling fetches HTML)
tool2agent --url https://scrapling.readthedocs.io/en/latest/

# Without an LLM (skeleton only)
tool2agent --pypi requests --no-llm

# Or without installing: python -m tool2agent --pypi scrapling
```

Output: `agents/scrapling.md` (agency-agents persona).

## Example output

See [examples/scrapling-data-engineer.md](examples/scrapling-data-engineer.md).

## Compliance

Generated personas carry a `Compliance & Safety` section. You are responsible for how you use them — don't generate agents for unauthorized scraping, credential stuffing, or data you have no right to collect.

## Project structure

```
tool2agent/
├── tool2agent/            # the package (stdlib only)
│   ├── cli.py
│   ├── fetch.py           # PyPI + Scrapling fetching
│   ├── llm.py             # OpenAI-compatible client
│   ├── template.py        # persona prompt
│   └── generate.py        # pipeline
├── tests/
├── examples/
├── pyproject.toml
├── .github/workflows/ci.yml
├── README.md / README.zh-CN.md
└── LICENSE
```

## License

MIT — see [LICENSE](LICENSE).
