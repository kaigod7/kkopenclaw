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
- Python 修图技巧：memory/python-photo-editing.md
- 学习来源：tavily 全网搜索、官方文档、社区论坛
