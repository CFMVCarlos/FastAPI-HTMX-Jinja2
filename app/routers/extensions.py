import asyncio
import datetime
import time
from typing import List, NoReturn, Optional

from fastapi import APIRouter, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sse_starlette import EventSourceResponse
import logging

router = APIRouter(prefix="/extensions", tags=["EXT"])

# Set up logging
logger = logging.getLogger(__name__)  # Create a logger object for this module
logger.setLevel(logging.INFO)  # Set the logging level to INFO
handler = logging.StreamHandler()  # Create a stream handler to output logs to the console
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Define the log message format
handler.setFormatter(formatter)  # Set the formatter for the handler
logger.addHandler(handler)  # Add the handler to the logger

# --------------------------------------------------------------------------------
# SSE Event Triggered Route
# --------------------------------------------------------------------------------
@router.get("/sse_event_triggered", response_class=HTMLResponse)
async def sse_event_triggered(
    request: Request, dataFromSSE: Optional[str] = None
) -> HTMLResponse:
    """
    Endpoint to trigger SSE event. It returns the data sent from SSE, if provided.
    """
    return HTMLResponse(content=dataFromSSE or "No data provided")


# --------------------------------------------------------------------------------
# Streaming Events Route (Server-Sent Events)
# --------------------------------------------------------------------------------
@router.get("/stream")
async def message_stream(request: Request) -> EventSourceResponse:
    """
    Streams events to the client using Server-Sent Events (SSE).
    Generates new messages every second.
    """
    async def event_generator():
        count = 0
        while True:
            # If the client disconnects, stop the event stream
            if await request.is_disconnected():
                break

            count += 1
            # Send a message every second (e.g., every 1 count)
            if count % 1 == 0:
                yield {
                    "event": "sse_event",
                    "data": f"<div>SSE Content right here boys {count}</div>",
                }

            # Every 10 counts, send a special message
            if count % 10 == 0:
                yield {
                    "event": "sse_event_10",
                    "data": f"<div>SSE 10 Content right here boys {int(count/10)}</div>",
                }

            # Sleep for 1 second before sending the next message
            await asyncio.sleep(1)

    return EventSourceResponse(event_generator(), media_type="text/event-stream")


# --------------------------------------------------------------------------------
# WebSocket Route
# --------------------------------------------------------------------------------
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    """
    Handles WebSocket connections. Receives JSON messages from the client
    and sends them to all connected clients.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Wait for the client to send a message (JSON format)
            msg = await websocket.receive_json()
            # Send the message to all connected clients
            await manager.send_message(msg["chat_message"])
    except WebSocketDisconnect:
        # Handle client disconnection
        logger.info("Client has disconnected.")
    except Exception as e:
        # Handle any unexpected errors
        logger.error(f"Error Occurred: {e}")
    finally:
        # Ensure the client is disconnected properly
        await manager.disconnect(websocket)


# --------------------------------------------------------------------------------
# Loading States Route (POST)
# --------------------------------------------------------------------------------
@router.post("/loading_states", response_class=Response)
async def post_loading_states(request: Request) -> Response:
    """
    Simulates a loading state by introducing a delay.
    Typically used when performing a time-consuming task.
    """
    time.sleep(5)  # Simulate a delay of 5 seconds
    return Response(status_code=204)  # No content to return


# --------------------------------------------------------------------------------
# Loading States Route (GET)
# --------------------------------------------------------------------------------
@router.get("/loading_states", response_class=HTMLResponse)
async def get_loading_states(request: Request) -> HTMLResponse:
    """
    Returns a simple HTML button that simulates a loading state when clicked.
    """
    html_content: str = """
        Click me for preload (Swapped)
        """
    return HTMLResponse(content=html_content)


# --------------------------------------------------------------------------------
# Path Dependencies Route (GET)
# --------------------------------------------------------------------------------
@router.get("/path_deps", response_class=HTMLResponse)
async def get_path_deps(request: Request) -> HTMLResponse:
    """
    Returns a simple HTML list item.
    This is an example of a path dependency in a route.
    """
    html_content: str = """
        <li>Path Deps</li>
    """
    return HTMLResponse(content=html_content)


# --------------------------------------------------------------------------------
# Path Dependencies Route (POST)
# --------------------------------------------------------------------------------
@router.post("/path_deps", response_class=HTMLResponse)
async def post_path_deps(request: Request) -> HTMLResponse:
    """
    Returns an HTML button that can be used to post more data to the list.
    The button will not trigger a page reload and uses hx-swap for dynamic content update.
    """
    html_content: str = """
        <button hx-post="/path_deps" hx-swap="none">Post more to the list</button>
    """
    return HTMLResponse(content=html_content)


# --------------------------------------------------------------------------------
# Sweet Alert Confirmation Route (GET)
# --------------------------------------------------------------------------------
@router.get("/sweet_alert_confirmed", response_class=HTMLResponse)
async def sweet_alert_confirmed(request: Request) -> HTMLResponse:
    """
    Returns a confirmation message when a sweet alert is confirmed.
    """
    html_content: str = """
        Sweet Alert Confirmed
    """
    return HTMLResponse(content=html_content)


# --------------------------------------------------------------------------------
# SSE Connection Manager (Handles WebSocket connections)
# --------------------------------------------------------------------------------
class ConnectionManager:
    def __init__(self):
        """
        Initializes the connection manager with an empty list of active connections.
        """
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> NoReturn:
        """
        Accepts a WebSocket connection and adds it to the list of active connections.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> NoReturn:
        """
        Removes the WebSocket connection from the list of active connections.
        """
        self.active_connections.remove(websocket)

    async def send_message(self, message: str) -> NoReturn:
        """
        Sends a message to all active WebSocket connections. Formats the message with a timestamp.
        """
        for connection in self.active_connections:
            # Format the current time
            formatted_time: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content: str = f"""
                <div hx-swap-oob="beforeend:#content">
                <p>{formatted_time} || {message}</p>
                </div>
                <input hx-swap-oob="outerHTML:#web_socket_input" id="web_socket_input" name="chat_message" placeholder="Web Socket Phrase"/>
            """
            await connection.send_text(content)

# Initialize the connection manager instance
manager: ConnectionManager = ConnectionManager()
