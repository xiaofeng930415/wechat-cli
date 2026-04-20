import sqlite3
import os
import hashlib
from wechat_cli.core.context import AppContext
from wechat_cli.core.db_cache import DBCache

ctx = AppContext()
ctx.db_cache = DBCache(ctx.msg_db_keys, ctx.db_dir)

# the md5 of filehelper is:
h = hashlib.md5(b"filehelper").hexdigest()

found = False
for i in range(10):
    dec_path = ctx.db_cache._cache_path(f"msg/msg_{i}.db")
    if not os.path.exists(dec_path): continue
    conn = sqlite3.connect(dec_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cursor.fetchall() if h in r[0]]
    if tables:
        print(f"Found in msg_{i}.db: {tables}")
        cursor.execute(f"PRAGMA table_info({tables[0]})")
        print("Cols:", [c[1] for c in cursor.fetchall()])
        cursor.execute(f"SELECT * FROM {tables[0]} WHERE local_id IN (16, 17)")
        for r in cursor.fetchall():
            print(r)
        found = True
        break
