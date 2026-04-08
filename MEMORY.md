# MEMORY.md - Long-Term Memory

## TTS 语音（MiniMax）

**重要 bug：** OpenClaw 内置 tts 工具调用 MiniMax TTS 一直失败，返回 "no audio data"。
根因：MiniMax API 要求 `voice_id` 必须嵌套在 `voice_setting` 对象里，但 OpenClaw 传的是顶层参数。

**正确格式：**
```python
data = {
    "model": "speech-02-hd",
    "text": "文字",
    "voice_setting": {"voice_id": "female-shaonv"},  # 必须嵌套！
    "stream": False
}
```

**音色表在** `~/.openclaw/workspace/voice_favorites.json`

**临时解决方案：** 用 Python 脚本直接调 MiniMax API 生成 MP3 → ffmpeg 转 opus → message(asVoice=true) 发送。

## 已安装的库

- Homebrew 5.1.5（/opt/homebrew）
- ImageMagick 7.1.2
- darktable CLI 5.4.1
- Python: opencv-python, scikit-image, rembg, matplotlib, wand, Pillow, numpy, scipy, imageio

## 学习内容存档（见 memory/LEARNED-CATALOG.md）

- Darktable 修图技巧：memory/darktable-tips.md
- Darktable 预设风格参数：memory/darktable-presets-styles.md
- Python 修图技巧：memory/python-photo-editing.md
- 学习来源：tavily 全网搜索、官方文档、社区论坛

## 备份方式（永久记住）

- **本地备份**：每次 heartbeat（~30分钟）自动执行 `backup_openclaw.sh local` → `~/openclaw-backup/`
- **GitHub 备份**：每天下午 16:00 自动执行 `backup_openclaw.sh github` → 推送至 `github.com/kaigod7/kkopenclaw`
- **GitHub 推送逻辑**：检查 `~/openclaw-backup/.github_pushed_today` 标记，每日只推一次
- **备份脚本**：`~/.openclaw/workspace/scripts/backup_openclaw.sh`
- **恢复脚本**：`~/.openclaw/workspace/scripts/restore_openclaw.sh`
- **macOS LaunchDaemon（稳定，不受 cron 问题影响）：**
  - `com.openclaw.backup` → 每天 03:00，本地备份
  - `com.openclaw.backup-github` → 每天 16:00，本地 + GitHub 推送
- **GitHub PAT**： stored in TOOLS.md（不在 MEMORY.md 明文存储）
