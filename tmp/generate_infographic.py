#!/usr/bin/env python3
"""Generate LLM Ranking Dashboard Infographic - Corporate Memphis Style"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon
import numpy as np

# Corporate Memphis color palette
COLORS = {
    'purple': '#9B5DE5',
    'orange': '#F15BB5', 
    'teal': '#00BBF9',
    'yellow': '#FEE440',
    'coral': '#FF6B35',
    'mint': '#06FFA5',
    'lavender': '#E0AAFF',
    'peach': '#FFD6A5',
    'sky': '#CAF0F8',
    'hot_pink': '#FF006E'
}

# Gold/Silver/Bronze for top 3
RANK_COLORS = ['#FFD700', '#C0C0C0', '#CD7F32']

# Set up the figure with 3:4 aspect ratio (vertical)
fig, ax = plt.subplots(figsize=(9, 12), facecolor='#FAFAFA')
ax.set_xlim(0, 100)
ax.set_ylim(0, 133.33)  # 4:3 ratio maintained
ax.axis('off')

# Use Chinese font
plt.rcParams['font.family'] = 'PingFang HK'
plt.rcParams['axes.unicode_minus'] = False

# === BACKGROUND DECORATIVE ELEMENTS (Corporate Memphis style) ===
# Floating geometric shapes
def add_floating_shape(shape_type, x, y, size, color, rotation=0):
    if shape_type == 'circle':
        circle = Circle((x, y), size, facecolor=color, edgecolor='none', alpha=0.3)
        ax.add_patch(circle)
    elif shape_type == 'rect':
        rect = FancyBboxPatch((x-size, y-size), size*2, size*2, 
                              boxstyle="round,pad=0.02", 
                              facecolor=color, edgecolor='none', alpha=0.25)
        ax.add_patch(rect)
    elif shape_type == 'triangle':
        triangle = Polygon([(x, y+size), (x-size, y-size), (x+size, y-size)], 
                         facecolor=color, edgecolor='none', alpha=0.2)
        ax.add_patch(triangle)

# Add decorative elements
add_floating_shape('circle', 8, 125, 6, COLORS['purple'])
add_floating_shape('circle', 92, 120, 4, COLORS['teal'])
add_floating_shape('rect', 15, 110, 3, COLORS['yellow'], 15)
add_floating_shape('triangle', 88, 105, 4, COLORS['orange'])
add_floating_shape('circle', 5, 20, 5, COLORS['mint'])
add_floating_shape('rect', 95, 30, 3, COLORS['coral'])

# === TITLE SECTION ===
# Main title box
title_box = FancyBboxPatch((10, 115), 80, 15, 
                          boxstyle="round,pad=1", 
                          facecolor='white', 
                          edgecolor=COLORS['purple'], 
                          linewidth=3)
ax.add_patch(title_box)

# Title text
ax.text(50, 124, '2026国产大模型综合实力排名', 
        fontsize=20, fontweight='bold', ha='center', va='center',
        color='#2D3436')
ax.text(50, 118, 'TOP 10 权威榜单', 
        fontsize=12, ha='center', va='center',
        color='#636E72')

# === TOP 3 PODIUM SECTION ===
podium_y = 98

# Draw podium blocks
def draw_podium(rank, model, company, score, x, y, color):
    height = 12 - rank * 2  # 1st is tallest
    # Podium base
    podium = FancyBboxPatch((x-8, y-height), 16, height,
                           boxstyle="round,pad=0.5",
                           facecolor=color,
                           edgecolor='none')
    ax.add_patch(podium)
    
    # Rank medal
    medal_colors = ['#FFD700', '#C0C0C0', '#CD7F32']
    medal = Circle((x, y+3), 2.5, facecolor=medal_colors[rank-1], edgecolor='white', linewidth=2)
    ax.add_patch(medal)
    ax.text(x, y+3, f'{rank}', fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Model name
    ax.text(x, y-height/2+2, model, fontsize=9, fontweight='bold', ha='center', va='center',
            color='white', wrap=True)
    ax.text(x, y-height/2-1, company, fontsize=7, ha='center', va='center',
            color='white', alpha=0.9)
    ax.text(x, y-height/2-4, f'综合 {score}', fontsize=10, fontweight='bold', ha='center', va='center',
            color='white')

# Draw top 3
draw_podium(2, '千问\nQwen 3.5', '阿里巴巴', '9.4', 25, podium_y, COLORS['teal'])
draw_podium(1, 'DeepSeek\nV3.2', 'DeepSeek', '9.6', 50, podium_y+2, COLORS['purple'])
draw_podium(3, 'Kimi\nK2.5', '月之暗面', '9.2', 75, podium_y-1, COLORS['orange'])

# === KPI WIDGETS SECTION ===
widget_y = 75

# Draw 4 KPI widgets in a 2x2 grid
kpi_data = [
    ('性能', '9.03', COLORS['coral'], '综合推理、编码、多模态'),
    ('智商', '8.94', COLORS['teal'], '逻辑推理、数学、知识'),
    ('性价比', '8.98', COLORS['mint'], 'API价格/性能比'),
    ('综合', '8.98', COLORS['purple'], '三项加权平均')
]

widget_positions = [(20, widget_y), (50, widget_y), (20, widget_y-18), (50, widget_y-18)]

for (label, value, color, desc), (x, y) in zip(kpi_data, widget_positions):
    # Widget background
    widget = FancyBboxPatch((x-12, y-10), 24, 16,
                           boxstyle="round,pad=0.8",
                           facecolor='white',
                           edgecolor=color,
                           linewidth=2)
    ax.add_patch(widget)
    
    # Color accent bar
    accent = Rectangle((x-12, y+4), 24, 2, facecolor=color, edgecolor='none')
    ax.add_patch(accent)
    
    # Label
    ax.text(x, y+7, label, fontsize=9, ha='center', va='center', color='#636E72')
    # Value (big)
    ax.text(x, y-1, value, fontsize=18, fontweight='bold', ha='center', va='center', color=color)
    # Description
    ax.text(x, y-6, desc, fontsize=6, ha='center', va='center', color='#B2BEC3')

# === RANKING CHART SECTION ===
chart_y = 35

# Chart background
chart_bg = FancyBboxPatch((8, 8), 84, chart_y-8,
                         boxstyle="round,pad=1",
                         facecolor='white',
                         edgecolor='#E0E0E0',
                         linewidth=1)
ax.add_patch(chart_bg)

# Header
ax.text(15, chart_y-3, '排名', fontsize=8, fontweight='bold', ha='center', color='#636E72')
ax.text(35, chart_y-3, '模型', fontsize=8, fontweight='bold', ha='center', color='#636E72')
ax.text(55, chart_y-3, '厂商', fontsize=8, fontweight='bold', ha='center', color='#636E72')
ax.text(70, chart_y-3, '综合', fontsize=8, fontweight='bold', ha='center', color='#636E72')
ax.text(85, chart_y-3, '得分条', fontsize=8, fontweight='bold', ha='center', color='#636E72')

# Full data
models_data = [
    (4, '豆包 2.0 Pro', '字节跳动', 9.1),
    (5, 'GLM-5', '智谱AI', 9.0),
    (6, 'MiniMax M2.5', 'MiniMax', 8.9),
    (7, '元宝', '腾讯', 8.7),
    (8, '文心 5.0', '百度', 8.6),
    (9, '百川', '百川智能', 8.4),
    (10, '360智脑', '360', 8.1),
]

row_height = 3.5
for i, (rank, model, company, score) in enumerate(models_data):
    y_pos = chart_y - 6 - i * row_height
    
    # Rank
    rank_color = COLORS['hot_pink'] if rank <= 5 else '#B2BEC3'
    ax.text(15, y_pos, f'{rank}', fontsize=8, fontweight='bold', ha='center', 
            color=rank_color)
    
    # Model name
    ax.text(25, y_pos, model, fontsize=7, ha='left', va='center', color='#2D3436')
    
    # Company
    ax.text(55, y_pos, company, fontsize=6, ha='center', va='center', color='#636E72')
    
    # Score
    ax.text(70, y_pos, f'{score}', fontsize=8, fontweight='bold', ha='center', 
            color=COLORS['purple'])
    
    # Score bar
    bar_width = score * 1.5  # scale to fit
    bar = FancyBboxPatch((75, y_pos-1), bar_width, 2,
                        boxstyle="round,pad=0.1",
                        facecolor=COLORS['teal'],
                        edgecolor='none',
                        alpha=0.7)
    ax.add_patch(bar)

# === FOOTER ===
footer_y = 5

# Data source box
source_box = FancyBboxPatch((10, footer_y-2), 80, 6,
                           boxstyle="round,pad=0.3",
                           facecolor='#F8F9FA',
                           edgecolor='#E0E0E0')
ax.add_patch(source_box)

ax.text(50, footer_y+1, '评分说明: 性能=推理/编码/多模态 | 智商=逻辑/数学/知识 | 性价比=价格/性能比 | 综合=加权平均', 
        fontsize=6, ha='center', va='center', color='#636E72')
ax.text(50, footer_y-0.5, '数据来源: 艾媒金榜、DataLearner、Arena AI等权威榜单综合整理', 
        fontsize=6, ha='center', va='center', color='#B2BEC3')

# === DECORATIVE ELEMENTS ===
# Add some floating dots
dots = [(20, 105), (80, 108), (12, 50), (88, 55), (30, 15), (70, 12)]
for dx, dy in dots:
    dot = Circle((dx, dy), 1, facecolor=np.random.choice(list(COLORS.values())), 
                edgecolor='none', alpha=0.4)
    ax.add_patch(dot)

# Save
plt.tight_layout(pad=0)
plt.savefig('/Users/kk/.openclaw/workspace/tmp/llm-ranking.png', 
            dpi=200, 
            facecolor='#FAFAFA',
            edgecolor='none',
            bbox_inches='tight',
            pad_inches=0.2)
print('Infographic saved to /Users/kk/.openclaw/workspace/tmp/llm-ranking.png')
