import asyncio
import random
from typing import Optional

from fastapi import APIRouter, Request, Response
from fastapi.responses import FileResponse, HTMLResponse

# Create an APIRouter instance for the built-in routes
router = APIRouter(prefix="/builtin", tags=["Builtin"])


@router.post(
    "/button_click/{color}",
    summary="Change the color of paragraph.",
    response_class=HTMLResponse,
)
async def button_click(request: Request, color: Optional[str] = "red"):
    """
    Endpoint to change the color of a paragraph element when a button is clicked.
    The color is passed as a parameter (default is red).
    """
    response = f"""
        <p id="p1" class="smooth {color}">This is my HTML template.</p>
    """
    return HTMLResponse(content=response, status_code=200)


@router.get(
    "/element",
    summary="Add a new element to the end of the body and swap a div using hx-swap-oob",
    response_class=HTMLResponse,
)
async def element(request: Request):
    """
    Endpoint to add a new element to the page and swap a div element
    using the hx-swap-oob feature.
    """
    response = """
        <p class="fade-me-in">This is a new element.</p>
        <div id="message" hx-swap-oob="true">Swap me directly using hx-swap-oob in the response!</div>
    """
    return HTMLResponse(content=response, status_code=200)


@router.get(
    "/select_element",
    summary="Select a particular element from the response",
    response_class=HTMLResponse,
)
async def select_element(request: Request):
    """
    Endpoint that returns multiple elements and allows the client
    to select specific elements.
    """
    response = """
        <p id="select_p">Paragraph</p>
        <div id="select_div">Div</div>
        <h id="select_h">Header</h>
    """
    return HTMLResponse(content=response, status_code=200)


@router.get(
    "/select_element_oob",
    summary="Select a particular element from the response to change the button and other OOB elements",
    response_class=HTMLResponse,
)
async def select_element_oob(request: Request) -> HTMLResponse:
    """
    Endpoint that selects elements from the response and modifies a button and other out-of-band (OOB) elements.
    """
    response = """
        <p id="select_p">Paragraph</p>
        <p id="p1">This paragraph was changed using hx-select-oob in the request</p>
        <div id="select_div">Div</div>
        <h1 id="select_h1" classes="add red:2s">Header was changed</h1>
        <span id="select_button_oob">Button Swapped</span>
    """
    return HTMLResponse(content=response, status_code=200)


@router.post(
    "/include",
    summary="Include extra information in the body of the request",
    response_class=HTMLResponse,
)
async def include(request: Request) -> HTMLResponse:
    """
    Endpoint to include extra information in the request body.
    """
    body = await request.body()
    _, value = body.decode().split("=")

    response = f"""
        Include information ({value})
    """
    return HTMLResponse(content=response, status_code=200)


@router.get(
    "/vals_example",
    summary="Add information in the request",
    response_class=HTMLResponse,
)
async def vals_example(request: Request, lastKey: str, extra_info: str) -> HTMLResponse:
    """
    Example endpoint that adds information in the request, checks for forbidden keys,
    and returns data based on the last key pressed.
    """
    forbidden_keys = forbidden_keys_list()
    if lastKey not in forbidden_keys:
        response = f"""
            <div>Last Key pressed: {lastKey}. {extra_info}</div>
        """
        return HTMLResponse(content=response, status_code=200)
    return HTMLResponse(status_code=204)


def forbidden_keys_list():
    """
    Returns a list of forbidden keys that should not trigger the endpoint.
    """
    forbidden_keys = [
        "undefined", "Enter", "Shift", "CapsLock", "Control", "Alt", "Meta",
        "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Backspace", "Delete",
        "Insert", "Home", "End", "PageUp", "PageDown", "Tab", "Escape", "F1",
        "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
        "ScrollLock", "Pause", "ContextMenu", "PrintScreen", "NumLock", "Clear",
    ]
    return forbidden_keys


@router.get(
    "/beautiful_div", summary="Returns divs with content", response_class=HTMLResponse
)
async def beautiful_div(request: Request) -> HTMLResponse:
    """
    Endpoint to return a beautiful div with content.
    """
    response = """
        <div>Beautiful Div Here</div>
    """
    return HTMLResponse(content=response, status_code=200)


ALLOW_RESPONSE_CHANGE: bool = False


@router.post(
    "/response_allow",
    summary="Changes the state of the variable ALLOW_RESPONSE_CHANGE",
    response_class=Response,
)
async def response_allow(request: Request) -> Response:
    """
    Endpoint to toggle the ALLOW_RESPONSE_CHANGE variable to enable or disable response changes.
    """
    global ALLOW_RESPONSE_CHANGE
    ALLOW_RESPONSE_CHANGE = not ALLOW_RESPONSE_CHANGE
    return Response(status_code=204)


@router.post(
    "/response_change",
    summary="Returns a text with random numbers when the state is True",
    response_class=Response,
)
async def response_change(request: Request) -> Response:
    """
    Endpoint that returns a text with a random number if ALLOW_RESPONSE_CHANGE is True.
    If False, it returns a 204 status (no content).
    """
    if not ALLOW_RESPONSE_CHANGE:
        return Response(status_code=204)

    random_number = random.randint(0, 100)
    response = f"Text Changed to number {random_number}"
    return Response(response, status_code=200)


@router.get(
    "/info", summary="Does not return anything but a OK status", response_class=Response
)
async def info(request: Request) -> Response:
    """
    Endpoint that returns an OK status (204) without any content.
    """
    return Response(status_code=204)


@router.get(
    "/htmx_headers",
    summary="Returns headers from the request",
    response_class=HTMLResponse,
)
async def htmx_headers(request: Request) -> HTMLResponse:
    """
    Endpoint that checks for the presence of a specific HTMX header and returns a response based on it.
    """
    await asyncio.sleep(1)
    if request.headers.get("HX-Trigger") == "htmx_header_button_id":
        response = """
            Correct button was selected based on HTMX Request Headers
        """
        return HTMLResponse(content=response, status_code=200)

    return HTMLResponse(status_code=200)


@router.get("/file_download", summary="Download a file", response_class=Response)
async def file_download(request: Request) -> Response:
    """
    Endpoint to trigger the download of a file (e.g., an image).
    """
    file_path = "static/img/trollface.png"
    return FileResponse(file_path, media_type="image/png", status_code=200)


@router.get(
    "/sync_first",
    summary="Does not return anything but a OK status",
    response_class=HTMLResponse,
)
async def sync_first(request: Request) -> HTMLResponse:
    """
    Simulate a slow operation and return a response indicating the first sync button was clicked.
    """
    await asyncio.sleep(2)  # Simulating some slow operation
    response = "First sync button won"
    return HTMLResponse(content=response, status_code=200)


@router.get(
    "/sync_second",
    summary="Does not return anything but a OK status",
    response_class=HTMLResponse,
)
async def sync_second(request: Request) -> HTMLResponse:
    """
    Simulate a slow operation and return a response indicating the second sync button was clicked.
    """
    await asyncio.sleep(2)  # Simulating some slow operation
    response = "Second sync button won"
    return HTMLResponse(content=response, status_code=200)


COUNT = 0


@router.get(
    "/server_event_trigger",
    summary="Trigger a server event",
    response_class=HTMLResponse,
)
def server_event_trigger(request: Request) -> HTMLResponse:
    """
    Trigger a server event when the COUNT variable reaches 5.
    The event is sent to the client via HX-Trigger header.
    """
    global COUNT
    COUNT += 1
    response = HTMLResponse(status_code=204)
    if COUNT == 5:
        COUNT = 0
        response.headers["HX-Trigger"] = "server_event_triggered"
    return response
