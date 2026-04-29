# MEMORY.md - Long-Term Memory

## 音乐生成 API（MiniMax music-2.6）

**重要发现（2026-04-20）：**
- `music-2.6` 必须带 `lyrics` 参数才能调用成功（API 返回 `lyrics is required`）
- OpenClaw 内置 `music_generate` 工具调用时未传 `lyrics`，导致一直失败
- **正确调用方式**：直接用 curl 调 MiniMax API，带 `lyrics` 参数
- 端点：`POST https://api.minimaxi.com/v1/music_generation`
- 模型：`music-2.6`
- 返回格式：`{"data":{"audio":"<hex>"}}`，需用 `bytes.fromhex()` 解码

**正确请求格式：**
```python
data = {
    "model": "music-2.6",
    "prompt": "描述",
    "lyrics": "[verse]\n歌词内容...",
    "duration": 240
}
```

## TTS 语音（MiniMax）

**MiniMax TTS 返回字段：** `result["data"]["audio"]` 不是 `audio_data`！

**默认音色：** MiniMax `Chinese (Mandarin)_Soft_Girl`（音色表1号「柔软女孩」）

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
- **每日定时任务**（记录在 `HEARTBEAT.md`）：
  - **08:00** 上海天气卡片（蓝）+ 悉尼天气卡片（蓝）
  - **12:00** 上海天气卡片（黄）+ 悉尼天气卡片（黄）
  - **16:00** 上海天气卡片（橙）+ 悉尼天气卡片（橙）
  - **20:00** 上海天气卡片（紫）+ 悉尼天气卡片（紫）
- 悉尼播报按悉尼本地时间触发（AEST UTC+10 / AEDT UTC+11），上海比悉尼快 2h（冬令时）/ 3h（夏令时）

## ⛈️ 天气数据降级经验（2026-04-27）

**核心教訓**：天氣 API 多級降級不能只保證「能拿到數據」，還要保證每級回傳的數據**結構和格式一致**。否則卡片端（build_card/build_evening_card）會因為字段類型/範圍不同而解析失敗。

**解決方案**：
- 寫了 `scripts/weather_lib.py` 統一處理天氣獲取，三級降級（彩雲→QWeather→Open-Meteo）
- 每級 API 返回的數據都在 lib 內轉換成標準格式，卡片構建邏輯不關心數據源
- AQI 也獨立從 Open-Meteo 補上（QWeather 免費版無 AQI）

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

## 天气数据源（彩云天气 v2.6）

**天气来源**：彩云天气 v2.6 API（稳定，包含空气质量）
**API Token**：`z7AhM2I98ZFxUt2c`
**数据**：实时天气 + 空气质量(AQI/PM2.5/PM10) + 逐小时降雨概率
**上海坐标**：121.47, 31.23 | **悉尼坐标**：151.2093, -33.8688
**备用降级**：和风 QWeather → Open-Meteo

数据获取统一由 `scripts/weather_lib.py` 处理（三级降级，输出标准格式）

**脚本位置**：
- `scripts/kk2/morning_briefing.sh`（上海 08:00）
- `scripts/kk2/noon_briefing.sh`（上海 12:00）
- `scripts/kk2/afternoon_briefing.sh`（上海 16:00）
- `scripts/kk2/evening_news.sh`（上海 20:00）
- `scripts/kk2/sydney_morning.sh` / `sydney_noon.sh` / `sydney_afternoon.sh` / `sydney_evening.sh`（按悉尼当地时间）

注意：彩云天气对悉尼不提供 AQI，悉尼空气质量用 Open-Meteo 补充。



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

### Tavily 新闻搜索

**两个独立账号，各1000免费credits/月：**
- **旧 key（GitHub 账号）**：`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` — 优先使用
- **新 key（Google 账号）**：`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` — 备用

**脚本 fallback 逻辑**：优先用旧 key，失败后自动切换新 key。

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


## 语言偏好
- **定时发送的天气播报（08:00/12:00/16:00/20:00）必须用中文**
- **时间格式：全部用 24 小时制**（如 08:00、14:30、23:45），不用 AM/PM

## 飞书群聊回复规则（永久记住）
- **群聊核心规则**：不 @ 我，我不读取、不分析、不回复。被 @ 才响应。
- **图片同理**：没 @ 不看图，等 @ 了再看图回复。
- **其他人消息**：不读、不分析、不回复，跟我无关。
- 这条规则已同时写入 AGENTS.md，两份永久生效。

## 飞书 Bot 凭证（2026-04-29 更新）

| Bot | App ID | App Secret | Bot open_id |
|-----|--------|------------|-------------|
| KK龙虾1号（OpenClaw KK1） | `cli_a9458c4ee4f99bc0` | `YDR6M7PifC1w1eW47bt7sdUdBCWxEBXE` | `ou_c3399de7218a32f213b200fda6675f79` |
| 红袍大将军（OpenClaw KK2） | `cli_a96f0a89bf795bb5` | `0qZOvpMy676geoq5w2h6neZgLk2Jhy04` | `ou_5e9fcfd9a3512896146c74266688a545` |
| KK爱马仕1号（Hermes） | `cli_a95590b738781bd3` | `VHtAIix2UUJ4xDFD5nEWIdBGbKJ3yd6S` | `ou_cbf0f609ad717b11fd951a1245f0f41a` |

## OpenClaw ↔ Hermes 联动（传声筒模式）

**目标**：在群里 Hermes @ 我（@KK龙虾1号）时，OpenClaw 能收到并回复；我 @ Hermes（@KK爱马仕1号）时，Hermes 能收到并回复。

**触发词**：@对方机器人名字（KK龙虾1号 ↔ KK爱马仕1号）

**Relay 脚本**：`~/.openclaw/workspace/scripts/feishu_relay.py`
- 监听 Hermes app 的群消息 API
- 检测到 @KK龙虾1号 → 转发给 OpenClaw 处理
- OpenClaw 回复 → 通过 Hermes API 发回群

**状态**：脚本已就绪，Gateway token 未配置（待解决）

## 新增 Skill（2026-04-29）

**neat-freak（洁癖）** — 来自 [khazix-skills](https://github.com/KKKKhazix/khazix-skills)
- 安装位置：`~/.openclaw/skills/neat-freak/`
- 触发词：`整理一下`、`同步一下`、`/neat`
- 功能：会话结束后自动对齐项目文档、AGENTS.md、记忆系统，防止「脑腐化」


