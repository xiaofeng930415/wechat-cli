import sqlite3
import os

dec_path = "/Users/guifengxiao/.wechat-cli/decrypted/msg/msg_0.db"
conn = sqlite3.connect(dec_path)
cursor = conn.cursor()

cursor.execute("SELECT local_id, local_type, create_time, msg_source, msg_desc, content FROM Chat_e1160350ca962d3a1f11a7f6f7d455ec WHERE local_id IN (16, 17)")
rows = cursor.fetchall()
for r in rows:
    print(r)
