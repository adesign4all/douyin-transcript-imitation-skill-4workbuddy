# 使用指南

本文档介绍 Skill 的三种输入方式和对应的输出物。

## 输入方式

### 方式 A：抖音分享链接

最常用方式。用户复制抖音 App 内分享的链接，AI 自动下载。

**输入示例**：

```text
帮我仿写这条抖音：https://v.douyin.com/abc123xyz/
```

**AI 内部流程**：

1. 调用 `yt-dlp` 下载视频到临时目录
2. ffmpeg 抽取音轨
3. whisper 转中文文字
4. 走 8 维度分析 → 仿写 → 敏感词扫描

### 方式 B：本地视频文件

用户把视频文件拖入对话窗口。适合处理自己拍的口播稿。

**输入示例**：

```text
把 /Users/me/Downloads/我的口播.mp4 仿写成抖音文案
```

### 方式 C：用户已粘贴的文稿

跳过下载和转写，直接从文稿开始。适合二次创作。

**输入示例**：

```text
仿写这段口播：
"姐妹们看过来！今天教大家一个超简单的美白方法..."
```

## 输出物

每次调用会产出 **3 份标准 Markdown 文件**：

### 文件 1：原稿（transcript）

来源：whisper 转写 + 人工校对（如有）。文件按时间戳分段。

→ 模板：[`templates/transcript-template.md`](../templates/transcript-template.md)
→ 示例：[`examples/sample-output-01-transcript.md`](../examples/sample-output-01-transcript.md)

### 文件 2：分析（analysis）

8 维度爆款分析：钩子/痛点/节奏/口吻/金句/结构/CTA/视听语言。

→ 模板：[`templates/analysis-template.md`](../templates/analysis-template.md)
→ 示例：[`examples/sample-output-02-analysis.md`](../examples/sample-output-02-analysis.md)

### 文件 3：仿写（imitation）

按分析维度 1:1 复刻，生成新文案，并附敏感词扫描结果。

→ 模板：[`templates/imitation-template.md`](../templates/imitation-template.md)
→ 示例：[`examples/sample-output-03-imitation.md`](../examples/sample-output-03-imitation.md)

## 调用参数（高级）

通过自然语言微调：

| 用户说 | 效果 |
|--------|------|
| "用 XX 博主的风格" | 锁定某个口吻特征 |
| "控制在 30 秒" | 调整字数（普通抖音 30 秒约 80-100 字） |
| "加大钩子力度" | 重写前 3 秒 |
| "再口语化一些" | 弱化书面语 |
| "避免广告法风险词" | 严格模式扫描 |
| "生成 3 个备选版本" | 多次输出供挑选 |

## 完整工作流示例

详见 [`references/workflow-examples.md`](../references/workflow-examples.md)，含 4 个真实场景的端到端流程。

## 调试与日志

遇到问题时：

1. **开启详细日志**：在对话中说「请输出详细执行日志」
2. **查看本地临时文件**：默认在 `~/Downloads/douyin-tmp/`
3. **单独测试敏感词**：
   ```bash
   python scripts/sensitive_check.py "你的文案"
   ```
4. **手动验证 SKILL 完整性**：
   ```bash
   python scripts/validate_skill.py SKILL.md
   ```

## 性能与限制

| 指标 | 数值 | 备注 |
|------|------|------|
| 视频大小 | < 500MB | ffmpeg 内存限制 |
| 视频时长 | < 10 分钟 | whisper 推理时间 |
| 仿写速度 | 30-60 秒/篇 | 取决于 LLM |
| 准确率 | 90%+ | 中文普通话标准发音 |
| 敏感词召回 | 95%+ | 10 维度规则覆盖 |

## 隐私与合规

- ✅ 所有处理在用户本地完成
- ✅ 视频文件处理后立即删除
- ❌ 不上传任何用户数据到第三方
- ❌ 不存储历史记录

详见 [SECURITY.md](../SECURITY.md)。
