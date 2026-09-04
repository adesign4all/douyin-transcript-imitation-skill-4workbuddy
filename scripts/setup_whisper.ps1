# 部署 whisper.cpp 转写工具（Windows）
# 用法: powershell -ExecutionPolicy Bypass -File setup_whisper.ps1 -WorkDir "<目标目录>"
param(
    [string]$WorkDir = "."
)

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null

Write-Host "[1/3] 下载 whisper.cpp 二进制..."
$binZip = Join-Path $WorkDir "whisper-bin.zip"
Invoke-WebRequest -Uri "https://github.com/ggml-org/whisper.cpp/releases/download/v1.7.6/whisper-bin-x64.zip" -OutFile $binZip
Expand-Archive -Path $binZip -DestinationPath $WorkDir -Force
Remove-Item $binZip

Write-Host "[2/3] 下载中文模型 ggml-small-q5_1.bin (约190MB)..."
Invoke-WebRequest -Uri "https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-small-q5_1.bin" -OutFile (Join-Path $WorkDir "ggml-small-q5_1.bin")

Write-Host "[3/3] 部署完成。使用:"
Write-Host "  $WorkDir\Release\whisper-cli.exe -m $WorkDir\ggml-small-q5_1.bin -l zh -f <audio.wav> -otxt -of <输出前缀> -nt -pp"