# # # # # from mcp.server.fastmcp import FastMCP
# # # # # import requests

# # # # # # ---------------------------
# # # # # # Directly set your Slack Bot Token here
# # # # # # ---------------------------
# # # # # SLACK_TOKEN = "os.get("SLACK_TOKEN")"  # <-- Replace with your actual token
# # # # # HEADERS = {"Authorization": f"Bearer {SLACK_TOKEN}"}

# # # # # # Create MCP server
# # # # # mcp = FastMCP("SlackManager")
#

# # # # # # ---------------------------
# # # # # # Tool: List Channels
# # # # # # ---------------------------
# # # # # @mcp.tool()
# # # # # def list_channels() -> str:
# # # # #     """List all accessible channels (public, private, DMs, MPIMs)"""
# # # # #     url = "https://slack.com/api/conversations.list?types=public_channel,private_channel,im,mpim&limit=200"
# # # # #     res = requests.get(url, headers=HEADERS).json()
    
# # # # #     if not res.get("ok"):
# # # # #         return f"Error fetching channels: {res.get('error')}"
    
# # # # #     channels = []
# # # # #     for ch in res.get("channels", []):
# # # # #         ch_type = "DM" if ch.get("is_im") else "MPIM" if ch.get("is_mpim") else "Private" if ch.get("is_private") else "Public"
# # # # #         name = ch.get("name") or f"DM/{ch.get('user')}"
# # # # #         channels.append(f"{name} ({ch_type}) → ID: {ch['id']}")
    
# # # # #     return "\n".join(channels)

# # # # # # ---------------------------
# # # # # # Tool: Fetch Messages
# # # # # # ---------------------------
# # # # # @mcp.tool()
# # # # # def fetch_messages(channel_id: str, limit: int = 20) -> str:
# # # # #     """
# # # # #     Fetch messages from a given Slack channel or DM.
# # # # #     `channel_id` = Slack channel ID
# # # # #     `limit` = number of messages to fetch
# # # # #     """
# # # # #     url = f"https://slack.com/api/conversations.history?channel={channel_id}&limit={limit}"
# # # # #     res = requests.get(url, headers=HEADERS).json()
    
# # # # #     if not res.get("ok"):
# # # # #         return f"Error fetching messages: {res.get('error')}"
    
# # # # #     messages = []
# # # # #     for msg in res.get("messages", []):
# # # # #         user = msg.get("user", "Unknown")
# # # # #         text = msg.get("text", "")
# # # # #         ts = msg.get("ts", "")
# # # # #         messages.append(f"[{ts}] {user}: {text}")
    
# # # # #     return "\n".join(messages)

# # # # # # ---------------------------
# # # # # # Resource: Greeting
# # # # # # ---------------------------
# # # # # @mcp.resource("greeting://{name}")
# # # # # def get_greeting(name: str) -> str:
# # # # #     return f"Hello, {name}! I can help you fetch Slack messages and channels."

# # # # # # ---------------------------
# # # # # # Run MCP server
# # # # # # ---------------------------
# # # # # if __name__ == "__main__":
# # # # #     mcp.run()




















from fastmcp import FastMCP
import requests
# from fastmcp import FastMCP

# ---------------------------
# Directly set your Slack Bot Token here
# ---------------------------
HEADERS = {"Authorization": f"Bearer {SLACK_TOKEN}"}

# Create MCP server
mcp = FastMCP("SlackManager")

# ---------------------------
# Helper: Get Slack user mapping
# ---------------------------
def get_user_mapping():
    """Fetch all users and return a dict mapping user_id -> username"""
    url = "https://slack.com/api/users.list"
    res = requests.get(url, headers=HEADERS).json()
    user_map = {}
    if res.get("ok"):
        for user in res.get("members", []):
            user_map[user["id"]] = user.get("real_name") or user.get("name")
    return user_map

USER_MAP = get_user_mapping()

# ---------------------------
# Tool: List Channels
# ---------------------------
@mcp.tool
def list_channels() -> str:
    """List all accessible channels (public, private, DMs, MPIMs)"""
    url = "https://slack.com/api/conversations.list?types=public_channel,private_channel,im,mpim&limit=200"
    res = requests.get(url, headers=HEADERS).json()
    
    if not res.get("ok"):
        return f"Error fetching channels: {res.get('error')}"
    
    channels = []
    for ch in res.get("channels", []):
        ch_type = "DM" if ch.get("is_im") else "MPIM" if ch.get("is_mpim") else "Private" if ch.get("is_private") else "Public"
        name = ch.get("name") or f"DM/{USER_MAP.get(ch.get('user'), ch.get('user'))}"
        channels.append(f"{name} ({ch_type}) → ID: {ch['id']}")
    
    return "\n".join(channels)

