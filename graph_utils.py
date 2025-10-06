# graph_utils.py
GRAPH_BASE = os.getenv("GRAPH_BASE", "https://graph.microsoft.com/v1.0")
SCOPE = [os.getenv("GRAPH_SCOPE", "https://graph.microsoft.com/.default")]


if not (TENANT_ID and CLIENT_ID and CLIENT_SECRET):
log.warning("Some Azure credentials are missing; set them in .env or environment variables")


_app = msal.ConfidentialClientApplication(
client_id=CLIENT_ID,
client_credential=CLIENT_SECRET,
authority=f"https://login.microsoftonline.com/{TENANT_ID}"
)




def acquire_token() -> str:
"""Acquire an app-only access token via client credentials."""
result = _app.acquire_token_for_client(scopes=SCOPE)
if "access_token" in result:
return result["access_token"]
raise RuntimeError(f"Failed to acquire token: {result}")




def graph_get(path: str, params: Optional[dict] = None) -> Dict[str, Any]:
"""GET wrapper for Microsoft Graph API.


`path` can be either a full URL (starting with https://) or a path under v1.0.
"""
token = acquire_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}


if path.startswith("http"):
url = path
else:
url = urljoin(GRAPH_BASE + '/', path.lstrip('/'))


r = requests.get(url, headers=headers, params=params or {})
if r.status_code >= 400:
# helpful error content
log.error("Graph GET %s returned %s: %s", url, r.status_code, r.text)
r.raise_for_status()
return r.json()




def iterate_paged(path: str, params: Optional[dict] = None) -> Iterator[Dict[str, Any]]:
"""Yield items across paged Graph responses honoring `@odata.nextLink`."""
data = graph_get(path, params=params)
items = data.get("value", [])
for it in items:
yield it
next_link = data.get("@odata.nextLink")
while next_link:
data = graph_get(next_link)
items = data.get("value", [])
for it in items:
yield it
next_link = data.get("@odata.nextLink")