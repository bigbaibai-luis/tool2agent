# 🛠️ tool2agent

[![CI](https://github.com/bigbaibai-luis/tool2agent/actions/workflows/ci.yml/badge.svg)](https://github.com/bigbaibai-luis/tool2agent/actions/workflows/ci.yml)

把任意 Python 工具/库，自动生成一个 [agency-agents](https://github.com/msitarzewski/agency-agents) 风格的 AI 角色——基于它的真实文档。

> [English](README.md)

## 这是什么

`tool2agent` 读取一个库的文档，用 LLM 生成一个可直接安装的 **agent 角色**（YAML frontmatter + 系统提示词），内含准确 API 引用和合规护栏。不用再手写角色，也不会再出现"编造 API"的问题。

## 工作原理

1. **抓取**——从 PyPI 拉取包的 README，或用 Scrapling 抓文档页；
2. **生成**——LLM 基于真实文档写出角色（不编造）；
3. **写出**——保存为 `agents/<slug>.md`，可直接装进 Claude Code / Cursor / Qwen Code。

## 安装

核心**纯标准库、零依赖**，Python 3.9+。

```bash
git clone https://github.com/bigbaibai-luis/tool2agent.git
cd tool2agent
pip install -e .            # 安装 tool2agent 命令
```

可选：Scrapling（仅当 `--url` 抓 HTML 页面时需要）：

```bash
pip install "scrapling[fetchers]"
```

## 配置 API Key

默认走 DeepSeek（便宜、OpenAI 兼容）。设置：

```bash
# PowerShell
$env:TOOL2AGENT_API_KEY = "sk-..."
# macOS/Linux
export TOOL2AGENT_API_KEY=sk-...
```

任何 OpenAI 兼容端点都行——再设 `TOOL2AGENT_BASE_URL` + `TOOL2AGENT_MODEL`：

| 供应商 | Base URL | 模型 |
|---|---|---|
| DeepSeek（默认） | https://api.deepseek.com | deepseek-chat |
| Kimi / 月之暗面 | https://api.moonshot.cn/v1 | moonshot-v1-8k |
| 通义千问 / DashScope | https://dashscope.aliyuncs.com/compatible-mode/v1 | qwen-plus |
| SiliconFlow | https://api.siliconflow.cn/v1 | deepseek-ai/DeepSeek-V3 |
| OpenAI | https://api.openai.com/v1 | gpt-4o-mini |

## 用法

```bash
# 从 Python 包
tool2agent --pypi scrapling
tool2agent --pypi pandas --out-dir agents

# 从文档页（Scrapling 抓 HTML）
tool2agent --url https://scrapling.readthedocs.io/en/latest/

# 不用 LLM（只生成骨架）
tool2agent --pypi requests --no-llm

# 或不安装直接运行：python -m tool2agent --pypi scrapling
```

输出：`agents/scrapling.md`（agency-agents 角色）。

## 示例输出

见 [examples/scrapling-data-engineer.md](examples/scrapling-data-engineer.md)。

## 合规声明

生成的角色自带 `Compliance & Safety` 章节。你对自己如何使用它们负责——不要为未授权的抓取、撞库、或无权采集的数据生成 agent。

## 目录结构

```
tool2agent/
├── tool2agent/            # 包（纯标准库）
│   ├── cli.py
│   ├── fetch.py           # PyPI + Scrapling 抓取
│   ├── llm.py             # OpenAI 兼容客户端
│   ├── template.py        # 角色提示词模板
│   └── generate.py        # 主流程
├── tests/
├── examples/
├── pyproject.toml
├── .github/workflows/ci.yml
├── README.md / README.zh-CN.md
└── LICENSE
```

## 许可证

MIT — 见 [LICENSE](LICENSE)。
