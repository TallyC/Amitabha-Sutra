#!/usr/bin/env python3
"""推出前執行：python3 check.py
檢查 index.html 裡每一段 <script> 的語法（需要 node）。
任何一段語法錯，整個工具就會打不開、只剩底圖，所以一定要過了才推。"""
import re, subprocess, sys, tempfile, os

s = open("index.html", encoding="utf8").read()
blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", s, re.S)
bad = 0
for i, js in enumerate(blocks):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf8") as f:
        f.write(js)
        p = f.name
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    os.unlink(p)
    if r.returncode:
        bad += 1
        msg = [l for l in r.stderr.splitlines() if "Error" in l]
        print(f"第 {i+1} 段 script 語法錯誤：{msg[0] if msg else r.stderr[:300]}")
print("全部通過" if not bad else f"有 {bad} 段錯誤，請先修正再推")
sys.exit(1 if bad else 0)
