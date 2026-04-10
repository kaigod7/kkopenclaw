#!/bin/bash
# 每日晚间新闻 (17:00) - 通过 Feishu API 发送
# 全球 Top 10 新闻

python3 << 'PYEOF'
import json, os, urllib.request

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LOG = os.path.join(WORKSPACE, "memory/evening-news.log")

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"[{os.popen('date').read().strip()}] {msg}\n")

log("=== 晚间新闻开始 ===")

# ── 通过 tavily 搜索新闻 ──
news_text = ""
try:
    import subprocess
    result = subprocess.run([
        "python3", "-c", """
import urllib.request, json
url = "https://api.tavily.com/search"
data = json.dumps({
    "query": "今日全球重大新闻 2026年4月10日",
    "max_results": 10,
    "search_depth": "basic",
    "topic": "news"
}).encode()
req = urllib.request.Request(url, data=data,
    headers={"Content-Type": "application/json", "Authorization": "Bearer atb-4254-afj2bkc74b0c5e4c6d3e9d6f7g8h9i0j"},
    method="POST")
with urllib.request.urlopen(req, timeout=15) as r:
    resp = json.loads(r.read())
for i, r in enumerate(resp.get("results", [])[:10], 1):
    print(f"{i}. {r.get('title', '')[:80]}")
"""], capture_output=True, text=True, timeout=20)
    news_text = result.stdout.strip()
    log(f"搜索结果: {len(news_text)} 字符")
except Exception as e:
    log(f"搜索错误: {e}")

# ── 发送飞书 ──
try:
    with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
        cfg = json.load(f)
    feishu = cfg["channels"]["feishu"]

    FEISHU_API = "https://open.feishu.cn/open-apis"
    OPEN_ID = "ou_5db13b27b4a70dde91c409d35ac16bb1"

    data = json.dumps({"app_id": feishu["appId"], "app_secret": feishu["appSecret"]}).encode()
    req = urllib.request.Request(
        f"{FEISHU_API}/auth/v3/tenant_access_token/internal",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        token = json.loads(r.read())["tenant_access_token"]

    if news_text:
        msg = f"🌆 今日晚间新闻 Top 10\n\n{news_text}"
    else:
        msg = "🌆 今日晚间新闻\n（新闻获取失败，请手动查看 BBC/RFI）"

    body = json.dumps({
        "receive_id": OPEN_ID,
        "msg_type": "text",
        "content": json.dumps({"text": msg})
    }).encode()

    req = urllib.request.Request(
        f"{FEISHU_API}/im/v1/messages?receive_id_type=open_id",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        result = json.loads(r.read())

    if result.get("code") == 0:
        log(f"发送成功: {result['data']['message_id']}")
        print(f"SEND_OK: {result['data']['message_id']}")
    else:
        log(f"发送失败: {result}")
except Exception as e:
    log(f"Feishu错误: {e}")
    print(f"ERROR: {e}")

log("=== 完成 ===")
PYEOF