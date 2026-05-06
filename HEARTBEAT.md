# Heartbeat checklist

## 每次心跳自动执行
- 运行 `bash $HOME/.openclaw/workspace/scripts/backup_openclaw.sh` 进行本地备份
- **检查 OpenClaw 版本更新**：运行 `bash $HOME/.openclaw/workspace/scripts/check_openclaw_update.sh`
  - 有新版本时通过 Gateway API 发飞书私聊通知老K（带 changelog）
  - 已通知过的版本不重复通知（自动更新 `lastTouchedVersion`）
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
（已停用 — 天气播报已关闭）

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
