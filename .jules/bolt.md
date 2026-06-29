## 2024-06-25 - Avoid `asyncio.gather` for Mass Broadcasting
**Learning:** In a FastAPI app with Starlette WebSockets (`ConnectionManager` pattern), using `asyncio.gather` to parallelize `await connection.send_text()` across 10,000 active connections is significantly slower (taking ~10.9s vs ~0.15s) compared to sequential `await`s. This is likely due to the enormous overhead of creating and scheduling 10,000 individual task wrappers.
**Action:** When broadcasting messages to a large pool of WebSocket connections, keep the code simple with sequential `await`s in a loop, and ensure the message payload creation (formatting, HTML escaping, string interpolation) is strictly performed *once* outside of the broadcast loop.
## 2024-11-21 - [FastAPI Starlette Websocket HTML O(N) Formatting]
**Learning:** Inside `ConnectionManager.send_message()`, the HTML payload dynamically sent to clients inside `for connection in self.active_connections` contained a static format operation using `datetime.datetime.now().strftime(...)` and `html.escape()`. In FastAPI/Starlette, this resulted in thousands of repeated string allocations per broadcast request, bottlenecking performance from ~5 seconds down to ~0.15s for 100 broadcasts to 10k users.
**Action:** When working on broadcast functions for WebSockets, ensure string allocations, encoding, formatting, and HTML construction occur ONCE outside the iteration loop, rather than redundantly for every connection.

## 2024-11-21 - [FastAPI Starlette `isinstance` Optimization Fix]
**Learning:** `FORBIDDEN_KEYS` was already correctly optimized to a `frozenset()` but the Pytest suite `test_app.py::test_forbidden_keys_list` contained `assert isinstance(keys, list)` which failed the CI check, breaking the test suite when the list was updated.
**Action:** Verify that pre-existing O(1) structures correctly match the associated pytest verification layers.
## 2024-06-28 - Fast string generation for large WebSocket broadcasts
**Learning:** When sending messages to a massive number of connections (e.g. 10,000 WebSocket clients in FastAPI), doing HTML escaping or string formatting *inside* the loop is a severe bottleneck (O(N) operations).
**Action:** Always pre-compute message payloads outside the loop before starting the broadcast loop. Avoid `asyncio.gather` for the subsequent loop, as it creates too much overhead for simple `send_text` calls.

## 2023-11-13 - WebSocket Broadcast O(N) Formatting Optimization
**Learning:** Found an O(N) bottleneck in WebSocket broadcasting where identical string interpolation (including datetime and HTML escaping) was computed repeatedly inside a loop per client connection. This caused high overhead for large numbers of connections.
**Action:** Always hoist identical string formatting and processing outside of loops that iterate over large collections (e.g., active WebSocket connections) to convert O(N) formatting into O(1) before a simple send loop.
