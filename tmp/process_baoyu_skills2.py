#!/usr/bin/env python3
"""
下载 baoyu-skills README 中的所有图片到 Obsidian 附件文件夹，
并重写 markdown 文件，更新图片路径指向附件文件夹。
"""

import os
import re
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
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
img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
images = re.findall(img_pattern, content)

print(f"找到 {len(images)} 个图片引用")

# 下载图片并建立映射
img_map = {}
success = 0
fail = 0

for alt, path in images:
    if path.startswith("http"):
        # Star History SVG 保留原链接
        continue
    
    clean_path = path.lstrip("./")
    path_parts = clean_path.replace("/", "-")
    new_filename = f"baoyu-skills-{path_parts}"
    local_path = os.path.join(ATTACHMENT_FOLDER, new_filename)
    
    if not os.path.exists(local_path):
        url = urljoin(GITHUB_RAW_BASE, clean_path)
        print(f"下载: {clean_path}")
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=30) as response:
                data = response.read()
                with open(local_path, "wb") as f:
                    f.write(data)
            success += 1
        except Exception as e:
            print(f"  ✗ 失败: {e}")
            fail += 1
            continue
    else:
        print(f"已存在: {new_filename}")
        success += 1
    
    rel_path = f"../附件（非必要不打开）/{new_filename}"
    img_map[path] = rel_path

print(f"\n下载完成: {success} 成功, {fail} 失败")

# 替换图片路径
new_content = content
for old_path, new_path in img_map.items():
    new_content = new_content.replace(f"]({old_path})", f"]({new_path})")

# 保存新文件
output_path = os.path.join(SKILL_FOLDER, OUTPUT_FILENAME)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"\n文件已保存到: {output_path}")
