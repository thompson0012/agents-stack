# Long-Running Backend Servers

Run a real server process (FastAPI, Express, Flask, etc.) inside the sandbox and connect it to your frontend via port forwarding. Use this when you need:

- WebSocket or SSE streaming
- In-memory state across requests
- Framework features (middleware, dependency injection, ORMs)
- Background tasks or scheduled work
- Multiple related endpoints with shared state
- LLM or media generation (text, image, video, audio) — **read `shared/20-llm-api.md`** for all available APIs, helpers, and usage examples

## How It Works

1. Write a server that listens on a port (e.g., 8000)
2. Start it as a background process in the sandbox with `api_credentials=["llm-api:website"]` if it needs LLM/media access
3. After testing locally, use `__PORT_8000__` in your frontend code — `deploy_website` replaces it with the real proxy path at deploy time
4. All traffic flows through the same JWT-authenticated proxy as static assets

## Visitor Data Isolation

The proxy injects an `X-Visitor-Id` header on every request (HTTP and WebSocket) that identifies the browser. Sites run in sandboxed iframes where cookies, localStorage, and sessionStorage are all unavailable — this header is the only way to distinguish visitors.

Use it when the site stores visitor-created content. Read-only content that the agent authored does not need per-visitor scoping.

## Step-by-Step

### 1. Write the Server

Create a standard server in your project directory. Example with FastAPI:

```python
#!/usr/bin/env python3
"""api_server.py — runs on port 8000 inside the sandbox."""
import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

db = sqlite3.connect("data.db", check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

@asynccontextmanager
async def lifespan(app):
    yield
    db.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Item(BaseModel):
    name: str

@app.get("/api/items")
def list_items():
    rows = db.execute("SELECT id, name, created_at FROM items ORDER BY id").fetchall()
    return [{"id": r[0], "name": r[1], "created_at": r[2]} for r in rows]

@app.post("/api/items", status_code=201)
def create_item(item: Item):
    cur = db.execute("INSERT INTO items (name) VALUES (?)", [item.name])
    db.commit()
    return {"id": cur.lastrowid, "name": item.name}

@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    db.execute("DELETE FROM items WHERE id = ?", [item_id])
    db.commit()
    return {"deleted": item_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. Start the Server

Pre-installed in the sandbox: `fastapi`, `uvicorn`, `flask`, `websockets` (Python); `express`, `socket.io` (Node).

```
start_server(command="python api_server.py", project_path="/home/user/workspace/my-project", port=8000, api_credentials=["llm-api:website"])
```

`start_server` kills any existing process on the port, starts the command in the background, and polls until the port is listening (up to 60s). It returns the PID, URL, and recent logs — no manual health check needed.

Use `api_credentials=["llm-api:website"]` when the server calls any LLM or media generation API (Anthropic SDK, image/video/audio generation, etc.). This injects credentials as environment variables. Use `:website` for long-lived website backend servers. Omit secrets entirely if the server doesn't need LLM access. **Read `shared/20-llm-api.md`** for available models, async SDK helpers, and usage examples.

**Billing note:** When a deployed website uses LLM or media generation APIs, each request consumes credits billed to the user. The site starts private but can be shared publicly — if shared, all visitors' usage is billed to the user. Before building the website, you MUST use `confirm_action` to warn about this. The confirmation should warn that usage costs credits and that if the site is shared publicly, visitors' usage is also billed to the user. Keep it concise — use "Build website" as the accept label.

**Sharing note:** When a deployed website uses external tool connectors, the connectors are accessible to anyone who can reach the site. Before building the website, you MUST use `confirm_action` to warn that if the site is shared publicly, visitors will be able to trigger the user's connected tools. Keep it concise — use "Build website" as the accept label.

### 3. Connect the Frontend

Set the API base URL dynamically so it works both during local testing and after deployment. `__PORT_8000__` is replaced with `port/8000` at deploy time by `deploy_website`.

```js
// Works locally (http://localhost:8000) AND after deploy (port/8000 via proxy)
const API = "__PORT_8000__".startsWith("__") ? "http://localhost:8000" : "__PORT_8000__";

async function loadItems() {
  const res = await fetch(`${API}/api/items`);
  return res.json();
}

async function addItem(name) {
  const res = await fetch(`${API}/api/items`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  return res.json();
}
```

### 4. Deploy

Deploy with `deploy_website` as usual. The proxy handles routing:
- `/port/8000/api/items` → forwarded to the sandbox server on port 8000
- `/index.html`, `/style.css` → served from S3

## WebSocket Example

Server (Python with websockets):

```python
#!/usr/bin/env python3
import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"echo: {message}")

async def main():
    async with websockets.serve(echo, "0.0.0.0", 8000):
        await asyncio.Future()

asyncio.run(main())
```

Client:

```js
const ws = new WebSocket(`${location.origin}${location.pathname.replace(/\/[^/]*$/, '')}/__PORT_8000__/ws`);
```

For WebSocket, construct the URL relative to the current page origin and path prefix so it routes through the same proxy.

## Express.js Example

```js
// server.js
const express = require("express");
const app = express();
app.use(express.json());

let items = [];
let nextId = 1;

app.get("/api/items", (req, res) => res.json(items));
app.post("/api/items", (req, res) => {
  const item = { id: nextId++, ...req.body };
  items.push(item);
  res.status(201).json(item);
});

app.listen(8000, "0.0.0.0", () => console.log("listening on 8000"));
```

```
start_server(command="node server.js", project_path="/home/user/workspace/my-project", port=8000)
```

## Multiple Ports

You can run multiple servers on different ports. Use a separate placeholder for each:

```js
const API = "__PORT_8000__";       // REST API
const WS_URL = "__PORT_8001__";    // WebSocket server
```

## Limits

- **Status**: HTTP status code (default: `200`). 5xx codes are clamped to `422` by the proxy — use 4xx codes for errors (e.g., `400`, `404`, `422`)
- **5-minute read timeout** per HTTP request (resets on each chunk — SSE and streaming work indefinitely)
- **10MB max request body**
- **5 retries** with 1s intervals if the backend isn't ready yet (sandbox wake-up)
- SSE (`text/event-stream`), chunked responses, and long-polling all work through the proxy
- WebSocket connections have automatic ping/keepalive (20s interval)
- Server must bind to `0.0.0.0`, not `127.0.0.1` or `localhost`
- Sandbox ports are private — all traffic goes through the authenticated proxy
