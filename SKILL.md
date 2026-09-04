---
name: douyin-transcript-imitation
display_name: "抖音逐字稿仿写"
display_name_en: "Douyin Script Imitation"
description: "从抖音视频链接或本地视频文件，自动下载、提取口播文案、分析视频特点、仿写一篇亲和力强且通过抖音敏感词检测的口播逐字稿，输出【原稿】【分析】【仿写】三份标准文件。"
description_zh: "抖音视频下载 + 中文语音转写 + 视频特点分析 + 口播逐字稿仿写 + 10 维度敏感词检测，一站式产出可直接发布的口播文案。"
description_en: "End-to-end Douyin video workflow: download, Chinese speech-to-text, video feature analysis, voiceover script imitation, and 10-dimension sensitive-word checking. Outputs three standard deliverable files ready to post."
version: "1.0.0"
category: "内容创作"
author: "WorkBuddy User"
allowed-tools: "Read,Write,Bash,WebFetch"
---

# 抖音逐字稿仿写 Skill

将一条抖音视频（链接或本地文件）转化为三份可直接交付的口播文件：原稿文案 + 视频分析 + 仿写逐字稿（含敏感词检测记录）。

## 触发条件

- 用户发送抖音视频链接或本地视频文件
- 用户说"提取这条视频的文案""仿写逐字稿""分析这条抖音""检查敏感词"
- 命中上述任一意图时，加载本 Skill 执行端到端流程

## 前置依赖

- **yt-dlp**：视频下载工具，环境已内置（`yt-dlp --version` 验证）
- **ffmpeg / ffprobe**：Windows 需可用（`ffmpeg -version` 验证）
- **whisper.cpp**：转写工具，缺失时运行 `scripts/setup_whisper.ps1` 一键部署
  - 二进制：`https://github.com/ggml-org/whisper.cpp/releases/download/v1.7.6/whisper-bin-x64.zip`
  - 中文模型：`https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-small-q5_1.bin`（约 190MB）

## 执行流程

### 0. 下载视频（仅链接来源）
```bash
yt-dlp --no-playlist -f "bv*[height<=1080]+ba/b" -o "<工作目录>/%(title)s.%(ext)s" "<抖音视频链接>"
```
- 支持 `https://www.douyin.com/video/<id>` 与分享短链 `https://v.douyin.com/xxx/`
- **失败处理**：先尝试 `yt-dlp --cookies <cookie文件>`；仍失败则告知用户原因，请其提供本地视频文件，**不得伪造下载成功**
- 用户已提供本地视频：跳过本步，标题从文件名提取并清理" - 抖音"后缀

### 1. 读取元信息
```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_type,codec_name,width,height -of default=noprint_wrappers=1 "<视频路径>"
```

### 2. 提取音频
```bash
ffmpeg -y -v error -i "<视频路径>" -vn -ac 1 -ar 16000 "<工作目录>/audio.wav"
```

### 3. 语音转写
```bash
"<whisper目录>/Release/whisper-cli.exe" -m "<whisper目录>/ggml-small-q5_1.bin" -l zh -f "<工作目录>/audio.wav" -otxt -of "<工作目录>/transcript" -nt -pp
```
读取 `<工作目录>/transcript.txt` 获取转写文本。

### 4. 校正文案
whisper 中文转写常见同音字误差，须结合语境人工校正，参考 `references/expert-profile.md` 中的校正示例。

### 5. 生成三份文件
按 `templates/` 目录下的三个模板输出：
- `【原稿】视频标题.txt` → `templates/transcript-template.md`
- `【分析】视频标题.txt` → `templates/analysis-template.md`
- `【仿写】视频标题.txt` → `templates/imitation-template.md`

### 6. 敏感词检测
```bash
python scripts/sensitive_check.py "<仿写稿正文>"
```
命中词必须修改，并在仿写稿文末记录「命中词 → 处理结果」。完整词库与维度说明见 `references/sensitive-word-categories.md`。

### 7. 交付
用文件展示工具一次性展示三份文件（按原→分析→仿写顺序）。

## 输出规范

| 文件 | 命名 | 来源模板 |
|------|------|----------|
| 原稿文案 | `【原稿】视频标题.txt` | `templates/transcript-template.md` |
| 视频分析 | `【分析】视频标题.txt` | `templates/analysis-template.md` |
| 仿写逐字稿 | `【仿写】视频标题.txt` | `templates/imitation-template.md` |

- 输出目录：用户指定优先，否则与源视频同目录
- 文件名完整保留视频标题（含 # 标签与空格）
- 仿写稿与原文要点一一对应，**但文字不得照抄原文句子**

## 注意事项

- 视频标题以下载元数据为准，清理" - 抖音"等平台后缀
- 模型不支持读图时：**不得编造画面内容**，文案一律以音频转写为准
- 敏感词一经命中必须修改，且交付文件中记录「命中词 → 处理结果」
- 绝对化用语处理：口语强调词（如"最要紧"）改为"特别要紧"等；序数词"第一/第二"属正常列举、非广告宣称，可保留
- 涉及微信推送、发布等外部动作时，**必须先获用户明确确认**
- 完整工作流示例见 `references/workflow-examples.md`