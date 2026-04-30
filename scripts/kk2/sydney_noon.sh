#!/bin/bash
# 悉尼 午间天气 (悉尼 12:00 / 上海 10:00)

cd "$HOME/.openclaw/workspace/scripts/kk2"
python3 weather_card.py --city sydney --slot noon
