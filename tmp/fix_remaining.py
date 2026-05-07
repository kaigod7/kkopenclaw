#!/usr/bin/env python3
"""
修复剩余的3个表格前无空行问题
"""

FILE = "/Users/kk/Documents/Obsidian Vault/Skill/baoyu-skills.md"

with open(FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 需要修复的位置（当前行号，1-based）
target_lines = [
    '**布局**（信息密度）：',
    '**布局**（分镜排列）：',
    '**环境变量**（配置方法见[环境配置](#环境配置)）：',
]

changes = []
for target in target_lines:
    for i, line in enumerate(lines):
        if line.strip() == target:
            # 检查下一行是否以 | 开头
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
                # 检查当前行后面是否已经是空行
                if lines[i].endswith("\n") and (i + 1 >= len(lines) or lines[i + 1].strip() != ""):
                    # 在当前行后面插入空行
                    lines.insert(i + 1, "\n")
                    changes.append(f"Line {i+1}: 在 '{target[:35]}' 后添加空行")
                    break

with open(FILE, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"修复 {len(changes)} 处:\n")
for c in changes:
    print(f"  {c}")
