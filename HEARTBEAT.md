# Heartbeat checklist

## 每次心跳自动执行
- 运行 `bash $HOME/.openclaw/workspace/scripts/backup_openclaw.sh` 进行本地备份
- 本地备份路径：`~/openclaw-backup/`
- 无需询问，直接执行

## GitHub 备份
- GitHub 备份由 launchd 定时任务在每天下午 16:00 自动执行（推送到 github.com/kaigod7/kkopenclaw）
- 脚本：`~/Library/LaunchAgents/com.openclaw.backup-github.plist`
