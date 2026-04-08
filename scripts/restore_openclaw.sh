#!/bin/bash
# OpenClaw 记忆与学习内容恢复脚本
# 用法: bash scripts/restore_openclaw.sh

BACKUP_DIR="$HOME/openclaw-backup"
DEST_DIR="$HOME/.openclaw/workspace"

if [[ ! -d "$BACKUP_DIR" ]]; then
    echo "❌ 备份目录不存在: $BACKUP_DIR"
    echo "请先运行 backup_openclaw.sh"
    exit 1
fi

echo "🔄 开始从备份恢复..."

# 检查 workspace 是否存在
if [[ ! -d "$DEST_DIR" ]]; then
    echo "❌ Workspace 目录不存在，请先安装 OpenClaw"
    exit 1
fi

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
