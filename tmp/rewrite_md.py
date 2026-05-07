#!/usr/bin/env python3
"""
重写 baoyu-skills markdown，更新图片路径并重新设计排版。
"""

import os
import re

VAULT_PATH = "/Users/kk/Documents/Obsidian Vault"
SKILL_FOLDER = os.path.join(VAULT_PATH, "Skill")
ATTACHMENT_FOLDER = os.path.join(VAULT_PATH, "附件（非必要不打开）")
OUTPUT_FILENAME = "baoyu-skills.md"

with open("/Users/kk/.openclaw/workspace/tmp/baoyu-skills-readme.md", "r", encoding="utf-8") as f:
    content = f.read()

# 替换图片路径
img_map = {}
imgs = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
for alt, path in imgs:
    if path.startswith("http"):
        continue
    clean_path = path.lstrip("./")
    new_filename = "baoyu-skills-" + clean_path.replace("/", "-")
    rel_path = f"../附件（非必要不打开）/{new_filename}"
    img_map[path] = rel_path

for old_path, new_path in img_map.items():
    content = content.replace(f"]({old_path})", f"]({new_path})")

# 重新设计排版
lines = content.split("\n")
new_lines = []

# 添加 frontmatter
new_lines.append("---")
new_lines.append("tags: [claude-code, skill, ai-tool]")
new_lines.append("date: 2026-05-07")
new_lines.append("---")
new_lines.append("")

in_code_block = False
for i, line in enumerate(lines):
    # 保留原始 frontmatter 已经被跳过，原始文档没有 frontmatter
    
    # 代码块标记
    if line.strip().startswith("```"):
        in_code_block = not in_code_block
        new_lines.append(line)
        continue
    
    if in_code_block:
        new_lines.append(line)
        continue
    
    # 在主要技能分类之间添加分隔线
    if line.startswith("### 内容技能") or line.startswith("### AI 生成技能") or line.startswith("### 工具技能"):
        new_lines.append("")
        new_lines.append("---")
        new_lines.append("")
        new_lines.append(line)
        continue
    
    # 在二级技能标题前添加空行（如果还没有）
    if line.startswith("#### baoyu-"):
        new_lines.append("")
        new_lines.append(line)
        continue
    
    new_lines.append(line)

# 合并
new_content = "\n".join(new_lines)

# 添加目录（在 frontmatter 后、正文前）
toc = """
## 📑 目录

- [前置要求](#前置要求)
- [安装](#安装)
- [更新技能](#更新技能)
- [可用技能](#可用技能)
  - [内容技能](#内容技能-content-skills)
  - [AI 生成技能](#ai-生成技能-ai-generation-skills)
  - [工具技能](#工具技能-utility-skills)
- [环境配置](#环境配置)
- [自定义扩展](#自定义扩展)
- [免责声明](#免责声明)
- [致谢](#致谢)
- [许可证](#许可证)

---

"""

# 在第一个一级标题后插入目录
new_content = new_content.replace("# baoyu-skills\n", "# baoyu-skills\n\n> 宝玉分享的 Claude Code 技能集，提升日常工作效率。\n\n" + toc)

# 保存
output_path = os.path.join(SKILL_FOLDER, OUTPUT_FILENAME)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"已保存到: {output_path}")
print(f"总字符数: {len(new_content)}")
