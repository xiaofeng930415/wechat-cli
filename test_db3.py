import sqlite3
import os
from wechat_cli.core.context import AppContext
from wechat_cli.core.db_cache import DBCache

ctx = AppContext()
ctx.db_cache = DBCache(ctx.msg_db_keys, ctx.db_dir)

dec_path = ctx.db_cache.get("msg/msg_0.db")
conn = sqlite3.connect(dec_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(Chat_e1160350ca962d3a1f11a7f6f7d455ec)")
print("Columns:", [c[1] for c in cursor.fetchall()])

cursor.execute("SELECT * FROM Chat_e1160350ca962d3a1f11a7f6f7d455ec WHERE local_id IN (16, 17)")
for r in cursor.fetchall():
    print(r)
