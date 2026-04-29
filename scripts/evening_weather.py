#!/usr/bin/env python3
"""晚间天气播报 (20:00) — 纯天气，无新闻"""

import json, urllib.request, time, os, sys

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LOG_FILE = os.path.join(WORKSPACE, "memory/evening-weather.log")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M')}] {msg}\n")

log("=== 晚间天气开始 ===")

def to_emoji_time(t):
    """12:00 → 1️⃣2️⃣:0️⃣0️⃣"""
    dmap = {"0":"0️⃣","1":"1️⃣","2":"2️⃣","3":"3️⃣","4":"4️⃣",
            "5":"5️⃣","6":"6️⃣","7":"7️⃣","8":"8️⃣","9":"9️⃣",":":"："}
    return "".join(dmap.get(c, c) for c in t)

# ── 1. 获取天气数据（彩云天气 v2.6）──
CAIYUN_TOKEN = "z7AhM2I98ZFxUt2c"
# ⏰ 临时改到武汉：2026-04-29 ~ 2026-05-04（5月4日晚间恢复上海）
SH_LOC = "114.3055,30.5928"
CITY_NAME = "武汉"

try:
    url = f"https://api.caiyunapp.com/v2.6/{CAIYUN_TOKEN}/{SH_LOC}/weather"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    result = data.get("result", {})
    realtime = result.get("realtime", {})
    daily = result.get("daily", {})
    hourly_precip = result.get("hourly", {}).get("precipitation", [])
    hourly_skycon = result.get("hourly", {}).get("skycon", [])

    temp = realtime.get("temperature", "?")
    skycon = realtime.get("skycon", "?")
    humidity = realtime.get("humidity", 0)
    wind = realtime.get("wind", {})
    aqi = realtime.get("air_quality", {})

    skycn = {"CLEAR_DAY":"晴","CLEAR_NIGHT":"晴","PARTLY_CLOUDY_DAY":"多云","PARTLY_CLOUDY_NIGHT":"多云",
             "CLOUDY":"阴","RAIN":"雨","LIGHT_RAIN":"小雨","MODERATE_RAIN":"中雨",
             "HEAVY_RAIN":"大雨","SNOW":"雪","WIND":"风","FOG":"雾","HAZE":"霾"}

    skycn_emoji = {"CLEAR_DAY":"☀️","CLEAR_NIGHT":"🌙","PARTLY_CLOUDY_DAY":"⛅","PARTLY_CLOUDY_NIGHT":"☁️",
                   "CLOUDY":"☁️","RAIN":"🌧️","LIGHT_RAIN":"🌧️","MODERATE_RAIN":"🌧️",
                   "HEAVY_RAIN":"🌧️","SNOW":"❄️","WIND":"💨","FOG":"🌫️","HAZE":"🌫️"}

    weather_text = skycn.get(skycon, "?")
    humidity_pct = int(float(humidity) * 100)
    wind_speed = wind.get("speed", 0)
    wind_dir = wind.get("direction", 0)
    dirs = ["北","东北","东","东南","南","西南","西","西北"]

    # AQI
    aqi_val = aqi.get("aqi", {}).get("chn", "?")
    pm25 = aqi.get("pm25", "?")
    pm10 = aqi.get("pm10", "?")
    aqi_desc = aqi.get("description", {}).get("chn", "")

    # 日出日落
    astro = daily.get("astro", [{}])[0] if daily.get("astro") else {}
    sunrise = astro.get("sunrise", {}).get("time", "--:--")
    sunset = astro.get("sunset", {}).get("time", "--:--")

    # 时间→天气映射
    skycon_map = {}
    for s in hourly_skycon or []:
        skycon_map[s["datetime"][11:16]] = s["value"]

    # 逐小时预报
    rain_lines = []
    for h in (hourly_precip or [])[:6]:
        dt = h.get("datetime", "")
        prob = h.get("probability", 0)
        if isinstance(prob, (int, float)) and len(dt) >= 13:
            t = dt[11:16]
            p = int(prob)
            sk_emoji = skycn_emoji.get(skycon_map.get(t, "CLEAR_NIGHT"), "🌙")
            rain_lines.append(f"{to_emoji_time(t)} │ {sk_emoji}" + (f" │ {p}%" if p > 0 else ""))

    rain_formatted = "\n".join(rain_lines) if rain_lines else "未来6小时无显著降雨"
    log(f"天气获取成功：{temp}°C {skycon}")
except Exception as e:
    log(f"天气获取失败：{e}")
    sys.exit(1)

# ── 2. 构建消息（匹配卡片格式）──
card_text = f"""**━━━ 📍 {CITY_NAME}当前天气 ━━━**
{weather_text} {temp}°C | 湿度 {humidity_pct}%
风力 {wind_speed} km/h | 风向 {dirs[int(wind_dir/45)%8] if wind_dir else "?"}

**━━━ 💧 未来6小时天气 ━━━**
{rain_formatted}

**━━━ 🌫️ 空气质量 ━━━**
AQI {aqi_val}（{aqi_desc}）
PM2.5: {pm25} | PM10: {pm10}

**━━━ 🌅 日出日落 ━━━**
日出 {sunrise} | 日落 {sunset}"""

# ── 3. 通过 Feishu API 发送 ──
APP_ID = "cli_a9458c4ee4f99bc0"
APP_SECRET = "YDR6M7PifC1w1eW47bt7sdUdBCWxEBXE"

try:
    auth_data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    auth_req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=auth_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(auth_req, timeout=10) as resp:
        token = json.loads(resp.read())["tenant_access_token"]
    log("Feishu token 获取成功")

    # 构建 interactive 卡片
    card_data = {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": f"🌙 晚安！ {time.strftime('%Y年%m月%d日')} {CITY_NAME}天气"}, "template": "purple"},
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 📍 {CITY_NAME}当前天气 ━━━**\n{weather_text} {temp}°C | 湿度 {humidity_pct}%\n风力 {wind_speed} km/h | 风向 {dirs[int(wind_dir/45)%8] if wind_dir else '?'}\n"}},
            {"tag": "hr"},
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 💧 未来6小时天气 ━━━**\n{rain_formatted}"}},
            {"tag": "hr"},
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 🌫️ 空气质量 ━━━**\nAQI {aqi_val}（{aqi_desc}）\nPM2.5: {pm25} | PM10: {pm10}"}},
            {"tag": "hr"},
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 🌅 日出日落 ━━━**\n日出 {sunrise} | 日落 {sunset}"}}
        ]
    }

    msg_data = json.dumps({
        "receive_id": "ou_5db13b27b4a70dde91c409d35ac16bb1",
        "msg_type": "interactive",
        "content": json.dumps(card_data)
    }).encode()

    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=msg_data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        r = json.loads(resp.read())
    log("✅ 卡片发送成功" if r.get("code") == 0 else f"⚠️ 失败：{r.get('msg','')}")
except Exception as e:
    log(f"❌ 发送异常：{e}")

log("=== 完成 ===")
