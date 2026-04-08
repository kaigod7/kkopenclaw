#!/bin/bash
# OpenClaw 记忆与学习内容备份脚本
# 用法: bash scripts/backup_openclaw.sh

BACKUP_DIR="$HOME/openclaw-backup"
SRC_DIR="$HOME/.openclaw/workspace"

echo "📦 开始备份 OpenClaw 记忆和学习内容..."

mkdir -p "$BACKUP_DIR"

# 备份核心记忆文件
cp "$SRC_DIR/MEMORY.md" "$BACKUP_DIR/MEMORY.md"
cp "$SRC_DIR/TOOLS.md" "$BACKUP_DIR/TOOLS.md"
cp "$SRC_DIR/AGENTS.md" "$BACKUP_DIR/AGENTS.md"
cp "$SRC_DIR/SOUL.md" "$BACKUP_DIR/SOUL.md"
cp "$SRC_DIR/USER.md" "$BACKUP_DIR/USER.md"
cp "$SRC_DIR/IDENTITY.md" "$BACKUP_DIR/IDENTITY.md"
cp "$SRC_DIR/voice_favorites.json" "$BACKUP_DIR/voice_favorites.json"

# 备份 memory 目录
rm -rf "$BACKUP_DIR/memory"
cp -r "$SRC_DIR/memory" "$BACKUP_DIR/memory"

# 备份脚本目录
rm -rf "$BACKUP_DIR/scripts"
cp -r "$SRC_DIR/scripts" "$BACKUP_DIR/scripts"

# 备份 HEARTBEAT
cp "$SRC_DIR/HEARTBEAT.md" "$BACKUP_DIR/HEARTBEAT.md"

# Git 提交（如果有改动）
cd "$SRC_DIR" || exit
if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
    git add -A
    git commit -m "auto-backup $(date '+%Y-%m-%d %H:%M')"
    echo "✅ git 提交完成"
else
    echo "✅ 文件已备份（无 git 变动）"
fi

# 统计
echo ""
echo "📊 备份统计："
echo "  备份目录: $BACKUP_DIR"
echo "  文件大小: $(du -sh "$BACKUP_DIR" | cut -f1)"
echo "  memory 文件: $(find "$BACKUP_DIR/memory" -name "*.md" | wc -l | tr -d ' ') 个"
echo ""
echo "✅ 备份完成！备份位置: $BACKUP_DIR"
