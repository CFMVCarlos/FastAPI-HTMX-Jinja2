import asyncio
import time
import datetime
from app.routers.extensions import ConnectionManager

class MockWebSocket:
    async def send_text(self, text: str):
        pass

async def main():
    manager = ConnectionManager()
    # Add many connections
    for _ in range(10000):
        manager.active_connections.append(MockWebSocket())

    start_time = time.perf_counter()
    for _ in range(100):
        await manager.send_message("Test message")
    end_time = time.perf_counter()

    print(f"Time taken for 100 broadcasts to 10,000 connections: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
