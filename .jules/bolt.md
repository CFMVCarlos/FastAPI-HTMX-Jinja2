## 2023-11-13 - WebSocket Broadcast O(N) Formatting Optimization
**Learning:** Found an O(N) bottleneck in WebSocket broadcasting where identical string interpolation (including datetime and HTML escaping) was computed repeatedly inside a loop per client connection. This caused high overhead for large numbers of connections.
**Action:** Always hoist identical string formatting and processing outside of loops that iterate over large collections (e.g., active WebSocket connections) to convert O(N) formatting into O(1) before a simple send loop.
