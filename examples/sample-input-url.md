# 输入示例：抖音分享链接

## 用户原始输入

```text
@douyin-transcript-imitation
帮我仿写这条抖音：https://v.douyin.com/abc123xyz/

主题：职场新人如何快速融入团队
风格：参考原博主的亲切感
```

## AI 识别到的信息

| 字段 | 值 | 来源 |
|------|-----|------|
| 输入类型 | 抖音分享链接 | URL 模式匹配 |
| 触发 Skill | douyin-transcript-imitation | @ 触发 |
| 主题 | 职场新人如何快速融入团队 | 用户补充 |
| 风格要求 | 亲切感 | 用户补充 |
| 时长预估 | ~45 秒（基于 yt-dlp 元数据） | 工具返回 |

## 解析后的内部数据

```yaml
input:
  type: url
  url: "https://v.douyin.com/abc123xyz/"
  topic: "职场新人如何快速融入团队"
  style: "亲切、贴近生活"
constraints:
  max_duration: 60  # 秒
  cta: "关注获取更多职场干货"  # 自动推断
```

## 进入工作流

按 `SKILL.md` 的 prompt 流程：

1. **下载**：yt-dlp → `videos/abc123xyz.mp4`（约 12MB）
2. **抽音**：ffmpeg → `videos/abc123xyz.wav`
3. **转写**：whisper（tiny 模型，中文）→ 原始文稿
4. **校对**：AI 自动分段
5. **分析**：8 维度填充
6. **仿写**：按"亲切感"风格 + 主题
7. **扫描**：`sensitive_check.py`
8. **输出**：3 份 Markdown 文件

## 对应的输出

- [阶段 1：原稿](sample-output-01-transcript.md)
- [阶段 2：分析](sample-output-02-analysis.md)
- [阶段 3：仿写](sample-output-03-imitation.md)
