#!/usr/bin/env python3
"""
下载 baoyu-skills README 中的所有图片到 Obsidian 附件文件夹，
并重写 markdown 文件，更新图片路径指向附件文件夹。
"""

import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urljoin

# 配置
VAULT_PATH = "/Users/kk/Documents/Obsidian Vault"
SKILL_FOLDER = os.path.join(VAULT_PATH, "Skill")
ATTACHMENT_FOLDER = os.path.join(VAULT_PATH, "附件（非必要不打开）")
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/JimLiu/baoyu-skills/main/"
OUTPUT_FILENAME = "baoyu-skills.md"

# 确保目录存在
os.makedirs(SKILL_FOLDER, exist_ok=True)
os.makedirs(ATTACHMENT_FOLDER, exist_ok=True)

# 读取原始 markdown
with open("/Users/kk/.openclaw/workspace/tmp/baoyu-skills-readme.md", "r", encoding="utf-8") as f:
    content = f.read()

# 提取所有图片链接
# 匹配 ![alt](path) 格式
img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
images = re.findall(img_pattern, content)

print(f"找到 {len(images)} 个图片引用")

# 下载图片并建立映射
img_map = {}  # old_path -> new_path
for alt, path in images:
    # 跳过已经是 URL 的
    if path.startswith("http"):
        # Star History SVG 保留原链接
        continue
    
    # 去掉 ./ 前缀
    clean_path = path.lstrip("./")
    filename = os.path.basename(clean_path)
    
    # 为 baoyu-skills 的图片添加前缀避免冲突
    # 根据路径添加子目录前缀
    path_parts = clean_path.replace("/", "-")
    new_filename = f"baoyu-skills-{path_parts}"
    
    local_path = os.path.join(ATTACHMENT_FOLDER, new_filename)
    
    # 下载图片（如果不存在）
    if not os.path.exists(local_path):
        url = urljoin(GITHUB_RAW_BASE, clean_path)
        print(f"下载: {url} -> {local_path}")
        result = subprocess.run(
            ["curl", "-sL", "-o", local_path, url],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"  失败: {result.stderr}")
            continue
    else:
        print(f"已存在: {local_path}")
    
    # 构建相对于 Skill 文件夹的路径
    # Skill 在 /Users/kk/Documents/Obsidian Vault/Skill/
    # 附件在 /Users/kk/Documents/Obsidian Vault/附件（非必要不打开）/
    # 从 Skill 到附件: ../附件（非必要不打开）/filename
    rel_path = f"../附件（非必要不打开）/{new_filename}"
    img_map[path] = rel_path

# 替换图片路径
new_content = content
for old_path, new_path in img_map.items():
    # 精确匹配括号内的路径
    new_content = new_content.replace(f"]({old_path})", f"]({new_path})")

# 保存新文件
output_path = os.path.join(SKILL_FOLDER, OUTPUT_FILENAME)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"\n文件已保存到: {output_path}")
print(f"图片保存在: {ATTACHMENT_FOLDER}")
print(f"总共处理了 {len(img_map)} 个本地图片")
