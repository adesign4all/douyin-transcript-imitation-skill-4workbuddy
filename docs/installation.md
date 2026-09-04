# 安装指南

> 📖 想看怎么**用**？直接看 [usage.md](usage.md)。
>
> 🏗️ 想了解**架构**？看 [architecture.md](architecture.md)。
>
> 🆘 遇到问题？看 [troubleshooting.md](troubleshooting.md)。

本文档介绍三种安装/部署方式，按推荐顺序排列。

## 方式 1：WorkBuddy 开放平台（推荐）

适合：普通用户快速使用。

### 步骤

1. 登录 [workbuddy.cn](https://www.workbuddy.cn/) → 顶部「技能」
2. 点击「添加技能」→ 选「导入 ZIP」→ 上传本仓库根目录的 `douyin-transcript-imitation-skill.zip`
3. 系统自动解析 `SKILL.md` 的 frontmatter，识别必填字段
4. 上传一张 512×512 的 PNG 头像（可从 [WorkBuddy 平台素材库](https://www.workbuddy.cn/materials) 选）
5. 选择类目（推荐：「内容创作 → 短视频工具」）
6. 提交审核（1-2 个工作日）

### 触发使用

在任何 AI 对话窗口：

```text
@douyin-transcript-imitation
帮我仿写这条抖音：https://v.douyin.com/xxxx
```

或者直接说：

```text
用抖音逐字稿仿写这个视频的口播稿
```

### 验证安装

- 在 WorkBuddy 主对话中输入：`触发 skill douyin-transcript-imitation`
- 看到 AI 回复「已加载 XXX skill」即表示成功

---

## 方式 2：本地 WorkBuddy 客户端

适合：本地开发、调试、自定义。

### 步骤

#### Windows

```powershell
# 1. 克隆仓库
git clone https://github.com/your-username/douyin-transcript-imitation-skill.git
cd douyin-transcript-imitation-skill

# 2. 复制到 WorkBuddy 客户端 skill 目录
$skillDir = "$env:APPDATA\WorkBuddy\skills\douyin-transcript-imitation-skill"
New-Item -ItemType Directory -Path $skillDir -Force
Copy-Item -Recurse -Force .\* $skillDir\

# 3. 重启 WorkBuddy 客户端
```

#### macOS

```bash
SKILL_DIR="$HOME/Library/Application Support/WorkBuddy/skills/douyin-transcript-imitation-skill"
git clone https://github.com/your-username/douyin-transcript-imitation-skill.git
mkdir -p "$SKILL_DIR"
cp -r douyin-transcript-imitation-skill/* "$SKILL_DIR/"
# 重启 WorkBuddy 客户端
```

#### Linux

```bash
SKILL_DIR="$HOME/.config/WorkBuddy/skills/douyin-transcript-imitation-skill"
git clone https://github.com/your-username/douyin-transcript-imitation-skill.git
mkdir -p "$SKILL_DIR"
cp -r douyin-transcript-imitation-skill/* "$SKILL_DIR/"
# 重启 WorkBuddy 客户端
```

---

## 方式 3：作为 Python 工具直接使用

适合：CI/CD、批处理、定制工作流。

### 环境要求

- Python 3.8+
- ffmpeg（视频处理）
- yt-dlp（链接下载）
- whisper.cpp 或 faster-whisper（语音识别）

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/douyin-transcript-imitation-skill.git
cd douyin-transcript-imitation-skill

# 2. 安装 Python 依赖
pip install pyyaml

# 3. 验证 SKILL.md 格式
python scripts/validate_skill.py SKILL.md

# 4. 测试敏感词扫描
python scripts/sensitive_check.py "正常文案"
python scripts/sensitive_check.py "100% 治愈 根治"  # 应触发警告

# 5. 部署 whisper（Windows PowerShell）
powershell -ExecutionPolicy Bypass -File scripts/setup_whisper.ps1
```

### 卸载

```bash
# WorkBuddy 开放平台：技能管理 → 删除
# 本地客户端：删除对应 skill 目录即可
# Python：直接 pip uninstall 对应依赖
```

---

## 常见安装错误

| 错误 | 原因 | 修复 |
|------|------|------|
| `frontmatter 无法解析` | YAML 格式错误（特殊字符未引号） | `python scripts/validate_skill.py` 自动定位 |
| `allowed-tools 权限不足` | 平台版本过旧 | 升级到 WorkBuddy 1.0+ |
| `whisper 模型下载失败` | 网络问题 | 手动下载 ggml-tiny.bin 到 models/ |
| `yt-dlp 下载失败` | 抖音反爬 | 升级 yt-dlp：`pip install -U yt-dlp` |
| `ffmpeg 未找到` | 未安装 ffmpeg | `winget install ffmpeg` 或 `brew install ffmpeg` |

更多排查见 [troubleshooting.md](troubleshooting.md)。
