import pytest
from app.main import app
from fastapi.testclient import TestClient
from app.routers.builtin import forbidden_keys_list


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def client():
    """Fixture to create a test client for FastAPI app."""
    with TestClient(app) as client:
        yield client


# --------------------------------------------------------------------------------
# Test API Responses and Template Rendering
# --------------------------------------------------------------------------------

def test_read_root(client):
    """Test the root endpoint to check if the template renders properly."""
    response = client.get("/")
    assert response.status_code == 200  # Check if the response status is 200 OK
    assert b"This is my HTML template." in response.content  # Check if the template content is correct


def test_delete_root(client):
    """Test the DELETE request on the root endpoint."""
    response = client.delete("/")
    assert response.status_code == 200  # Ensure the DELETE request is successful


def test_button_click(client):
    """Test button click to see if the proper changes are reflected in the response."""
    response = client.post("/builtin/button_click/red")
    assert response.status_code == 200  # Check if the button click returns status 200
    assert (
        b'<p id="p1" class="smooth red">This is my HTML template.</p>'
        in response.content
    )  # Ensure the HTML content changes after the button click


def test_button_click_xss_mitigation(client):
    """Test button click to ensure XSS payload is properly escaped."""
    import urllib.parse
    payload = "\"><img src=x onerror=alert('XSS')>"
    encoded_payload = urllib.parse.quote(payload, safe="")
    response = client.post(f"/builtin/button_click/{encoded_payload}")
    assert response.status_code == 200
    assert (
        b'<p id="p1" class="smooth &quot;&gt;&lt;img src=x onerror=alert(&#x27;XSS&#x27;)&gt;">This is my HTML template.</p>'
        in response.content
    )  # Ensure HTML payload is escaped


def test_element(client):
    """Test if the new element is successfully added to the response."""
    response = client.get("/builtin/element")
    assert response.status_code == 200  # Check the response status
    assert b'<p class="fade-me-in">This is a new element.</p>' in response.content  # Ensure the new element is added


def test_select_element(client):
    """Test if the select element endpoint renders correctly."""
    response = client.get("/builtin/select_element")
    assert response.status_code == 200  # Check if the request is successful
    assert b'<p id="select_p">Paragraph</p>' in response.content  # Check if the correct content is rendered


def test_select_element_oob(client):
    """Test out-of-band update for the select element."""
    response = client.get("/builtin/select_element_oob")
    assert response.status_code == 200  # Check if the request is successful
    assert b'<p id="select_p">Paragraph</p>' in response.content  # Check if the content is updated correctly


# --------------------------------------------------------------------------------
# Test Post and Include Functionalities
# --------------------------------------------------------------------------------

def test_include(client):
    """Test if the include functionality properly reflects the form input."""
    response = client.post("/builtin/include", data={"include_input": "test"})
    assert response.status_code == 200  # Ensure the response is successful
    assert (
        b'Include information (test)' in response.content
    )  # Check if the input is properly reflected in the response


def test_include_xss(client):
    """Test that XSS payload in include endpoint is properly HTML-escaped."""
    response = client.post("/builtin/include", content=b"include_input=<script>alert(1)</script>")
    assert response.status_code == 200
    # Payload should be escaped
    assert b"&lt;script&gt;alert(1)&lt;/script&gt;" in response.content
    # Raw payload should NOT be present
    assert b"<script>alert(1)</script>" not in response.content


def test_vals_example(client):
    """Test query parameters and ensure proper rendering of dynamic content."""
    response = client.get("/builtin/vals_example?lastKey=A&extra_info=Extra")
    assert response.status_code == 200  # Check if the request is successful
    assert b"<div>Last Key pressed: A. Extra</div>" in response.content  # Ensure dynamic content is rendered correctly


def test_vals_example_xss(client):
    """Test query parameters to ensure XSS payload is escaped."""
    response = client.get("/builtin/vals_example?lastKey=<script>alert('xss')</script>&extra_info=<img src=x onerror=alert('xss')>")
    assert response.status_code == 200
    assert b"&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;" in response.content
    assert b"&lt;img src=x onerror=alert(&#x27;xss&#x27;)&gt;" in response.content
    assert b"<script>" not in response.content


