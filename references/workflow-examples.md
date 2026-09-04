# 工作流示例（Workflow Examples）

本文件给出 Skill 在三种典型触发场景下的完整执行流程，作为 AI 调用本 Skill 时的参考模板。

## 示例 1：用户提供抖音链接

**用户输入**：
> 帮我把这条抖音视频的文案提取出来，并仿写一篇口播逐字稿 https://v.douyin.com/iJ5xyzAB/

**Skill 执行流程**：

1. **解析意图**：识别为"抖音链接 → 提取文案 + 仿写"
2. **下载视频**：
   ```bash
   yt-dlp --no-playlist -f "bv*[height<=1080]+ba/b" \
     -o "./work/%(title)s.%(ext)s" "https://v.douyin.com/iJ5xyzAB/"
   ```
   从输出提取标题（去掉" - 抖音"）→ 例如：`老年人补钙的三个误区`
3. **读取元信息**：
   ```bash
   ffprobe -v error -show_entries format=duration,size \
     -show_entries stream=codec_type,codec_name,width,height \
     -of default=noprint_wrappers=1 "./work/老年人补钙的三个误区.mp4"
   ```
4. **提取音频**：
   ```bash
   ffmpeg -y -v error -i "./work/老年人补钙的三个误区.mp4" \
     -vn -ac 1 -ar 16000 "./work/audio.wav"
   ```
5. **语音转写**：
   ```bash
   ./whisper/Release/whisper-cli.exe -m ./whisper/ggml-small-q5_1.bin \
     -l zh -f "./work/audio.wav" -otxt -of "./work/transcript" -nt -pp
   ```
6. **校正文案**：结合语境修正同音字
7. **特点分析**：按 `templates/analysis-template.md` 输出
8. **仿写逐字稿**：按 `templates/imitation-template.md` 输出
9. **敏感词检测**：
   ```bash
   python scripts/sensitive_check.py "<仿写稿正文>"
   ```
10. **交付三份文件**：
    - `【原稿】老年人补钙的三个误区.txt`
    - `【分析】老年人补钙的三个误区.txt`
    - `【仿写】老年人补钙的三个误区.txt`

## 示例 2：用户提供本地视频文件

**用户输入**：
> 这是我下载好的抖音视频，帮我提取文案并仿写 C:/Users/.../Downloads/video.mp4

**Skill 执行流程**：

1. 跳过下载步骤
2. 从文件名提取标题：`video` → 询问用户或读取元数据获取真实标题
3. 继续执行步骤 3-10

## 示例 3：仅做敏感词检测

**用户输入**：
> 检查这段口播逐字稿有没有抖音敏感词 "老年人要特别注意补钙，最关键的是…"

**Skill 执行流程**：

1. 跳过下载、转写、分析、仿写
2. 直接调用：
   ```bash
   python scripts/sensitive_check.py "老年人要特别注意补钙，最关键的是…"
   ```
3. 输出命中结果 + 处理建议
4. 用户确认后，输出修改后的版本 + 检测记录表

## 异常情况处理

### 下载失败
```
ERROR: 抖音视频下载失败，可能原因：
1. 视频需要登录态验证 → 请尝试在浏览器登录后导出 cookies.txt 给我
2. 视频已删除或设为私密 → 无法下载，请提供本地视频文件
3. 链接格式异常 → 请确认链接形如 https://www.douyin.com/video/xxx 或 https://v.douyin.com/xxx/
```

### whisper 部署失败
```
ERROR: whisper.cpp 部署失败：
- 检查网络是否能访问 hf-mirror.com 与 github.com
- Windows 需启用 PowerShell 脚本执行权限：Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass
- 手动部署请参考 README.md "前置依赖" 章节
```

### 敏感词命中密集
```
命中 X 处敏感词，已自动修改 X 处。请审阅【仿写】文件末尾的检测记录表，确认处理结果符合预期。
如需进一步调整，请告诉我具体段落。
```