#!/usr/bin/env python3
"""
KK1 天气播报 — 发老K私聊，仅上海
用法：
  python3 weather_card.py morning    # 蓝
  python3 weather_card.py noon       # 黄
  python3 weather_card.py afternoon  # 橙
  python3 weather_card.py evening    # 紫
"""

import json, urllib.request, time, os, sys

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LOG_FILE = os.path.join(WORKSPACE, "memory/kk1-weather.log")

CAIYUN_TOKEN = "z7AhM2I98ZFxUt2c"

# ⏰ 武汉临时坐标（4月29日 ~ 5月4日 20:00）
# 到期后自动切回上海
from datetime import datetime as _dt
_now = _dt.now()
_deadline = _dt(2026, 5, 4, 19, 59)  # 5月4日20:00前用武汉
if _now < _deadline:
    LOC = "114.3055,30.5928"
    CITY_NAME = "武汉"
    print("📍 使用武汉坐标（临时）")
else:
    LOC = "121.47,31.23"
    CITY_NAME = "上海"
    print("📍 已切回上海坐标")
print(f"📅 当前时间：{_now.strftime('%Y-%m-%d %H:%M')}，截止：{_deadline.strftime('%Y-%m-%d %H:%M')}")

SLOT_CFG = {
    "morning":   {"emoji": "🌅", "title": "早安",   "color": "blue"},
    "noon":      {"emoji": "☀️", "title": "中午",    "color": "yellow"},
    "afternoon": {"emoji": "🌤️", "title": "下午",    "color": "orange"},
    "evening":   {"emoji": "🌙", "title": "晚安",    "color": "purple"},
}

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M')}] {msg}\n")

def to_emoji_time(t):
    dmap = {"0":"0️⃣","1":"1️⃣","2":"2️⃣","3":"3️⃣","4":"4️⃣",
            "5":"5️⃣","6":"6️⃣","7":"7️⃣","8":"8️⃣","9":"9️⃣",":":":"}
    return "".join(dmap.get(c, c) for c in t)

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SLOT_CFG:
        print("用法: python3 weather_card.py <morning|noon|afternoon|evening>")
        sys.exit(1)

    slot = sys.argv[1]
    cfg = SLOT_CFG[slot]

    log(f"=== {slot} {CITY_NAME} 天气开始 ===")

    # ── 获取天气 ──
    try:
        url = f"https://api.caiyunapp.com/v2.6/{CAIYUN_TOKEN}/{LOC}/weather"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        log(f"❌ 天气获取失败：{e}")
        sys.exit(1)

    result = data.get("result", {})
    rt = result.get("realtime", {})
    daily = result.get("daily", {})
    hp = result.get("hourly", {}).get("precipitation", [])
    hs = result.get("hourly", {}).get("skycon", [])

    temp = rt.get("temperature", "?")
    skycon = rt.get("skycon", "?")
    humidity = rt.get("humidity", 0)
    wind = rt.get("wind", {})
    aqi = rt.get("air_quality", {})

    sk = {"CLEAR_DAY":"晴","CLEAR_NIGHT":"晴","PARTLY_CLOUDY_DAY":"多云",
          "PARTLY_CLOUDY_NIGHT":"多云","CLOUDY":"阴","RAIN":"雨",
          "LIGHT_RAIN":"小雨","MODERATE_RAIN":"中雨","HEAVY_RAIN":"大雨",
          "SNOW":"雪","WIND":"风","FOG":"雾","HAZE":"霾"}
    sk_emoji = {"CLEAR_DAY":"☀️","CLEAR_NIGHT":"🌙","PARTLY_CLOUDY_DAY":"⛅",
                "PARTLY_CLOUDY_NIGHT":"☁️","CLOUDY":"☁️","RAIN":"🌧️",
                "LIGHT_RAIN":"🌧️","MODERATE_RAIN":"🌧️","HEAVY_RAIN":"🌧️",
                "SNOW":"❄️","WIND":"💨","FOG":"🌫️","HAZE":"🌫️"}

    weather = sk.get(skycon, "?")
    hum_pct = int(float(humidity) * 100)
    ws = wind.get("speed", 0)
    wd = wind.get("direction", 0)
    dirs = ["北","东北","东","东南","南","西南","西","西北"]

    aqi_val = aqi.get("aqi", {}).get("chn", "?")
    pm25 = aqi.get("pm25", "?")
    pm10 = aqi.get("pm10", "?")

    astro = daily.get("astro", [{}])[0] if daily.get("astro") else {}
    sunrise = astro.get("sunrise", {}).get("time", "--:--")
    sunset = astro.get("sunset", {}).get("time", "--:--")

    smap = {}
    for s in hs or []:
        smap[s["datetime"][11:16]] = s["value"]

    rain_lines = []
    for h in (hp or [])[:6]:
        dt = h.get("datetime", "")
        prob = h.get("probability", 0)
        if isinstance(prob, (int, float)) and len(dt) >= 13:
            t = dt[11:16]; p = int(prob)
            e = sk_emoji.get(smap.get(t, "🌙"), "🌙")
            rain_lines.append(f"{to_emoji_time(t)} │ {e}" + (f" │ {p}%" if p > 0 else ""))

    rf = "\n".join(rain_lines) if rain_lines else "未来6小时无显著降雨"
    log(f"天气获取成功：{temp}°C {skycon}")

    # ── 构建卡片 ──
    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 📍 {CITY_NAME}天气 ━━━**"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"{weather} {temp}°C | 湿度 {hum_pct}%"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"风力 {ws} km/h | 风向 {dirs[int(wd/45)%8] if wd else '?'}"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 🌫️ 空气质量 ━━━**"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"AQI {aqi_val}  PM2.5: {pm25} | PM10: {pm10}"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 💧 未来6小时天气 ━━━**"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"{rf}"}},
    ]
    if slot in ("morning", "evening"):
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 🌅 日出日落 ━━━**"}})
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"日出 {sunrise} | 日落 {sunset}"}})

    card = {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": f"{cfg['emoji']} {cfg['title']}！ {time.strftime('%Y年%m月%d日')} {CITY_NAME}天气"}, "template": cfg["color"]},
        "elements": elements
    }

    # ── 通过 KK1 的 Feishu bot 发私聊 ──
    APP_ID = "cli_a9458c4ee4f99bc0"
    APP_SECRET = "YDR6M7PifC1w1eW47bt7sdUdBCWxEBXE"
    USER_OPEN_ID = "ou_5db13b27b4a70dde91c409d35ac16bb1"

    try:
        auth = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
        req = urllib.request.Request(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            data=auth, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            token = json.loads(resp.read())["tenant_access_token"]

        msg = json.dumps({
            "receive_id": USER_OPEN_ID,
            "msg_type": "interactive",
            "content": json.dumps(card)
        }).encode()

        req = urllib.request.Request(
            "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
            data=msg,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            r = json.loads(resp.read())
            if r.get("code") == 0:
                log("✅ 私聊卡片发送成功")
            else:
                log(f"⚠️ 失败：{r.get('msg','')}")
    except Exception as e:
        log(f"❌ 发送异常：{e}")
        sys.exit(1)

    log(f"=== 完成 ({CITY_NAME}) ===")

    # 如果到期切回上海，写一条日志提醒
    if CITY_NAME == "上海" and _now.date() >= _dt(2026, 5, 4).date():
        log("📌 武汉临时天气已到期，自动切回上海")

if __name__ == "__main__":
    main()
