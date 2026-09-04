# 贡献指南

感谢你考虑为「抖音逐字稿仿写 Skill」做出贡献！🎉

## 🐛 报告 Bug

发现 Bug？欢迎提 Issue。请使用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug_report.md)，并附上：

- 复现步骤
- 预期行为 vs 实际行为
- SKILL.md 的 frontmatter 内容
- 报错截图或日志
- 环境信息（OS、Python 版本、WorkBuddy 版本）

## 💡 提交功能建议

有想法？用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature_request.md)，描述：

- 你想解决什么问题
- 建议的方案
- 是否愿意贡献代码

## 🔧 提交 Pull Request

### 本地开发流程

```bash
# 1. Fork 并克隆
git clone https://github.com/your-username/douyin-transcript-imitation-skill.git
cd douyin-transcript-imitation-skill

# 2. 创建分支
git checkout -b feat/your-feature

# 3. 改完后跑本地校验
python scripts/validate_skill.py SKILL.md

# 4. 提交
git add .
git commit -m "feat: add XX feature"
git push origin feat/your-feature

# 5. 在 GitHub 上开 PR
```

### 提交规范

我们用 [Conventional Commits](https://www.conventionalcommits.org/)：

| 前缀 | 用途 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug 修复 |
| `docs:` | 文档变更 |
| `refactor:` | 重构 |
| `test:` | 测试 |
| `chore:` | 构建/工具/杂项 |

### 修改 SKILL.md 的注意

- frontmatter 改动必须通过 `python scripts/validate_skill.py` 校验
- 任何含特殊字符（`:`、`+`、`【】`、`""`、`''`）的字段值必须用英文双引号包裹
- 修改后用 WorkBuddy 客户端实测一遍

### 修改 references/ 的注意

- 这是 AI 按需查阅的参考文档，文字密度要高、可执行性要强
- 例子尽量用真实场景而非 Lorem Ipsum

### 修改 templates/ 的注意

- 模板字段命名要稳定，新加字段请同步更新 examples/ 里的示例
- 字段顺序按用户阅读顺序排

## 📋 代码风格

- Python：PEP 8 + 4 空格缩进
- Markdown：标题层级不超过 4 级，列表用 `-` 而非 `*`
- 文件名：英文 + 短横线（`transcript-template.md`）
- 中文文档：英文标点统一用半角，中文标点统一用全角

## 🤝 社区准则

参与本项目即代表你同意遵守 [Code of Conduct](CODE_OF_CONDUCT.md)。

## ❓ 提问

- 一般问题：开 [Discussion](https://github.com/your-username/douyin-transcript-imitation-skill/discussions)
- Bug 报告：用 [Issue 模板](.github/ISSUE_TEMPLATE/bug_report.md)
- 安全问题：看 [SECURITY.md](SECURITY.md)（不要在公开 Issue 里发）

## 📜 许可证

贡献者同意其贡献按 [MIT License](LICENSE) 授权。
