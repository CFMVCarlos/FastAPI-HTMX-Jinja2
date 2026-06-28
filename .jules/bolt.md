## 2024-06-28 - Fast string generation for large WebSocket broadcasts
**Learning:** When sending messages to a massive number of connections (e.g. 10,000 WebSocket clients in FastAPI), doing HTML escaping or string formatting *inside* the loop is a severe bottleneck (O(N) operations).
**Action:** Always pre-compute message payloads outside the loop before starting the broadcast loop. Avoid `asyncio.gather` for the subsequent loop, as it creates too much overhead for simple `send_text` calls.