# ---------------------------
# Tool: Fetch Messages
# ---------------------------
@mcp.tool
def fetch_messages(channel_id: str, limit: int = 20) -> str:
    """
    Fetch messages from a given Slack channel or DM.
    `channel_id` = Slack channel ID
    `limit` = number of messages to fetch
    """
    url = f"https://slack.com/api/conversations.history?channel={channel_id}&limit={limit}"
    res = requests.get(url, headers=HEADERS).json()
    
    if not res.get("ok"):
        return f"Error fetching messages: {res.get('error')}"
    
    messages = []
    for msg in res.get("messages", []):
        user_id = msg.get("user")
        user_name = USER_MAP.get(user_id, user_id) if user_id else "Unknown"
        text = msg.get("text", "")
        ts = msg.get("ts", "")
        messages.append(f"[{ts}] {user_name}: {text}")
    
    return "\n".join(messages)

# ---------------------------
# Resource: Greeting
# ---------------------------
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}! I can help you fetch Slack messages and channels."

# ---------------------------
# Run MCP server
# ---------------------------
if __name__ == "__main__":
    # Test list_channels directly
    # print("Fetching all channels...")
    # print(list_channels())

    # Optional: fetch messages from a channel for testing
    # Replace with a valid channel ID from list_channels output
    # print(fetch_messages(channel_id="C0123456789", limit=5))

    # Start MCP server
    # print("Starting Slack MCP server on http://localhost:8000 ...")
    # mcp.run()
    # if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8001, 
        path="/mcp",
    )





























# # 
# # 
# from mcp.server.fastmcp import FastMCP
# import requests
# import time
# # 
# # ---------------------------
# # Directly set your Slack Bot Token here
# # ---------------------------
# SLACK_TOKEN = "os.get("SLACK_TOKEN")"  # <-- Replace with your actual token
# HEADERS = {"Authorization": f"Bearer {SLACK_TOKEN}"}
# # 
# # Create MCP server
# mcp = FastMCP("SlackManager")
# # 
# # ---------------------------
# # Helper: Get Slack user mapping
# # ---------------------------
# def get_user_mapping():
#     """Fetch all users and return a dict mapping user_id -> username"""
#     url = "https://slack.com/api/users.list"
#     res = requests.get(url, headers=HEADERS).json()
#     user_map = {}
#     if res.get("ok"):
#         for user in res.get("members", []):
#             user_map[user["id"]] = user.get("real_name") or user.get("name")
#     return user_map
# # 
# USER_MAP = get_user_mapping()
# # 
# # ---------------------------
# # Tool: List Channels
# # ---------------------------
# @mcp.tool()
# def list_channels() -> str:
#     """List all accessible channels (public, private, DMs, MPIMs)"""
#     url = "https://slack.com/api/conversations.list?types=public_channel,private_channel,im,mpim&limit=200"
#     res = requests.get(url, headers=HEADERS).json()
#     # 
#     if not res.get("ok"):
#         return f"Error fetching channels: {res.get('error')}"
#     # 
#     channels = []
#     for ch in res.get("channels", []):
#         ch_type = "DM" if ch.get("is_im") else "MPIM" if ch.get("is_mpim") else "Private" if ch.get("is_private") else "Public"
#         name = ch.get("name") or f"DM/{USER_MAP.get(ch.get('user'), ch.get('user'))}"
#         channels.append(f"{name} ({ch_type}) → ID: {ch['id']}")
#     # 
#     return "\n".join(channels)
# # 
# # ---------------------------
# # Tool: Fetch Messages
# # ---------------------------
# @mcp.tool()
# def fetch_messages(channel_id: str, limit: int = 20) -> str:
#     """
#     Fetch messages from a given Slack channel or DM.
#     `channel_id` = Slack channel ID
#     `limit` = number of messages to fetch
#     """
#     url = f"https://slack.com/api/conversations.history?channel={channel_id}&limit={limit}"
#     res = requests.get(url, headers=HEADERS).json()
#     # 
#     if not res.get("ok"):
#         return f"Error fetching messages: {res.get('error')}"
#     # 
#     messages = []
#     for msg in res.get("messages", []):
#         user_id = msg.get("user")
#         user_name = USER_MAP.get(user_id, user_id) if user_id else "Unknown"
#         text = msg.get("text", "")
#         ts = msg.get("ts", "")
#         messages.append(f"[{ts}] {user_name}: {text}")
#     # 
#     return "\n".join(messages)
# # 
# # ---------------------------
# # Resource: Greeting
# # ---------------------------
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     return f"Hello, {name}! I can help you fetch Slack messages and channels."
# # 
# # ---------------------------
# # Auto Fetch Messages Function
# # ---------------------------
# def auto_fetch_messages(interval=10, limit=5):
#     """
#     Automatically fetch latest messages from all channels every `interval` seconds.
#     `limit` = number of messages per channel
#     """
#     print(f"Starting auto-fetching messages every {interval} seconds...\n")
#     # 
#     while True:
#         try:
#             # Get all channels
#             url = "https://slack.com/api/conversations.list?types=public_channel,private_channel,im,mpim&limit=200"
#             res = requests.get(url, headers=HEADERS).json()
#             if not res.get("ok"):
#                 print(f"Error fetching channels: {res.get('error')}")
#                 time.sleep(interval)
#                 continue
#             # 
#             for ch in res.get("channels", []):
#                 ch_type = "DM" if ch.get("is_im") else "MPIM" if ch.get("is_mpim") else "Private" if ch.get("is_private") else "Public"
#                 ch_name = ch.get("name") or f"DM/{USER_MAP.get(ch.get('user'), ch.get('user'))}"
#                 ch_id = ch['id']
#                 # 
#                 # Fetch last `limit` messages
#                 messages = fetch_messages(ch_id, limit=limit)
#                 print(f"--- {ch_name} ({ch_type}) ---")
#                 print(messages)
#                 print("\n")
#             # 
#             time.sleep(interval)
#         except KeyboardInterrupt:
#             print("Stopping auto-fetch.")
#             break
#         except Exception as e:
#             print(f"Error: {e}")
#             time.sleep(interval)
# # 
# # ---------------------------
# # Run MCP server + Auto Fetch
# # ---------------------------
# if __name__ == "__main__":
#     # Start MCP server in a separate thread
#     import threading
#     server_thread = threading.Thread(target=lambda: mcp.run(), daemon=True)
#     server_thread.start()
#     # 
#     # Start auto-fetching messages
#     auto_fetch_messages(interval=15, limit=5)  # every 15 seconds, fetch last 5 messages
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 









