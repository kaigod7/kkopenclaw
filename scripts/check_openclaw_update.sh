#!/bin/bash
# OpenClaw 版本更新检查 + 飞书推送
# 每次 heartbeat 调用

set -e

CONFIG="/Users/kk/.openclaw/openclaw.json"
LOG_FILE="/tmp/openclaw-update-check.log"

# 飞书 Bot 凭证（KK龙虾1号）
APP_ID="cli_a9458c4ee4f99bc0"
APP_SECRET="YDR6M7PifC1w1eW47bt7sdUdBCWxEBXE"

# 飞书目标：老K的 open_id
TARGET_USER="ou_5db13b27b4a70dde91c409d35ac16bb1"

# 获取当前记录的版本
CURRENT_VERSION="$(python3 -c "import json; print(json.load(open('$CONFIG')).get('meta',{}).get('lastTouchedVersion','unknown'))")"

# 获取 npm 最新版本
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking npm..." >> "$LOG_FILE"
LATEST="$(curl -s --max-time 10 "https://registry.npmjs.org/openclaw/latest" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('version','failed'))")"

if [ "$LATEST" = "failed" ]; then
    # 走代理重试
    LATEST="$(curl -s --max-time 10 --proxy http://127.0.0.1:7890 "https://registry.npmjs.org/openclaw/latest" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('version','failed'))")"
fi

if [ "$LATEST" = "failed" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Failed to fetch version from npm" >> "$LOG_FILE"
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Current: $CURRENT_VERSION, Latest: $LATEST" >> "$LOG_FILE"

# 版本对比
if [ "$LATEST" = "$CURRENT_VERSION" ]; then
    exit 0
fi

# 有新版本！获取 release 链接
RELEASE_INFO="$(curl -s --max-time 10 "https://api.github.com/repos/openclaw/openclaw/releases/latest" 2>/dev/null)"
RELEASE_URL="$(echo "$RELEASE_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin).get('html_url','https://github.com/openclaw/openclaw/releases'))")"

# 获取飞书 tenant_access_token
TOKEN_RESP="$(curl -s --max-time 10 -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}" 2>/dev/null)"

TENANT_TOKEN="$(echo "$TOKEN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")"

if [ -z "$TENANT_TOKEN" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Failed to get Feishu token" >> "$LOG_FILE"
    exit 1
fi

# 构建并发送飞书消息（简洁版）
echo "[$(date '+%Y-%m-%d %H:%M:%S')] New version detected, sending notification..." >> "$LOG_FILE"

MESSAGE="🚀 **OpenClaw 新版本发布**

**当前版本：** $CURRENT_VERSION
**最新版本：** $LATEST

[查看更新说明]($RELEASE_URL)

是否升级？"

# 用 Python 处理 JSON 转义并发送
RESPONSE="$(python3 -c "
import json, urllib.request

message = '''$MESSAGE'''
token = '$TENANT_TOKEN'
target = '$TARGET_USER'

payload = json.dumps({
    'receive_id': target,
    'content': json.dumps({'text': message}),
    'msg_type': 'text'
}).encode('utf-8')

req = urllib.request.Request(
    'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
    data=payload,
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        print(resp.read().decode('utf-8'))
except Exception as e:
    print(f'{\"error\": \"{str(e)}\"}')
")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Feishu response: $RESPONSE" >> "$LOG_FILE"

# 更新 lastTouchedVersion，避免重复通知
python3 -c "
import json
with open('$CONFIG', 'r') as f:
    config = json.load(f)
if 'meta' not in config:
    config['meta'] = {}
config['meta']['lastTouchedVersion'] = '$LATEST'
config['meta']['updateNotifiedAt'] = '$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'
with open('$CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Updated lastTouchedVersion to $LATEST" >> "$LOG_FILE"