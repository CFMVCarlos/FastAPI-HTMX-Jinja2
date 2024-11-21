import pytest
from app.main import app
from fastapi.testclient import TestClient


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


def test_vals_example(client):
    """Test query parameters and ensure proper rendering of dynamic content."""
    response = client.get("/builtin/vals_example?lastKey=A&extra_info=Extra")
    assert response.status_code == 200  # Check if the request is successful
    assert b"<div>Last Key pressed: A. Extra</div>" in response.content  # Ensure dynamic content is rendered correctly


# --------------------------------------------------------------------------------
# Test Dynamic Content and SSE
# --------------------------------------------------------------------------------

def test_beautiful_div(client):
    """Test if a beautiful div is rendered correctly."""
    response = client.get("/builtin/beautiful_div")
    assert response.status_code == 200  # Check if the request is successful
    assert b"<div>Beautiful Div Here</div>" in response.content  # Check if the div content is rendered


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


def test_path_deps(client):
    """Test path dependencies."""
    response = client.get("/extensions/path_deps")
    assert response.status_code == 200  # Ensure status is 200
    assert b"<li>Path Deps</li>" in response.content  # Check if the content is rendered properly


# --------------------------------------------------------------------------------
# Test Miscellaneous Functionality
# --------------------------------------------------------------------------------

def test_info(client):
    """Test the /info endpoint."""
    response = client.get("/builtin/info")
    assert response.status_code == 204  # Ensure the status is 204


def test_sweet_alert_confirmed(client):
    """Test if sweet alert is confirmed."""
    response = client.get("/extensions/sweet_alert_confirmed")
    assert response.status_code == 200  # Ensure status is 200
    assert b"Sweet Alert Confirmed" in response.content  # Ensure Sweet Alert confirmation message appears
