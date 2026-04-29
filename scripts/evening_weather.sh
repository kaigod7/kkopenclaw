#!/bin/bash
# 晚间天气播报 (20:00) - 纯天气，无新闻

WORKSPACE="$HOME/.openclaw/workspace"
LOG="$WORKSPACE/memory/evening-weather.log"

echo "[$(date '+%Y-%m-%d %H:%M')] === 晚间天气播报开始 ===" >> "$LOG"

python3 "$WORKSPACE/scripts/evening_weather.py" 2>&1 | tee -a "$LOG"
