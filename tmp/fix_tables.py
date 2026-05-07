#!/usr/bin/env python3
"""
修复 baoyu-skills.md 中的表格格式问题：
1. 在表格描述和表格之间添加空行
2. 修复空表头（添加零宽空格占位符）
"""

import re

FILE = "/Users/kk/Documents/Obsidian Vault/Skill/baoyu-skills.md"

with open(FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

fixed_lines = []
changes = []

i = 0
while i < len(lines):
    line = lines[i]
    fixed_lines.append(line)
    
    # 检查当前行是否是表格描述，下一行是否是表格
    if i + 1 < len(lines):
        next_line = lines[i + 1]
        stripped = line.strip()
        next_stripped = next_line.strip()
        
        # 如果当前行是表格描述（不以 | 开头，但以 ** 开头且以 ：结尾）
        # 且下一行是表格行（以 | 开头）
        if (stripped.startswith("**") and stripped.endswith("**：") and 
            next_stripped.startswith("|") and not stripped.startswith("|")):
            # 检查当前行和下一行之间是否缺少空行
            # fixed_lines 的最后一个元素就是当前行
            # 如果当前行不是空行，我们需要在下一行之前插入空行
            # 但当前行已经 append 到 fixed_lines 了
            # 我们只需要确认下一行之前需要有空行
            # 因为 fixed_lines 的末尾是当前行（非空），下一行应该插入一个空行
            fixed_lines.append("\n")
            changes.append(f"Line {i+1}: 在 '{stripped[:40]}' 后添加空行")
    
    i += 1

# 修复空表头：将 | | | | 替换为包含零宽空格的表头
new_content = "".join(fixed_lines)

# 找到所有空表头表格：第一行是 | 或全空格，第二行是 | :---: | :---: | :---: |
# 使用正则替换
# 匹配模式：行首的 | 空格 | 空格 | ... 后面跟着分隔行
# 将 |   |   |   | 替换为 | &#8203; | &#8203; | &#8203; |

def fix_empty_header(match):
    header_line = match.group(1)
    # 将 | 空格 | 空格 | 替换为 | &#8203; | &#8203; |
    # 保留原始的空格数量和对齐方式
    cells = header_line.split("|")
    new_cells = []
    for cell in cells:
        stripped = cell.strip()
        if stripped == "":
            new_cells.append(" &#8203; ")
        else:
            new_cells.append(cell)
    return "|".join(new_cells)

# 替换所有空表头（单元格内容为空格或空的）
# 注意：需要匹配整行都是 | 空格 | 的行
pattern = r'^(\|[\s|]*\|)$'
for line_num, line in enumerate(fixed_lines):
    if re.match(r'^\|\s*\|\s*\|\s*\|$', line.strip()):
        # 这是空表头行
        parts = line.split("|")
        new_parts = []
        for j, part in enumerate(parts):
            if j == 0 or j == len(parts) - 1:
                new_parts.append(part)  # 保留开头和结尾
            elif part.strip() == "":
                new_parts.append(" &#8203; ")
            else:
                new_parts.append(part)
        fixed_lines[line_num] = "|".join(new_parts)
        changes.append(f"Line {line_num+1}: 修复空表头")

# 保存
with open(FILE, "w", encoding="utf-8") as f:
    f.writelines(fixed_lines)

print(f"共修复 {len(changes)} 处格式问题:\n")
for c in changes:
    print(f"  {c}")
