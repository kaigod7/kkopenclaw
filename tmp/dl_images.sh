#!/bin/bash
# 下载剩余图片
set -e

ATT="/Users/kk/Documents/Obsidian Vault/附件（非必要不打开）"
BASE="https://raw.githubusercontent.com/JimLiu/baoyu-skills/main"

dl() {
    local path="$1"
    local fname="baoyu-skills-$(echo "$path" | tr '/' '-')"
    local fpath="$ATT/$fname"
    if [ ! -f "$fpath" ]; then
        curl -sL --proxy http://127.0.0.1:7890 -o "$fpath" "$BASE/$path"
        echo "✓ $fname"
    fi
}

dl screenshots/infographic-styles/claymation.webp
dl screenshots/infographic-styles/kawaii.webp
dl screenshots/infographic-styles/storybook-watercolor.webp
dl screenshots/infographic-styles/chalkboard.webp
dl screenshots/infographic-styles/cyberpunk-neon.webp
dl screenshots/infographic-styles/bold-graphic.webp
dl screenshots/infographic-styles/aged-academia.webp
dl screenshots/infographic-styles/corporate-memphis.webp
dl screenshots/infographic-styles/technical-schematic.webp
dl screenshots/infographic-styles/origami.webp
dl screenshots/infographic-styles/pixel-art.webp
dl screenshots/infographic-styles/ui-wireframe.webp
dl screenshots/infographic-styles/subway-map.webp
dl screenshots/infographic-styles/ikea-manual.webp
dl screenshots/infographic-styles/knolling.webp
dl screenshots/infographic-styles/lego-brick.webp
dl screenshots/slide-deck-styles/blueprint.webp
dl screenshots/slide-deck-styles/chalkboard.webp
dl screenshots/slide-deck-styles/bold-editorial.webp
dl screenshots/slide-deck-styles/corporate.webp
dl screenshots/slide-deck-styles/dark-atmospheric.webp
dl screenshots/slide-deck-styles/editorial-infographic.webp
dl screenshots/slide-deck-styles/fantasy-animation.webp
dl screenshots/slide-deck-styles/intuition-machine.webp
dl screenshots/slide-deck-styles/minimal.webp
dl screenshots/slide-deck-styles/notion.webp
dl screenshots/slide-deck-styles/pixel-art.webp
dl screenshots/slide-deck-styles/scientific.webp
dl screenshots/slide-deck-styles/sketch-notes.webp
dl screenshots/slide-deck-styles/vector-illustration.webp
dl screenshots/slide-deck-styles/vintage.webp
dl screenshots/slide-deck-styles/watercolor.webp
dl screenshots/comic-layouts/standard.webp
dl screenshots/comic-layouts/cinematic.webp
dl screenshots/comic-layouts/dense.webp
dl screenshots/comic-layouts/splash.webp
dl screenshots/comic-layouts/mixed.webp
dl screenshots/comic-layouts/webtoon.webp
dl screenshots/article-illustrator-styles/notion.webp
dl screenshots/article-illustrator-styles/elegant.webp
dl screenshots/article-illustrator-styles/warm.webp
dl screenshots/article-illustrator-styles/minimal.webp
dl screenshots/article-illustrator-styles/blueprint.webp
dl screenshots/article-illustrator-styles/watercolor.webp
dl screenshots/article-illustrator-styles/editorial.webp
dl screenshots/article-illustrator-styles/scientific.webp

echo "完成"
