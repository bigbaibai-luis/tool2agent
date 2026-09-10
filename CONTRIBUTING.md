# Contributing / 贡献指南

Thanks for considering contributing! / 感谢你考虑贡献！

## How to contribute / 如何贡献

1. Fork the repo / Fork 本仓库
2. Create a branch / 新建分支
3. Make changes / 修改
4. Open a pull request / 提交 PR

## Design rules / 设计规则

- Core (`tool2agent/`) stays **stdlib-only** — do not add third-party runtime deps / 核心保持**纯标准库**，不要引入第三方运行时依赖
- Scrapling remains an optional extra (`--url` on HTML) / Scrapling 保持可选（仅 HTML 抓取用）
- Keep generated personas compliant (robots.txt, ToS, privacy law) / 生成的角色必须带合规护栏

## Local checks / 本地校验

```bash
python -m compileall tool2agent
python -m unittest discover -s tests -v
```

CI runs these automatically / CI 会自动执行。
