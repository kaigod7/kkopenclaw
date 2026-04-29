# 学习内容目录 | Learned Content Catalog

> 所有 K 让我学的东西都在这里，持续更新。

---

## 已备份的学习内容

### 📸 摄影修图

| 主题 | 文件 | 状态 |
|---|---|---|
| Darktable 预设风格参数（风景/人像/宠物/街拍/电影感/胶片模拟/二次元） | `memory/darktable-presets-styles.md` | ✅ 已备份 |
| Python 修图技巧（Pillow/OpenCV/scikit-image/rembg/Wand） | `memory/python-photo-editing.md` | ✅ 已备份 |

### 🎵 音频语音

| 主题 | 文件 | 状态 |
|---|---|---|
| MiniMax TTS API 正确格式（voice_setting 嵌套） | `MEMORY.md` 第 1 节 | ✅ 已备份 |
| 音色表 | `voice_favorites.json` | ✅ 已备份 |

### 🛠️ 系统工具

| 主题 | 文件 | 状态 |
|---|---|---|
| TOOLS.md（工具配置笔记） | `TOOLS.md` | ✅ 已备份 |
| AGENTS.md（工作流程） | `AGENTS.md` | ✅ 已备份 |
| MEMORY.md（长期记忆） | `MEMORY.md` | ✅ 已备份 |
| Python 脚本 | `scripts/auto_photo_edit.py`, `batch_photo_edit.py` | ✅ 已备份 |

---

## 待学习 / 进行中

- [ ] Suno/Udio 歌声生成（尚未接入，需网页操作）
- [ ] 更多修图风格（待 K 指定）

---

## 学习来源

- tavily 全网搜索
- darktable.org 官方文档
- pixls.us 社区论坛
- Real Python / GeeksforGeeks / pyimagesearch 等教程站

---

_最后更新：2026-04-08_

## ⚠️ 彩云天气 dt_key 拼接规范（2026-04-16 教训）

**症状**：3点/4点显示🌧️图标但无概率，其余时间正确

**根因**（两个bug叠加）：
1. `dt_key` 拼接错误：用 `hh`（"14"）拼接成 `2026-04-16T14`，但彩云 skycon 字典的 key 是 `2026-04-16T14:00`（带完整时间）
2. `MODERATE_RAIN` / `HEAVY_RAIN` 漏了 emoji 映射

**正确写法**：
```python
hhmm = h.get("datetime", "")[11:16]  # "14:00"
dt_key = h.get("datetime", "")[:10] + "T" + hhmm  # "2026-04-16T14:00"
sky = hourly_skycon.get(dt_key, "CLOUDY")  # 匹配正确
```

**Emoji 映射必须包含**：
```python
"LIGHT_RAIN":"🌧️","MODERATE_RAIN":"🌧️","HEAVY_RAIN":"🌧️","RAIN":"🌧️"
```

**涉及脚本**：morning_briefing.sh、noon_briefing.sh、afternoon_briefing.sh
