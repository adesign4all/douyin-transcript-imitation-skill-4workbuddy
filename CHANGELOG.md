# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- 支持多语种识别（英/日/韩）
- 加入 B 站、小红书等平台链接解析
- 仿写质量自动评分（与原视频对比）

## [1.0.0] - 2026-09-04

### Added
- 🎉 首发版本
- 支持抖音分享链接下载（基于 yt-dlp）
- 支持本地视频文件处理
- 中文语音转写（whisper.cpp 一键部署脚本）
- 8 维度爆款分析框架
- 10 维度敏感词检测（涉政/涉黄/违禁/广告法/医疗夸大/未成年/低俗/暴恐/隐私/版权）
- 3 份标准输出模板（原稿/分析/仿写）
- 完整 SKILL.md frontmatter（含 WorkBuddy 开放平台必填字段）
- 三个 references 参考文档
- CI 校验工作流（GitHub Actions）

### Known Limitations
- 仅支持中文识别
- 抖音反爬限制时链接解析可能失败
- 极端口音识别准确率有限

[Unreleased]: https://github.com/your-username/douyin-transcript-imitation-skill/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/your-username/douyin-transcript-imitation-skill/releases/tag/v1.0.0
