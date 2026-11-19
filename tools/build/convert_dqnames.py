"""把遊戲存下的 DQNames.lua 轉成網站用的 JSON。
用法：python3 convert_dqnames.py DQNames.lua names.json
"""
import json, sys
from lupa import LuaRuntime

def to_py(t):
    if hasattr(t, "items"):
        d = {}
        for k, v in t.items():
            d[str(k)] = to_py(v)
        return d
    return t

src, out = sys.argv[1], sys.argv[2]
lua = LuaRuntime()
lua.execute(open(src, encoding="utf-8").read())
db = lua.globals().DQNamesDB
data = to_py(db) if db is not None else {}
json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in data.items() if isinstance(v, dict)})
