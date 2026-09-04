# 故障排查

本文档按"症状 → 原因 → 修复"组织，帮你快速定位问题。

## 症状 1：上传 WorkBuddy 开放平台提示「frontmatter 无法解析」

**原因**：YAML 格式错误。

**修复**：

```bash
# 1. 跑自动校验
python scripts/validate_skill.py SKILL.md

# 2. 常见问题：
#    - 含特殊字符的字段值未加引号（如 `:`、`+`、`【】`、`,`）
#    - 中文用了中文引号（`""`）而不是英文直引号（`""`）
#    - 多行字段用了 `|` 而忘了缩进

# 3. 标准修复：
#    把有问题的字段值用英文双引号包起来：
description_en: "End-to-end Douyin video workflow: download..."  
#                                          ↑ 这个冒号原本会让 YAML 误判
```

详见 [references/sensitive-word-categories.md](../references/sensitive-word-categories.md) 不，本条在 README 也有。

## 症状 2：yt-dlp 下载失败 / 视频解析不出

**原因**：抖音反爬。

**修复**：

```bash
# 1. 升级 yt-dlp
pip install -U yt-dlp

# 2. 手动复制 cookie
yt-dlp --cookies-from-browser chrome "https://v.douyin.com/xxx"

# 3. 如果仍失败，复制视频源地址直接用：
#    浏览器打开链接 → 右键视频 → 复制视频地址
yt-dlp "https://www.douyin.com/aweme/v1/play/?video_id=xxx"
```

## 症状 3：whisper 转写中文乱码

**原因**：模型不是中文专用。

**修复**：

```powershell
# 重新下载中文模型
cd models
Invoke-WebRequest -Uri "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin" -OutFile "ggml-tiny.bin"

# 推理时指定中文
./whisper.exe -m ggml-tiny.bin -l zh audio.wav
```

## 症状 4：AI 仿写绕过敏感词扫描

**原因**：AI 忽略 prompt 约束。

**修复**：

1. 在 `SKILL.md` 的 prompt 里强调：「必须**调用** `python scripts/sensitive_check.py`，不通过不放行」
2. 检查 `allowed-tools` 是否包含 `Bash`，否则脚本调用会被拒
3. 在 `examples/` 里加反例让 AI 学

## 症状 5：文件输出格式不统一

**原因**：AI 没严格按模板填字段。

**修复**：

1. 把 `templates/imitation-template.md` 的字段都用大写醒目标注：`【必须填写】`
2. 在 `SKILL.md` 里加：`"输出文件必须严格匹配 templates/imitation-template.md 的字段名与顺序"`
3. 提供完整示例（`examples/`）让 AI 模仿

## 症状 6：WorkBuddy 客户端识别不到 Skill

**原因**：目录结构错。

**修复**：

```bash
# 1. 检查 SKILL.md 是否在 skill 根目录
ls -la ~/.config/WorkBuddy/skills/douyin-transcript-imitation-skill/
# 应该看到:
#   SKILL.md
#   references/
#   templates/
#   scripts/

# 2. 检查 SKILL.md 头部是否有 YAML frontmatter
head -5 SKILL.md
# 应该看到:
#   ---
#   name: douyin-transcript-imitation
#   ...
#   ---

# 3. 重启 WorkBuddy 客户端
```

## 症状 7：脚本执行权限不足

**症状**：在对话窗口调用 `python scripts/sensitive_check.py` 报 permission denied。

**原因**：WorkBuddy 沙箱默认禁了 `Bash` 工具的某些子命令。

**修复**：

```bash
# 1. 在 WorkBuddy 中给该 Skill 显式授权
#    客户端 → Skills → 找到 douyin-transcript-imitation → 权限 → 启用 Bash

# 2. 或在 SKILL.md 的 frontmatter 里收紧：
allowed-tools: "Read,Write,Bash(yt-dlp:*),Bash(ffmpeg:*),Bash(python:*)"
```

## 症状 8：CI 校验失败

**症状**：在 GitHub 上看到 ❌ 的红色叉。

**修复**：

1. 点进失败的 Action run
2. 看具体哪一步失败
3. 多数情况是 `validate_skill.py` 报错
4. 本地修复后 push 即可重新触发

## 症状 9：仿写风格不还原

**原因**：references 里的样例不够或 LLM 温度过高。

**修复**：

1. 在 `references/workflow-examples.md` 多加 3-5 个真实爆款案例
2. 在 `SKILL.md` 里把温度调低：
   ```text
   仿写阶段使用较低温度（如 0.5），保持风格稳定
   ```
3. 启用"风格锁定"指令：用户说"严格按 XX 博主风格"

## 症状 10：处理大视频超时

**症状**：超过 10 分钟的视频 whisper 转写卡死。

**修复**：

1. 用 `tiny` 模型先粗转（< 5 分钟完成）
2. 切分视频：`ffmpeg -i input.mp4 -ss 0 -t 600 -c copy part1.mp4`
3. 升级硬件：whisper 推理吃 CPU/GPU

## 仍无法解决？

- 🔍 搜 [GitHub Issues](https://github.com/your-username/douyin-transcript-imitation-skill/issues) 看是否有人遇到过
- 🆕 开新 Issue，用 [Bug Report 模板](../.github/ISSUE_TEMPLATE/bug_report.md)
- 💬 在 [Discussions](https://github.com/your-username/douyin-transcript-imitation-skill/discussions) 提问
