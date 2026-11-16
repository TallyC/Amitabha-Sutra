#!/usr/bin/env python3
"""每次推出前執行：python3 ver.py <big|minor|micro> "這一版改了什麼（寫使用者看得懂的用法）"
版號 V-4.903：4 大修（整體架構）、9 小修、03 微調（文字等）。
會改 index.html 的 APPV，並在版本記錄 CHG 最前面加一筆（含日期與時間）。"""
import re,sys,json,datetime
kind,text=sys.argv[1],sys.argv[2]
p="index.html";s=open(p,encoding="utf8").read()
m=re.search(r'var APPV="V-(\d+)\.(\d)(\d\d)";',s);a,b,c=map(int,m.groups())
if kind=="big":a,b,c=a+1,0,0
elif kind=="minor":b,c=b+1,0
else:c+=1
if c>99:b,c=b+1,0
if b>9:a,b,c=a+1,0,0
v="V-%d.%d%02d"%(a,b,c)
now=datetime.datetime.now()
s=s.replace(m.group(0),'var APPV="%s";'%v)
e={"v":v,"d":now.strftime("%Y-%m-%d"),"tm":now.strftime("%H:%M"),"t":text}
s=s.replace("\nvar CHG=[","\nvar CHG=["+json.dumps(e,ensure_ascii=False,separators=(",",":"))+",",1)
open(p,"w",encoding="utf8").write(s);print(v)
