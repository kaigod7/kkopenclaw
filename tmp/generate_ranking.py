from PIL import Image, ImageDraw, ImageFont
import json

# 加载数据
with open("/Users/kk/.openclaw/workspace/tmp/models_data.json", "r") as f:
    models = json.load(f)

# 画布尺寸 (3:4比例，小红书风格)
WIDTH = 900
HEIGHT = 1200

# 配色方案
COLORS = {
    "bg_top": (102, 51, 204),      # 紫色渐变顶部
    "bg_bottom": (51, 102, 204),   # 蓝色渐变底部
    "gold": (255, 215, 0),         # 金牌
    "silver": (192, 192, 192),     # 银牌
    "bronze": (205, 127, 50),      # 铜牌
    "white": (255, 255, 255),
    "dark": (33, 33, 33),
    "gray": (128, 128, 128),
    "light_gray": (240, 240, 240),
    "accent1": (255, 107, 107),    # 珊瑚红
    "accent2": (78, 205, 196),     # 青绿
    "accent3": (255, 209, 102),    # 黄色
    "accent4": (150, 111, 214),    # 紫罗兰
}

# 创建画布
img = Image.new('RGB', (WIDTH, HEIGHT), COLORS["white"])
draw = ImageDraw.Draw(img)

# 绘制渐变背景
for y in range(HEIGHT):
    ratio = y / HEIGHT
    r = int(COLORS["bg_top"][0] * (1 - ratio) + COLORS["bg_bottom"][0] * ratio)
    g = int(COLORS["bg_top"][1] * (1 - ratio) + COLORS["bg_bottom"][1] * ratio)
    b = int(COLORS["bg_top"][2] * (1 - ratio) + COLORS["bg_bottom"][2] * ratio)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# 加载字体
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 48)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 28)
    font_model = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 24)
    font_company = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 18)
    font_score = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 22)
    font_small = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 16)
    font_tiny = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 14)
except:
    font_title = ImageFont.load_default()
    font_subtitle = font_title
    font_model = font_title
    font_company = font_title
    font_score = font_title
    font_small = font_title
    font_tiny = font_title

# 绘制标题区域
padding = 40
current_y = 60

# 主标题
draw.text((WIDTH//2, current_y), "2026国产大模型", font=font_title, fill=COLORS["white"], anchor="mm")
current_y += 55
draw.text((WIDTH//2, current_y), "综合实力排名", font=font_title, fill=COLORS["white"], anchor="mm")
current_y += 50

# 副标题
draw.text((WIDTH//2, current_y), "TOP 10 权威榜单", font=font_subtitle, fill=(255, 255, 255, 200), anchor="mm")
current_y += 50

# 绘制白色内容区域
content_top = current_y + 10
content_bottom = HEIGHT - 80
margin = 30
draw.rounded_rectangle(
    [(margin, content_top), (WIDTH - margin, content_bottom)],
    radius=20,
    fill=COLORS["white"]
)

# 表头
header_y = content_top + 25
col_x = [60, 120, 260, 420, 510, 600, 700, 790]
headers = ["排名", "模型", "厂商", "性能", "智商", "性价比", "综合"]
header_colors = [COLORS["dark"], COLORS["dark"], COLORS["dark"], COLORS["accent1"], COLORS["accent2"], COLORS["accent3"], COLORS["accent4"]]

for i, (x, h, c) in enumerate(zip(col_x, headers, header_colors)):
    if i == 0:
        draw.text((x, header_y), h, font=font_small, fill=c, anchor="lm")
    elif i == 1:
        draw.text((x, header_y), h, font=font_small, fill=c, anchor="lm")
    elif i == 2:
        draw.text((x, header_y), h, font=font_small, fill=c, anchor="lm")
    else:
        draw.text((x, header_y), h, font=font_small, fill=c, anchor="lm")

# 绘制分隔线
line_y = header_y + 25
draw.line([(margin + 15, line_y), (WIDTH - margin - 15, line_y)], fill=COLORS["light_gray"], width=2)

# 绘制数据行
row_start_y = line_y + 15
row_height = (content_bottom - 20 - row_start_y) // len(models)

for idx, m in enumerate(models):
    y = row_start_y + idx * row_height
    
    # 背景条（交替颜色）
    if idx % 2 == 0:
        draw.rectangle([(margin + 5, y - 2), (WIDTH - margin - 5, y + row_height - 5)], fill=(250, 250, 250))
    
    # 排名奖牌颜色
    if m["rank"] == 1:
        rank_color = COLORS["gold"]
    elif m["rank"] == 2:
        rank_color = COLORS["silver"]
    elif m["rank"] == 3:
        rank_color = COLORS["bronze"]
    else:
        rank_color = COLORS["gray"]
    
    # 排名
    draw.text((col_x[0], y + row_height//2), str(m["rank"]), font=font_score, fill=rank_color, anchor="lm")
    
    # 模型名
    draw.text((col_x[1], y + row_height//2), m["model"], font=font_model, fill=COLORS["dark"], anchor="lm")
    
    # 厂商
    draw.text((col_x[2], y + row_height//2), m["company"], font=font_company, fill=COLORS["gray"], anchor="lm")
    
    # 性能分数
    draw.text((col_x[3], y + row_height//2), f"{m['perf']}", font=font_score, fill=COLORS["accent1"], anchor="lm")
    
    # 智商分数
    draw.text((col_x[4], y + row_height//2), f"{m['iq']}", font=font_score, fill=COLORS["accent2"], anchor="lm")
    
    # 性价比分数
    draw.text((col_x[5], y + row_height//2), f"{m['value']}", font=font_score, fill=COLORS["accent3"], anchor="lm")
    
    # 综合分数（加粗）
    draw.text((col_x[6], y + row_height//2), f"{m['overall']}", font=font_score, fill=COLORS["accent4"], anchor="lm")

# 绘制底部说明
footer_y = HEIGHT - 60
draw.text((WIDTH//2, footer_y), "评分维度：性能=推理编码多模态 | 智商=逻辑数学知识 | 性价比=价格/性能比", 
          font=font_tiny, fill=COLORS["white"], anchor="mm")
draw.text((WIDTH//2, footer_y + 20), "数据来源：艾媒金榜 · DataLearner · Arena AI 综合整理", 
          font=font_tiny, fill=(255, 255, 255, 180), anchor="mm")

# 保存图片
output_path = "/Users/kk/.openclaw/workspace/tmp/llm-ranking.png"
img.save(output_path, "PNG", quality=95)
print(f"Image saved to {output_path}")
