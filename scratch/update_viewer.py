# -*- coding: utf-8 -*-
"""
update_viewer.py
【ネタバレ注意】第2作_VRゲーム小説_本文.md の最新全200話を index.html の novels["2"].chapters に反映する。
"""
import json
import re

MD_FILE = '【ネタバレ注意】第2作_VRゲーム小説_本文.md'
HTML_FILE = 'index.html'

# 1. 本文から全話抽出
with open(MD_FILE, 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.split(r'\n(?=## 第\d+話)', text)
chapters = []

for sec in sections[1:]:
    lines = sec.strip().splitlines()
    if not lines:
        continue
    raw_title = lines[0].strip()
    title = re.sub(r'^##\s*', '', raw_title)
    body = '\n'.join(lines[1:]).strip()
    chapters.append({
        'title': title,
        'content': body
    })

print(f'Extracted {len(chapters)} chapters for Novel 2.')

# 2. index.html の更新
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# novels["2"] の chapters 配列を置換
novel2_json = json.dumps(chapters, ensure_ascii=False)

pattern = r'("2":\s*\{\s*id:\s*"2",\s*fullTitle:\s*"[^"]*",\s*chapters:\s*)\[.*?\](\s*\})'
match = re.search(pattern, html, flags=re.DOTALL)

if not match:
    print('ERROR: novels["2"] structure not found in index.html!')
else:
    new_html = html[:match.start(1)] + match.group(1) + novel2_json + match.group(2) + html[match.end():]
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'SUCCESS: index.html updated with {len(chapters)} chapters of Novel 2!')
