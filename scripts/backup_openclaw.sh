#!/bin/bash
# OpenClaw 记忆与学习内容备份脚本
# 用法:
#   bash scripts/backup_openclaw.sh           # 本地备份（心跳调用）
#   bash scripts/backup_openclaw.sh github    # 本地 + GitHub 推送（定时任务调用）

MODE="${1:-local}"
BACKUP_DIR="$HOME/openclaw-backup"
SRC_DIR="$HOME/.openclaw/workspace"
GITHUB_MARKER="$BACKUP_DIR/.github_pushed_today"

echo "📦 开始备份 [模式: $MODE] ..."
mkdir -p "$BACKUP_DIR"

# 本地备份
cp "$SRC_DIR/MEMORY.md" "$BACKUP_DIR/MEMORY.md"
cp "$SRC_DIR/TOOLS.md" "$BACKUP_DIR/TOOLS.md"
cp "$SRC_DIR/AGENTS.md" "$BACKUP_DIR/AGENTS.md"
cp "$SRC_DIR/SOUL.md" "$BACKUP_DIR/SOUL.md"
cp "$SRC_DIR/USER.md" "$BACKUP_DIR/USER.md"
cp "$SRC_DIR/IDENTITY.md" "$BACKUP_DIR/IDENTITY.md"
cp "$SRC_DIR/voice_favorites.json" "$BACKUP_DIR/voice_favorites.json" 2>/dev/null || true

rm -rf "$BACKUP_DIR/memory"
cp -r "$SRC_DIR/memory" "$BACKUP_DIR/memory"

rm -rf "$BACKUP_DIR/scripts"
cp -r "$SRC_DIR/scripts" "$BACKUP_DIR/scripts"

cp "$SRC_DIR/HEARTBEAT.md" "$BACKUP_DIR/HEARTBEAT.md"

# Git 提交（在 workspace 目录操作）
cd "$SRC_DIR" || exit
if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
    git add -A
    git commit -m "auto-backup $(date '+%Y-%m-%d %H:%M')"
    echo "✅ git 提交完成"
else
    echo "✅ 文件已备份（无 git 变动）"
fi

# GitHub 推送（仅 github 模式）
if [[ "$MODE" == "github" ]]; then
    TOKEN=$(cat "$SRC_DIR/.gh-token" 2>/dev/null | grep -v '^#' | tr -d ' \n')
    if [[ -n "$TOKEN" ]]; then
        git remote set-url github "https://${TOKEN}@github.com/kaigod7/kkopenclaw.git"
        echo "📤 推送到 GitHub ..."
        git -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 push github main --force 2>&1 && echo "✅ GitHub 推送完成" || echo "⚠️ GitHub 推送失败"
        touch "$GITHUB_MARKER"
        echo "📌 GitHub 今日标记已创建"
    else
        echo "⚠️ 未找到 GitHub token（.gh-token 文件）"
    fi
fi

# 统计
echo ""
echo "📊 备份统计："
echo "  备份目录: $BACKUP_DIR"
echo "  文件大小: $(du -sh "$BACKUP_DIR" | cut -f1)"
echo "  memory 文件: $(find "$BACKUP_DIR/memory" -name "*.md" | wc -l | tr -d ' ') 个"
echo ""
echo "✅ 备份完成！"