# --------------------------------------------------------------------------------
# Test Dynamic Content and SSE
# --------------------------------------------------------------------------------

def test_beautiful_div(client):
    """Test if a beautiful div is rendered correctly."""
    response = client.get("/builtin/beautiful_div")
    assert response.status_code == 200  # Check if the request is successful
    assert b"<div>Beautiful Div Here</div>" in response.content  # Check if the div content is rendered


def test_sse_event_triggered_extension(client):
    """Test if the SSE event triggered endpoint returns the correct content."""
    # Test without dataFromSSE parameter
    response = client.get("/extensions/sse_event_triggered")
    assert response.status_code == 200
    assert b"No data provided" in response.content

    # Test with dataFromSSE parameter
    response = client.get("/extensions/sse_event_triggered?dataFromSSE=Custom+data")
    assert response.status_code == 200
    assert b"Custom data" in response.content
def test_sse_event_triggered_xss(client):
    """Test that the /extensions/sse_event_triggered endpoint escapes HTML to prevent XSS."""
    malicious_payload = "<script>alert(1)</script>"
    response = client.get(f"/extensions/sse_event_triggered?dataFromSSE={malicious_payload}")
    assert response.status_code == 200
    # Make sure the raw malicious payload is not present
    assert b"<script>alert(1)</script>" not in response.content
    # Make sure the escaped payload is present
    assert b"&lt;script&gt;alert(1)&lt;/script&gt;" in response.content


def test_sse_event_triggered(client):
    """Test that the server event is triggered after the COUNT reaches 5."""
    # Make 4 requests to increment COUNT up to 4 (since the event is triggered on the 5th request)
    for _ in range(4):
        response = client.get("/builtin/server_event_trigger")
        assert response.status_code == 204  # Ensure the status is 204 for normal requests
        assert "HX-Trigger" not in response.headers  # Ensure HX-Trigger is not set until COUNT reaches 5

    # Make the 5th request to trigger the event
    response = client.get("/builtin/server_event_trigger")
    
    # Check that the status is 204 and the HX-Trigger header is set
    assert response.status_code == 204
    assert "HX-Trigger" in response.headers  # Ensure HX-Trigger is present
    assert response.headers["HX-Trigger"] == "server_event_triggered"  # Verify the correct event name


@pytest.mark.anyio
async def test_message_stream():
    """Test the SSE message stream endpoint generator directly."""
    from app.routers.extensions import message_stream

    class MockRequest:
        def __init__(self):
            self.disconnected = False
        async def is_disconnected(self):
            return self.disconnected

    request = MockRequest()
    response = await message_stream(request)
    iterator = response.body_iterator

    # Test first event
    item1 = await anext(iterator)
    assert item1['event'] == 'sse_event'
    assert item1['data'] == '<div>SSE Content right here boys 1</div>'

    # Test disconnecting stops generator
    request.disconnected = True
    try:
        await anext(iterator)
        assert False, "Should have raised StopAsyncIteration"
    except StopAsyncIteration:
        pass


@pytest.mark.anyio
async def test_message_stream_special_message():
    """Test that the SSE message stream sends a special message every 10 counts."""
    from app.routers.extensions import message_stream
    from unittest.mock import patch

    # Mock asyncio.sleep to run the test quickly without actually waiting 10 seconds
    with patch("asyncio.sleep", return_value=None):
        class MockRequest:
            def __init__(self):
                self.disconnected = False
            async def is_disconnected(self):
                return self.disconnected

        request = MockRequest()
        response = await message_stream(request)
        iterator = response.body_iterator

        # Fast forward through first 9 events
        for i in range(1, 10):
            item = await anext(iterator)
            assert item['event'] == 'sse_event'
            assert item['data'] == f'<div>SSE Content right here boys {i}</div>'

        # The 10th count yields two events: one for % 1 == 0, one for % 10 == 0
        item = await anext(iterator)
        assert item['event'] == 'sse_event'
        assert item['data'] == '<div>SSE Content right here boys 10</div>'

        item = await anext(iterator)
        assert item['event'] == 'sse_event_10'
        assert item['data'] == '<div>SSE 10 Content right here boys 1</div>'

        # Stop generator
        request.disconnected = True
        try:
            await anext(iterator)
            assert False, "Should have raised StopAsyncIteration"
        except StopAsyncIteration:
            pass