# from mcp.server.fastmcp import FastMCP
# import requests
# import time
# import threading

# # ---------------------------
# # Directly set your Slack Bot Token here
# # ---------------------------
# HEADERS = {"Authorization": f"Bearer {SLACK_TOKEN}"}

# # Create MCP server
# mcp = FastMCP("SlackManager")

# # ---------------------------
# # Helper: Get Slack user mapping
# # ---------------------------
# def get_user_mapping():
#     url = "https://slack.com/api/users.list"
#     res = requests.get(url, headers=HEADERS).json()
#     user_map = {}
#     if res.get("ok"):
#         for user in res.get("members", []):
#             user_map[user["id"]] = user.get("real_name") or user.get("name")
#     else:
#         print("Warning: users.list failed:", res.get("error"))
#     return user_map

# USER_MAP = get_user_mapping()

# # ---------------------------
# # Helper: Join public channel
# # ---------------------------
# def join_channel(channel_id: str) -> bool:
#     """
#     Try to join a public channel using conversations.join.
#     Returns True if joined or already in channel, False otherwise.
#     Requires bot scope: channels:join
#     """
#     join_url = "https://slack.com/api/conversations.join"
#     res = requests.post(join_url, headers=HEADERS, json={"channel": channel_id}).json()
#     if res.get("ok"):
#         return True
#     # if already_in_channel or not_in_channel or restricted, return False
#     print(f"conversations.join failed for {channel_id}: {res.get('error')}")
#     # some errors are permissible: "already_in_channel" means success logically
#     if res.get("error") == "already_in_channel":
#         return True
#     return False

# # ---------------------------
# # Tool: List Channels
# # ---------------------------
# @mcp.tool()
# def list_channels() -> str:
#     url = "https://slack.com/api/conversations.list?types=public_channel,private_channel,im,mpim&limit=1000"
#     res = requests.get(url, headers=HEADERS).json()
#     if not res.get("ok"):
#         return f"Error fetching channels: {res.get('error')}"
#     channels = []
#     for ch in res.get("channels", []):
#         ch_type = "DM" if ch.get("is_im") else "MPIM" if ch.get("is_mpim") else "Private" if ch.get("is_private") else "Public"
#         name = ch.get("name") or f"DM/{USER_MAP.get(ch.get('user'), ch.get('user'))}"
#         channels.append(f"{name} ({ch_type}) → ID: {ch['id']}")
#     return "\n".join(channels)

