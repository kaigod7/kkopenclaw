# Heartbeat checklist

## 每次心跳自动执行
- 运行 `bash $HOME/.openclaw/workspace/scripts/backup_openclaw.sh` 进行本地备份
- 无需询问，直接执行
- **检查OpenClaw版本**：每次心跳必须执行，发现新版本**必须发送消息通知老K**
  - 获取版本：先直连 npm，失败走代理，再失败跳过（留待下次心跳重试）
    ```bash
    latest=$(curl -s "https://registry.npmjs.org/openclaw/latest" | python3 -c "import sys,json; print(json.load(sys.stdin).get('version','failed'))")
    if [ "$latest" = "failed" ]; then
      latest=$(curl -s --proxy http://127.0.0.1:7890 "https://registry.npmjs.org/openclaw/latest" | python3 -c "import sys,json; print(json.load(sys.stdin).get('version','failed'))")
    fi
    ```
  - 如果 `latest` 仍然是 `failed`：**记日志但不通知**，下次心跳重试
  - 如果 `latest` 比当前版本 `/Users/kk/.openclaw/openclaw.json` 里的 `lastTouchedVersion` 新：
    1. 发飞书消息通知老K（直接说 "OpenClaw 新版本 xxx 已发布，是否升级？"）
    2. 更新 `meta.lastTouchedVersion` 为最新版本
    3. 记录 `meta.updateNotifiedAt` 为当前时间戳
  - 如果 `latest` 跟 `lastTouchedVersion` 一样或更旧：跳过，不通知
  - **注意**：已经通知过的版本不重复通知（靠 `updateNotifiedAt` 判断）

### 📡 定时任务触发检查
检查触发文件是否存在（由 launchd 在 08:00 写入），如有则执行对应任务：

**morning-briefing-trigger (08:00)**：
1. 获取上海天气（彩云天气 v2.6）
2. 发送飞书天气消息给老K
3. 删除触发文件

**晚间播报 (20:00)**：
1. 走 launchd 直接触发 `evening_news.sh`
2. 无需触发文件

---

## 🌅 每日 08:00 定时任务
每天早上 8:00（Asia/Shanghai）自动执行：

### 早安天气
信息来源：彩云天气 v2.6

固定格式（中文）：每次连续发送 **上海 → 悉尼** 两张卡片：
```
━━━ 📍 上海天气 ━━━
{天气} {气温}°C | 湿度 {湿度}%
风力 {风速} km/h | 风向 {风向}

━━━ 💧 未来6小时降雨 ━━━
{HH:MM} {概率}%，...
（或"未来6小时无显著降雨"）

━━━ 🌫️ 空气质量 ━━━
AQI {数值}（{等级}）
PM2.5: {值} | PM10: {值}

━━━ 🌅 日出日落 ━━━
日出 {HH:MM} | 日落 {HH:MM}
```
（紧随其后发送完全相同的悉尼版本，卡片标题为紫色）

## ☀️ 每日 12:00 定时任务
每天中午 12:00（Asia/Shanghai）自动执行：

### 中午天气
每次连续发送 **上海 → 悉尼** 两张卡片（格式同上中午版）

## 🌇 每日 16:00 定时任务
每天下午 16:00（Asia/Shanghai）自动执行：

### 下午天气
每次连续发送 **上海 → 悉尼** 两张卡片（格式同上下午版）

## 🌙 每日 20:00 定时任务
每天晚上 20:00（Asia/Shanghai）自动执行：

### 晚安天气
每次连续发送 **上海 → 悉尼** 两张卡片（晚安版含4段降雨预报）

---

## 🌍 每日 Sydney 播报（KK2 独立发送，按悉尼当地时间）

**当前时区**：AEST（冬令时 UTC+10，上海比悉尼快2小时）

| 悉尼时间 | 上海触发时间 | 时差 |
|---------|------------|------|
| 06:00 | 03:00 | +2h |
| 10:00 | 07:00 | +2h |
| 14:00 | 12:00 | +2h |
| 18:00 | 17:00 | +2h |

**夏令时（AEDT UTC+11）**：10月第一个周日 ~ 4月第一个周日，上海比悉尼快3小时，plists 自动切换 Hour 值。

Sydney 播报均为**独立卡片**（紫色/indigo），格式同上海版本。
---

## ⚠️ 版本更新检查
已升级为每次心跳自动检查（见上方「每次心跳自动执行」）。

---

## 💧 水分提醒（已暂停）
- launchd：`com.openclaw.water-reminder`（每60秒触发）
- **当前状态：已停止**
- K 说「开始」后才重新启动

## 📚 学习进度汇报机制
当老K说"学习"时：
1. 在 HEARTBEAT.md 中标记学习任务（状态：进行中）
2. 启动 `com.openclaw.learning-check` launchd（每60秒检查一次）
3. 每隔约5分钟通过 heartbeat 机制发送进度汇报

当老K说"停止学习"时：
1. 更新 HEARTBEAT.md 中的学习状态为"已停止"
2. launchd 会自动停止发送汇报

---
## 🔥 当前学习任务
**主题**：Photoshop 全版本修图技巧（最新 v27.5）
**开始时间**：2026-04-10 09:55
**状态**：已停止
**汇报间隔**：每10分钟
**目标**：全网搜索PS2026干货技巧、热门修图博主参数心得
**下次汇报时间**：~10:00

---

## 版本速查表位置
`memory/photo-editing-study.md` 顶部
