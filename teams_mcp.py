# teams_mcp.py


@mcp.tool()
def list_channels(team_id: str) -> str:
data = graph_get(f"/teams/{team_id}/channels")
channels = data.get("value", [])
if not channels:
return f"No channels found for team {team_id}."
return "\n".join([f"{c['id']} - {c.get('displayName')}" for c in channels])




@mcp.tool()
def get_channel_messages(team_id: str, channel_id: str, top: int = 50) -> str:
"""Return `top` messages from channel (shortened)."""
path = f"/teams/{team_id}/channels/{channel_id}/messages?$top={top}"
msgs = list(iterate_paged(path))
if not msgs:
return "No messages found."
if _db_conn:
bulk_save(_db_conn, msgs, source="channel")
lines = []
for m in msgs:
created = m.get("createdDateTime")
sender = m.get("from", {}).get("user", {}).get("displayName") or "unknown"
body = str(m.get("body", {}).get("content", ""))
if len(body) > 300:
body = body[:300] + "…"
lines.append(f"[{created}] {sender}: {body}")
return "\n\n".join(lines)




@mcp.tool()
def list_chats(top: int = 50) -> str:
data = graph_get(f"/chats?$top={top}")
chats = data.get("value", [])
if not chats:
return "No chats found."
lines = []
for c in chats:
cid = c.get('id')
ctype = c.get('chatType')
topic = c.get('topic') or ''
lines.append(f"{cid} - {ctype} - {topic}")
return "\n".join(lines)




@mcp.tool()
def get_chat_messages(chat_id: str, top: int = 50) -> str:
path = f"/chats/{chat_id}/messages?$top={top}"
msgs = list(iterate_paged(path))
if not msgs:
return "No messages."
if _db_conn:
bulk_save(_db_conn, msgs, source="chat")
lines = []
for m in msgs:
created = m.get("createdDateTime")
sender = m.get("from", {}).get("user", {}).get("displayName") or "unknown"
body = str(m.get("body", {}).get("content", ""))
if len(body) > 300:
body = body[:300] + "…"
lines.append(f"[{created}] {sender}: {body}")
return "\n\n".join(lines)




if __name__ == "__main__":
mcp.run()