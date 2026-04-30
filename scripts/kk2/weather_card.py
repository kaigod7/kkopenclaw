#!/usr/bin/env python3
"""
KK2 天气播报卡片 — 支持上海/悉尼，早/午/下午/晚间模板

用法：
  python3 weather_card.py --city shanghai --slot morning
  python3 weather_card.py --city sydney --slot evening

--city: shanghai | sydney
--slot: morning (蓝) | noon (黄) | afternoon (橙) | evening (紫)
"""

import json, urllib.request, time, os, sys, argparse

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LOG_FILE = os.path.join(WORKSPACE, "memory/kk2-weather.log")

CAIYUN_TOKEN = "z7AhM2I98ZFxUt2c"

CITIES = {
    "shanghai": {"loc": "121.47,31.23", "name": "上海"},
    "sydney":   {"loc": "151.2093,-33.8688", "name": "悉尼"},
}

SLOT_CONFIG = {
    "morning":   {"emoji": "🌅", "title_prefix": "早安",   "color": "blue"},
    "noon":      {"emoji": "☀️", "title_prefix": "中午",    "color": "yellow"},
    "afternoon": {"emoji": "🌤️", "title_prefix": "下午",    "color": "orange"},
    "evening":   {"emoji": "🌙", "title_prefix": "晚安",    "color": "purple"},
}

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M')}] {msg}\n")

def to_emoji_time(t):
    dmap = {"0":"0️⃣","1":"1️⃣","2":"2️⃣","3":"3️⃣","4":"4️⃣",
            "5":"5️⃣","6":"6️⃣","7":"7️⃣","8":"8️⃣","9":"9️⃣",":":":"}
    return "".join(dmap.get(c, c) for c in t)

def fetch_weather(loc_str, city_name):
    url = f"https://api.caiyunapp.com/v2.6/{CAIYUN_TOKEN}/{loc_str}/weather"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def build_card_data(slot, city_name, weather_data):
    result = weather_data.get("result", {})
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

    aqi_val = aqi.get("aqi", {}).get("chn", "?")
    pm25 = aqi.get("pm25", "?")
    pm10 = aqi.get("pm10", "?")

    astro = daily.get("astro", [{}])[0] if daily.get("astro") else {}
    sunrise = astro.get("sunrise", {}).get("time", "--:--")
    sunset = astro.get("sunset", {}).get("time", "--:--")

    # skycon map for hourly
    skycon_map = {}
    for s in hourly_skycon or []:
        skycon_map[s["datetime"][11:16]] = s["value"]

    # 逐小时预报（最多6段）
    rain_lines = []
    for h in (hourly_precip or [])[:6]:
        dt = h.get("datetime", "")
        prob = h.get("probability", 0)
        if isinstance(prob, (int, float)) and len(dt) >= 13:
            t = dt[11:16]
            p = int(prob)
            sk_emoji = skycn_emoji.get(skycon_map.get(t, "🌙"), "🌙")
            if p > 0:
                rain_lines.append(f"{to_emoji_time(t)} │ {sk_emoji} │ {p}%")
            else:
                rain_lines.append(f"{to_emoji_time(t)} │ {sk_emoji}")

    rain_formatted = "\n".join(rain_lines) if rain_lines else "未来6小时无显著降雨"
    log(f"天气获取成功：{temp}°C {skycon} ({city_name})")

    slot_cfg = SLOT_CONFIG[slot]
    card_title = f"{slot_cfg['emoji']} {slot_cfg['title_prefix']}！ {time.strftime('%Y年%m月%d日')} {city_name}天气"

    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 📍 {city_name}天气 ━━━**"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"{weather_text} {temp}°C | 湿度 {humidity_pct}%"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"风力 {wind_speed} km/h | 风向 {dirs[int(wind_dir/45)%8] if wind_dir else '?'}"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 🌫️ 空气质量 ━━━**"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"AQI {aqi_val}  PM2.5: {pm25} | PM10: {pm10}"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 💧 未来6小时天气 ━━━**"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"{rain_formatted}"}},
    ]

    # 日出日落
    elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"**━━━ 🌅 日出日落 ━━━**"}})
    elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"日出 {sunrise} | 日落 {sunset}"}})

    return {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": card_title}, "template": slot_cfg["color"]},
        "elements": elements
    }


CHAT_ID = "oc_ad0a00b59da44eb026c86147bbf19884"
APP_ID = "cli_a96f0a89bf795bb5"
APP_SECRET = "0qZOvpMy676geoq5w2h6neZgLk2Jhy04"

def send_feishu(card_data):
    auth_data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    auth_req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=auth_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(auth_req, timeout=10) as resp:
        token = json.loads(resp.read())["tenant_access_token"]

    msg_data = json.dumps({
        "receive_id": CHAT_ID,
        "msg_type": "interactive",
        "content": json.dumps(card_data)
    }).encode()

    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        data=msg_data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        r = json.loads(resp.read())
    if r.get("code") == 0:
        log("✅ 卡片发送成功")
    else:
        log(f"⚠️ 发送失败：{r.get('msg','')}")


def main():
    parser = argparse.ArgumentParser(description="KK2 天气播报")
    parser.add_argument("--city", choices=list(CITIES.keys()), required=True)
    parser.add_argument("--slot", choices=list(SLOT_CONFIG.keys()), required=True)
    args = parser.parse_args()

    city = CITIES[args.city]
    loc, name = city["loc"], city["name"]

    log(f"=== {args.slot} {name} 天气开始 ===")

    try:
        data = fetch_weather(loc, name)
        card = build_card_data(args.slot, name, data)
        send_feishu(card)
    except Exception as e:
        log(f"❌ 失败：{e}")
        sys.exit(1)

    log(f"=== 完成 ===")

if __name__ == "__main__":
    main()
