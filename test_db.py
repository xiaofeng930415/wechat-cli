import sqlite3
import os
from wechat_cli.core.context import AppContext
from wechat_cli.core.db_cache import DBCache

ctx = AppContext()
ctx.db_cache = DBCache(ctx.msg_db_keys, ctx.db_dir)

dec_path = ctx.db_cache.get("msg/msg_0.db")
print("Decrypted path:", dec_path)

conn = sqlite3.connect(dec_path)
cursor = conn.cursor()

cursor.execute("SELECT local_id, local_type, create_time, content FROM Chat_e1160350ca962d3a1f11a7f6f7d455ec WHERE create_time >= 1776515760 AND create_time <= 1776515820")
rows = cursor.fetchall()
print("Rows:")
for r in rows:
    print(r)
