# Heartbeat checklist

## 每次心跳自动执行
- 运行 `bash $HOME/.openclaw/workspace/scripts/backup_openclaw.sh` 进行本地备份
- 无需询问，直接执行

### 📡 定时任务触发检查
检查触发文件是否存在（由 launchd 在 08:00/17:00 写入），如有则执行对应任务：

**morning-briefing-trigger (08:00)**：
1. 获取上海天气（wttr.in 或 tavily）
2. tavily 搜索全球 Top 5 新闻
3. 整合发送飞书消息给老K
4. 删除触发文件

**evening-news-trigger (17:00)**：
1. tavily 搜索全球 Top 10 新闻
2. 发送飞书消息给老K
3. 删除触发文件

---

## 🌅 每日 08:00 定时任务
每天早上 8:00（Asia/Shanghai）自动执行：

### 天气预报（详细版）
包括：
- 当天整体天气状况（温度范围、天气类型）
- 空气质量（AQI、PM2.5、PM10）
- 未来时段（当天每小时/每3小时）降雨概率和预计降雨量
- 体感温度、风力风向、湿度
- 日出日落时间

信息来源：weather skill 或 tavily 搜索

### 全球头条新闻（Top 5）
每天早上最热门的5条全球重要新闻
信息来源：tavily 搜索

---

## 🌆 每日 17:00 定时任务
每天下午 17:00（Asia/Shanghai）自动执行：

### 全球头条新闻（Top 10）
当天最新的10条热门头条（与早上不同的内容）
信息来源：tavily 搜索

---

## ⚠️ 每周检查更新（每周一执行）
每逢周一检查：

```bash
python3 --version
pip3 list --outdated
brew list darktable --versions
```

---

## 💧 水分提醒（独立运行）
每分钟发一次语音："起来喝点水啦～"
- launchd：`com.openclaw.water-reminder`（每60秒触发）
- **独立运行，不受学习状态控制**
- 要停止只能说"停止水分提醒"

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
**状态**：进行中
**汇报间隔**：每5分钟
**目标**：全网搜索PS2026干货技巧、热门修图博主参数心得
**下次汇报时间**：~10:00

---

## 版本速查表位置
`memory/photo-editing-study.md` 顶部
