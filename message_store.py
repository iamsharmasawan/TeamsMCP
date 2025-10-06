# message_store.py
import sqlite3
from typing import Any, Dict, Iterable
import os


DB_PATH = os.getenv("MESSAGES_DB", "./messages.sqlite")


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS messages (
id TEXT PRIMARY KEY,
source TEXT,
created TEXT,
sender TEXT,
body TEXT,
raw_json TEXT
)
"""




def get_conn():
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute(CREATE_SQL)
conn.commit()
return conn




def save_message(conn: sqlite3.Connection, msg: Dict[str, Any], source: str = "channel") -> None:
msg_id = msg.get("id")
created = msg.get("createdDateTime")
sender = None
try:
sender = msg.get("from", {}).get("user", {}).get("displayName")
except Exception:
sender = str(msg.get("from"))
body = str(msg.get("body", {}).get("content", ""))
raw = str(msg)
conn.execute(
"INSERT OR REPLACE INTO messages(id, source, created, sender, body, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
(msg_id, source, created, sender, body, raw)
)
conn.commit()




def bulk_save(conn: sqlite3.Connection, msgs: Iterable[Dict[str, Any]], source: str = "channel"):
for m in msgs:
save_message(conn, m, source=source)