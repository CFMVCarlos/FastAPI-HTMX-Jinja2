## 2024-06-28 - Fast string generation for large WebSocket broadcasts
**Learning:** When sending messages to a massive number of connections (e.g. 10,000 WebSocket clients in FastAPI), doing HTML escaping or string formatting *inside* the loop is a severe bottleneck (O(N) operations).
**Action:** Always pre-compute message payloads outside the loop before starting the broadcast loop. Avoid `asyncio.gather` for the subsequent loop, as it creates too much overhead for simple `send_text` calls.

## 2023-11-13 - WebSocket Broadcast O(N) Formatting Optimization
**Learning:** Found an O(N) bottleneck in WebSocket broadcasting where identical string interpolation (including datetime and HTML escaping) was computed repeatedly inside a loop per client connection. This caused high overhead for large numbers of connections.
**Action:** Always hoist identical string formatting and processing outside of loops that iterate over large collections (e.g., active WebSocket connections) to convert O(N) formatting into O(1) before a simple send loop.
