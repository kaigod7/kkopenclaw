#!/bin/bash
# ⚠️  OpenClaw 记忆与文件恢复脚本（谨慎使用！）
# 用法: bash scripts/restore_openclaw.sh
#
# 此脚本会从备份目录覆盖 workspace 的全部文件。
# 如果备份是旧版本，会导致近期修改丢失。
# 仅应在 workspace 严重损坏时使用。

BACKUP_DIR="$HOME/openclaw-backup"
DEST_DIR="$HOME/.openclaw/workspace"

if [[ ! -d "$BACKUP_DIR" ]]; then
    echo "❌ 备份目录不存在: $BACKUP_DIR"
    echo "请先运行 backup_openclaw.sh"
    exit 1
fi

echo ""
echo "⚠️⚠️⚠️  警告！ ⚠️⚠️⚠️"
echo "此操作会用备份覆盖以下内容："
echo "  - MEMORY.md"
echo "  - AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md"
echo "  - memory/ 目录（所有学习笔记）"
echo "  - scripts/ 目录（所有脚本）"
echo "  - HEARTBEAT.md"
echo ""
echo "如果备份不是最新版本，近期修改将丢失！"
echo ""

# 检查备份新鲜度
BACKUP_TIME=$(stat -f "%Sm" "$BACKUP_DIR/MEMORY.md" 2>/dev/null || echo "未知")
echo "📅 备份时间: $BACKUP_TIME"
echo ""

read -p "确认恢复？(输入 yes 继续): " CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
    echo "❌ 已取消"
    exit 0
fi

# 检查 workspace 是否存在
if [[ ! -d "$DEST_DIR" ]]; then
    echo "❌ Workspace 目录不存在，请先安装 OpenClaw"
    exit 1
fi

echo "🔄 开始从备份恢复..."

# 恢复核心文件
cp -f "$BACKUP_DIR/MEMORY.md" "$DEST_DIR/MEMORY.md"
cp -f "$BACKUP_DIR/TOOLS.md" "$DEST_DIR/TOOLS.md"
cp -f "$BACKUP_DIR/AGENTS.md" "$DEST_DIR/AGENTS.md"
cp -f "$BACKUP_DIR/SOUL.md" "$DEST_DIR/SOUL.md"
cp -f "$BACKUP_DIR/USER.md" "$DEST_DIR/USER.md"
cp -f "$BACKUP_DIR/IDENTITY.md" "$DEST_DIR/IDENTITY.md"
cp -f "$BACKUP_DIR/voice_favorites.json" "$DEST_DIR/voice_favorites.json"

# 恢复 memory 目录
rm -rf "$DEST_DIR/memory"
cp -r "$BACKUP_DIR/memory" "$DEST_DIR/memory"

# 恢复脚本目录
rm -rf "$DEST_DIR/scripts"
cp -r "$BACKUP_DIR/scripts" "$DEST_DIR/scripts"

# 恢复 HEARTBEAT
cp -f "$BACKUP_DIR/HEARTBEAT.md" "$DEST_DIR/HEARTBEAT.md"

echo "✅ 恢复完成！"
echo ""
echo "📋 已恢复的内容："
echo "  MEMORY.md"
echo "  memory/ (学习笔记: darktable-tips, python-photo-editing 等)"
echo "  TOOLS.md, AGENTS.md, SOUL.md, USER.md, IDENTITY.md"
echo "  voice_favorites.json"
echo "  scripts/ (备份和恢复脚本)"
echo ""
echo "⚠️  恢复后建议重启 OpenClaw 使改动生效"
