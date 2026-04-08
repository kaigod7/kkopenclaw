# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS（飞书语音）

- 当前默认：柔软女孩（Chinese (Mandarin)_Soft_Girl，MiniMax）
- 音色表：~/.openclaw/workspace/voice_favorites.json
- 快捷切换：python3 ~/.openclaw/workspace/scripts/voice_switch.py <编号或名字> <文本>

### 飞书语音发送

- **音色**：MiniMax「柔软女孩」(Chinese (Mandarin)_Soft_Girl)
- **voice_id**：female-shaonv（需嵌套在 voice_setting 对象里）
- **API Key**：`sk-api-A9Ep19sBDPGn_ku4UnKRh1ljpeP8S8xHhc5sBbxr7kgncLbif7ZSpPg8LaLBR7Sg_IbFHJpkbzVt77hkca4jFbmbaF8MCLMqPf3x9bd9EGBTJxggKLtKTww`
- **API 端点**：`https://api.minimaxi.com/v1/t2a_v2`
- **模型**：speech-02-hd
- **返回格式**：hex 字符串，用 `bytes.fromhex()` 解码
- **正确请求格式**：
  ```python
  data = {
      "model": "speech-02-hd",
      "text": "文字",
      "voice_setting": {"voice_id": "female-shaonv"},
      "stream": False
  }
  ```
- **流程**：
  1. POST 请求发送 TTS
  2. `bytes.fromhex()` 解码 hex → MP3
  3. ffmpeg 转 opus → 保存到 ~/.openclaw/workspace/
  4. message(asVoice=true) 发送
- 发之前去掉 emoji

### 网络代理

- flclash 代理端口：127.0.0.1:7890（规则模式）
- 已添加到 ~/.zshrc：
  ```
  export http_proxy=http://127.0.0.1:7890
  export https_proxy=http://127.0.0.1:7890
  ```
- 使用场景：Terminal 内使用 claude 等需要访问境外 API 的工具
- 注意：flclash 规则模式下，terminal 流量不依赖其规则分流，靠环境变量直连代理
- 如遇 "Unable to connect to Anthropic services" 报错，先检查代理是否开启

### 语音识别（funasr）

- 使用 paraformer-large 模型（modelscope 缓存）
- 转换：ffmpeg -i voice.ogg -ar 16000 /tmp/voice.wav
- 识别：python3 -c "from funasr import AutoModel; model = AutoModel(model='/Users/kk/.cache/modelscope/models/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch', device='cpu'); print(model.generate('/tmp/voice.wav')[0]['text'])"
- 备注：不用走 HuggingFace，直接用 modelscope 缓存，代理关了也能用

### 文件发送规则

- **所有对外发送的文件必须先保存到 ~/.openclaw/workspace/ 再发送**，不要从其他路径直接发送
- 收到文件请求时，优先复制到 workspace 目录再操作
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### 备份（永久记住）

| 周期 | 触发 | 目标 |
|------|------|------|
| ~30分钟 | heartbeat 自动 | 本地 `~/openclaw-backup/` |
| 每天 16:00 | LaunchDaemon | 本地 + GitHub `kaigod7/kkopenclaw` |
| 每天 03:00 | LaunchDaemon | 本地备份 |

备份脚本：`~/.openclaw/workspace/scripts/backup_openclaw.sh`
- `bash backup_openclaw.sh local` — 仅本地（heartbeat 调用）
- `bash backup_openclaw.sh github` — 本地 + GitHub（16:00 调用）

GitHub Token：`~/.openclaw/workspace/.gh-token`（本地私有，不上传 GitHub）

macOS LaunchDaemon：
- `~/Library/LaunchAgents/com.openclaw.backup.plist`（03:00 本地）
- `~/Library/LaunchAgents/com.openclaw.backup-github.plist`（16:00 GitHub）

GitHub 仓库：github.com/kaigod7/kkopenclaw