# # ---------------------------
# # Tool: Fetch Messages (returns tuple: ok(bool), payload(str))
# # ---------------------------
# def _fetch_messages_raw(channel_id: str, limit: int = 20):
#     url = f"https://slack.com/api/conversations.history?channel={channel_id}&limit={limit}"
#     res = requests.get(url, headers=HEADERS).json()
#     return res

# @mcp.tool()
# def fetch_messages(channel_id: str, limit: int = 20) -> str:
#     """Fetch messages from a given Slack channel or DM."""
#     res = _fetch_messages_raw(channel_id, limit=limit)
#     if not res.get("ok"):
#         return f"Error fetching messages: {res.get('error')}"
#     messages = []
#     for msg in res.get("messages", []):
#         user_id = msg.get("user")
#         user_name = USER_MAP.get(user_id, user_id) if user_id else "Unknown"
#         text = msg.get("text", "")
#         ts = msg.get("ts", "")
#         messages.append(f"[{ts}] {user_name}: {text}")
#     return "\n".join(messages)

# # ---------------------------
# # Resource: Greeting
# # ---------------------------
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     return f"Hello, {name}! I can help you fetch Slack messages and channels."

# # ---------------------------
# # Auto Fetch Messages with auto-join
# # ---------------------------
# def auto_fetch_messages(interval=15, limit=5):
#     """
#     Automatically fetch latest messages from all channels every `interval` seconds.
#     Will attempt to join public channels that return not_in_channel.
#     """
#     print(f"Starting auto-fetching messages every {interval} seconds...\n")

#     while True:
#         try:
#             # Get all channels
#             list_url = "https://slack.com/api/conversations.list?types=public_channel,private_channel,im,mpim&limit=1000"
#             list_res = requests.get(list_url, headers=HEADERS).json()
#             if not list_res.get("ok"):
#                 print("Failed to list channels:", list_res.get("error"))
#                 time.sleep(interval)
#                 continue

#             for ch in list_res.get("channels", []):
#                 ch_type = "DM" if ch.get("is_im") else "MPIM" if ch.get("is_mpim") else "Private" if ch.get("is_private") else "Public"
#                 ch_name = ch.get("name") or f"DM/{USER_MAP.get(ch.get('user'), ch.get('user'))}"
#                 ch_id = ch['id']

#                 # Fetch last messages
#                 res = _fetch_messages_raw(ch_id, limit=limit)
#                 if not res.get("ok"):
#                     err = res.get("error")
#                     # If not in channel and channel is public, try to join and retry once
#                     if err == "not_in_channel" and ch_type == "Public":
#                         print(f"Not in public channel {ch_name} ({ch_id}). Attempting to join...")
#                         joined = join_channel(ch_id)
#                         if joined:
#                             print(f"Joined {ch_name} ({ch_id}). Retrying fetch...")
#                             # retry once
#                             res_retry = _fetch_messages_raw(ch_id, limit=limit)
#                             if res_retry.get("ok"):
#                                 print(f"--- {ch_name} ({ch_type}) ---")
#                                 for msg in res_retry.get("messages", []):
#                                     user_id = msg.get("user")
#                                     user_name = USER_MAP.get(user_id, user_id) if user_id else "Unknown"
#                                     print(f"[{msg.get('ts')}] {user_name}: {msg.get('text','')}")
#                                 print("\n")
#                                 continue
#                             else:
#                                 print(f"After join, fetch failed: {res_retry.get('error')}")
#                                 continue
#                         else:
#                             print(f"Could not join public channel {ch_name} ({ch_id}). Skipping.")
#                             continue
#                     # If private and not_in_channel: tell user to invite bot
#                     elif err == "not_in_channel" and ch_type == "Private":
#                         print(f"Bot is not a member of private channel {ch_name} ({ch_id}). Invite the bot to that channel to fetch messages.")
#                         continue
#                     else:
#                         print(f"Error fetching messages for {ch_name} ({ch_id}): {err}")
#                         continue

#                 # OK response, print messages
#                 print(f"--- {ch_name} ({ch_type}) ---")
#                 for msg in res.get("messages", []):
#                     user_id = msg.get("user")
#                     user_name = USER_MAP.get(user_id, user_id) if user_id else "Unknown"
#                     print(f"[{msg.get('ts')}] {user_name}: {msg.get('text','')}")
#                 print("\n")

#             time.sleep(interval)

#         except KeyboardInterrupt:
#             print("Stopping auto-fetch.")
#             break
#         except Exception as e:
#             print(f"Unexpected error in auto-fetch: {e}")
#             time.sleep(interval)

# # ---------------------------
# # Run MCP server + Auto Fetch
# # ---------------------------
# if __name__ == "__main__":
#     mcp.run(transport="http",
#         host="127.0.0.1",
#         port= 8001,
#         path="/mcp",
#     )

