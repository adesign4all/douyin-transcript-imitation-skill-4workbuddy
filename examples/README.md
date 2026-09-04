# 示例目录

本目录提供 Skill 的完整输入/输出示例，帮助你快速理解工作流。

## 目录

### 输入示例

| 文件 | 场景 |
|------|------|
| [`sample-input-url.md`](sample-input-url.md) | 用户提供抖音分享链接 |
| （本地视频文件场景） | 用户拖入本地 `.mp4` 文件 |
| （已粘贴文稿场景） | 用户直接粘贴原文稿 |

### 输出示例

| 文件 | 对应模板 | 说明 |
|------|----------|------|
| [`sample-output-01-transcript.md`](sample-output-01-transcript.md) | [`templates/transcript-template.md`](../templates/transcript-template.md) | 阶段 1：whisper 转写后的原稿 |
| [`sample-output-02-analysis.md`](sample-output-02-analysis.md) | [`templates/analysis-template.md`](../templates/analysis-template.md) | 阶段 2：8 维度爆款分析 |
| [`sample-output-03-imitation.md`](sample-output-03-imitation.md) | [`templates/imitation-template.md`](../templates/imitation-template.md) | 阶段 3：仿写 + 敏感词扫描 |

## 端到端示例

完整工作流：用户输入抖音链接 → AI 经过三阶段 → 交付 3 份文件。

```text
用户：帮我仿写这条抖音：https://v.douyin.com/abc123xyz/

AI：（自动触发 douyin-transcript-imitation skill）
    1. 下载视频...
    2. 转写完成 → output/sample-output-01-transcript.md
    3. 8 维度分析完成 → output/sample-output-02-analysis.md
    4. 仿写 + 敏感词扫描通过 → output/sample-output-03-imitation.md
    ✅ 已生成 3 份文件，请查收
```

## 真实场景

### 场景 1：美食博主

> 输入：美食类口播视频（30 秒）  
> 输出：仿写"懒人早餐"主题的同风格新文案

### 场景 2：职场博主

> 输入：职场干货视频（60 秒）  
> 输出：仿写"面试技巧"主题，保留其金句风格

### 场景 3：亲子博主

> 输入：育儿经验视频（45 秒）  
> 输出：仿写"幼小衔接"主题，更亲和的家长口吻

更多场景见 [`references/workflow-examples.md`](../references/workflow-examples.md)。

## 自定义示例

仿照本目录的格式，提交你自己的真实案例：

1. Fork 仓库
2. 在 `examples/` 下加 `my-case-input.md` 和 `my-case-output-*.md`
3. PR 时说明：原视频出处、为什么这个案例有价值
4. 审核通过后会合并到主分支

详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