# --------------------------------------------------------------------------------
# Test WebSocket Functionality
# --------------------------------------------------------------------------------

def test_websocket_endpoint(client):
    """Test WebSocket communication."""
    with client.websocket_connect("/extensions/ws") as websocket:
        websocket.send_json({"chat_message": "test"})  # Send a test message over WebSocket
        response = websocket.receive_text()  # Receive a message from the WebSocket
        assert "test" in response  # Ensure the received message contains 'test'


# --------------------------------------------------------------------------------
# Test Response and State Changes
# --------------------------------------------------------------------------------

def test_response_allow(client):
    """Test the response for the 'allow' endpoint."""
    response = client.post("/builtin/response_allow")
    assert response.status_code == 204  # Check that the response status is 204 for successful request


def test_response_change(client):
    """Test response change behavior."""
    # test_response_allow was called before this, so ALLOW_RESPONSE_CHANGE should be True
    response = client.post("/builtin/response_change")
    assert response.status_code == 200  # Ensure status is 200 when ALLOW_RESPONSE_CHANGE is True
    assert b"Text Changed to number" in response.content  # Verify the content change

    # Make another request after response_allow, and check if the response status is 204
    response = client.post("/builtin/response_allow")
    assert response.status_code == 204

    # Check response_change after the allow call, expecting status 204
    response = client.post("/builtin/response_change")
    assert response.status_code == 204


def test_loading_states(client):
    """Test if the loading states are rendered correctly."""
    response = client.post("/extensions/loading_states")
    assert response.status_code == 204  # Check if the loading states are handled correctly


def test_get_loading_states(client):
    """Test if the GET loading states endpoint returns the correct HTML content."""
    response = client.get("/extensions/loading_states")
    assert response.status_code == 200
    assert b"Click me for preload (Swapped)" in response.content


def test_path_deps(client):
    """Test path dependencies."""
    response = client.get("/extensions/path_deps")
    assert response.status_code == 200  # Ensure status is 200
    assert b"<li>Path Deps</li>" in response.content  # Check if the content is rendered properly


def test_post_path_deps(client):
    """Test POST request to path dependencies endpoint."""
    response = client.post("/extensions/path_deps")
    assert response.status_code == 200  # Ensure status is 200
    assert b'<button hx-post="/path_deps" hx-swap="none">Post more to the list</button>' in response.content


# --------------------------------------------------------------------------------
# Test Miscellaneous Functionality
# --------------------------------------------------------------------------------

def test_sync_second(client):
    """Test the sync_second endpoint."""
    response = client.get("/builtin/sync_second")
    assert response.status_code == 200
    assert b"Second sync button won" in response.content


def test_info(client):
    """Test the /info endpoint."""
    response = client.get("/builtin/info")
    assert response.status_code == 204  # Ensure the status is 204


def test_forbidden_keys_list():
    """Test if forbidden_keys_list returns the expected list of keys."""
    keys = forbidden_keys_list()
    assert isinstance(keys, (list, set, frozenset, tuple))
    assert len(keys) == 38
    assert "undefined" in keys
    assert "Enter" in keys
    assert "Escape" in keys
    assert "Clear" in keys


def test_sweet_alert_confirmed(client):
    """Test if sweet alert is confirmed."""
    response = client.get("/extensions/sweet_alert_confirmed")
    assert response.status_code == 200  # Ensure status is 200
    assert b"Sweet Alert Confirmed" in response.content  # Ensure Sweet Alert confirmation message appears


def test_sync_first(client):
    """Test the sync_first endpoint."""
    response = client.get("/builtin/sync_first")
    assert response.status_code == 200
    assert b"First sync button won" in response.content
def test_htmx_headers(client):
    """Test the htmx_headers endpoint with and without the HX-Trigger header."""
    # Test without the header
    response = client.get("/builtin/htmx_headers")
    assert response.status_code == 200
    assert b"Correct button was selected" not in response.content

    # Test with the header
    response = client.get(
        "/builtin/htmx_headers", headers={"HX-Trigger": "htmx_header_button_id"}
    )
    assert response.status_code == 200
    assert b"Correct button was selected based on HTMX Request Headers" in response.content
