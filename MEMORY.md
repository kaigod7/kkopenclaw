# MEMORY.md - Long-Term Memory

## TTS 语音（MiniMax）

**MiniMax TTS 返回字段：** `result["data"]["audio"]` 不是 `audio_data`！

**默认音色：** MiniMax `Chinese (Mandarin)_Soft_Girl`（音色表1号「柔软女孩」）
**音色表在** `~/.openclaw/workspace/voice_favorites.json`

### 飞书语音气泡发送方法（重要！必须用这个！）

**OpenClaw 的 `asVoice: true` 参数在飞书上无效**，会变成文字消息。

**正确方法：直接调 Feishu 开放 API 发 `msg_type=audio` 消息**

流程：
1. MiniMax TTS → MP3
2. ffmpeg 转 opus
3. Feishu API 上传文件获取 file_key
4. Feishu API 发 `msg_type=audio` 消息

**参考脚本：** `~/.openclaw/workspace/scripts/water_reminder.sh`

**Gateway API：** `POST http://127.0.0.1:18789/tools/invoke` 可主动发飞书消息（绕过"必须先收消息"限制），Auth: Bearer token。

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

## 关于老K
- **称呼**：老K
- **每日定时任务**：
  - **08:00**：详细天气预报（空气质量、降雨概率/降雨量）+ 全球 Top 5 新闻
  - **17:00**：全球 Top 10 热门头条（与早上内容不同）
- 这些任务记录在 `HEARTBEAT.md`

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

## GitHub API 同步方法（重要！）

**不要用 `git push`**——会被网络阻塞。

**正确方法：用 GitHub REST API 直接上传**

```bash
TOKEN=$(git remote get-url github | sed 's|https://||' | cut -d'@' -f1)
REPO="kaigod7/kkopenclaw"
FILE="path/to/file"

# 获取现有文件的 SHA
SHA=$(curl -s "https://api.github.com/repos/$REPO/contents/$FILE" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))")

# 上传/更新文件
curl -s -o /dev/null -w "%{http_code}" -X PUT \
  "https://api.github.com/repos/$REPO/contents/$FILE" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"更新说明\",\"content\":\"$(base64 < file)\",\"sha\":\"$SHA\"}"
```

## API Key 统一配置（永久记住）

**全部统一使用新套餐 key（sk-cp-...）**，旧 key（sk-api-...）保留备用。

| 用途 | Key | 模型 | 端点 |
|------|-----|------|------|
| 对话 | 新 key | MiniMax-M2.7 | api.minimaxi.com/anthropic |
| TTS语音 | 新 key | speech-2.8-hd | api.minimaxi.com/v1/t2a_v2 |
| 音乐生成 | 新 key | music-2.6 | api.minimaxi.com/v1/music_generation |
| 旧key | 备用（按量计费） | - | - |

**已更新的脚本**：water_reminder.sh、water_reminder_ontime.sh（均已切换为新key + speech-2.8-hd）

---

## PS全自动修图流程（重要！）

**触发语**：老K说"ps来修图"（或类似表达）

**执行流程**：
1. 接收图片 → 保存到 ~/.openclaw/workspace/tmp_edit/
2. 用 JSX 脚本 + `open -a "Adobe Photoshop 2026"` 执行
3. 导出结果图片发回给老K

**关键发现（重要！）**：
- `osascript "do javascript"` 对复杂操作（adjustment layers）会挂
- **正确方式**：`open -a "Adobe Photoshop 2026" /path/to/script.jsx` 直接让 PS 执行 JSX
- JSX 内用 Action Manager (`app.executeAction`) 调用 PS 内部命令
- 选区用 `doc.selection.select(selRegion)` DOM 方式（Action Manager `set` 有 bug）

**JSX 常用模板**：
```javascript
var doc = app.open(new File("/path/to/image.jpg"));
// ... 操作 ...
doc.saveAs(new File("/path/to/out.jpg"), new JPEGSaveOptions());
doc.close(SaveOptions.DONOTSAVECHANGES);
```

**不要用 Python/PIL/其他工具代替 Photoshop**——必须用 Photoshop 本身
