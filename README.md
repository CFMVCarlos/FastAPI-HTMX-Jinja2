# FastAPI Custom Made

This project showcases a custom implementation using **FastAPI** for backend services and **HTMX** for dynamic web development. It integrates various HTMX features with FastAPI to create a smooth, interactive user experience, enabling server-driven updates without full-page reloads.

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/CFMVCarlos/FastAPI-HTMX-Jinja2
    ```

2. **Navigate to the project directory:**
    ```bash
    cd FastAPI-HTMX-Jinja2
    ```

3. **Install the necessary dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application locally, follow these steps:

1. **Start the FastAPI server:**
    ```bash
    uvicorn app.main:app --reload
    ```

2. **Open your browser and visit:**
    [localhost](http://127.0.0.1:8000)

To run the FastAPI tests, use the following command:

```bash
python -m pytest test_app.py
```

## Features

This project combines **HTMX** with **FastAPI** to deliver an interactive web interface with the following features:

### 1. Built-in HTMX Features

- **Button Click Actions:**
   - Dynamically change text colors (`RED`, `BLUE`, `GREEN`) by sending `hx-post` requests.
   - Changes are reflected on the target element (`#p1`).
  
- **Element Addition:**
   - Add new elements dynamically to the bottom of the page using `hx-swap-oob="true"` and `hx-target="body"`.

- **Element Swapping:**
   - Swap an element's content with the response using `hx-select`.

- **Input Value Inclusion:**
   - Include input field values in requests with `hx-include`.

- **Confirmation Before Action:**
   - Display a confirmation prompt before executing actions like deletions using `hx-confirm`.

- **Boosted Content:**
   - Enhance links and targets for content swapping using `hx-boost="true"`.

- **Loading States:**
   - Implement loading states with custom classes for target elements (`data-loading-states`).

- **Path Dependencies:**
   - Trigger updates based on specific path dependencies using `hx-ext="path-deps"`.

- **Request Synchronization:**
   - Ensure requests run sequentially using `hx-sync`.

- **File Download:**
   - Provide downloadable files through anchor links with `download="surprise_party.png"`.

### 2. HTMX Extensions Features

- **Class Tools Extension:**
   - Toggle classes on elements dynamically (`classes="toggle faded:1s & toggle red:1s"`).

- **Server-Sent Events (SSE):**
   - Implement real-time updates with server streams using `hx-ext="sse"`.

- **WebSockets Extension:**
   - Enable WebSocket connections for live data updates using `hx-ext="ws"`.

- **Advanced Loading States:**
   - Add advanced loading states with delays and class changes during content refreshes.

- **Preload Extension:**
   - Preload content when interacting with specific elements (`preload="mousedown"`).

- **Remove-Me Extension:**
   - Automatically remove elements after a set duration (`remove-me="10s"`).

- **SweetAlert2 Integration:**
   - Use **SweetAlert2** for enhanced confirmation dialogs (`onClick="Swal.fire({...})"`).

- **HTMX Event Handling (`hx-on:*`):**
   - Trigger JavaScript code before and after HTMX requests (`hx-on::before-request`, `hx-on::after-request`).

### 3. Jinja2 Templates

The project utilizes **Jinja2** for dynamic HTML generation. It allows the creation of custom content by rendering variables, loops, and conditionals on the server side, then sending this content to the client.

### 4. FastAPI Pytest Tests

The project includes a comprehensive suite of **FastAPI pytest tests** to verify application functionality. Key tests include:

- **Root and Delete Endpoints:**
   - Test for proper rendering of the root template and handling of DELETE requests.

- **Button Click Behavior:**
   - Ensure that button clicks trigger the expected content changes (e.g., color updates).

- **Element Addition and Swapping:**
   - Validate the addition of new elements and the swapping of content dynamically.

- **Dynamic Content Rendering:**
   - Verify that form inputs and query parameters are properly rendered in response to user interactions.

- **Server-Sent Events (SSE):**
   - Ensure that server events are triggered when a predefined condition is met (e.g., after a certain number of requests).

- **WebSocket Communication:**
   - Confirm WebSocket connections and message exchanges for real-time updates.

- **Response and State Changes:**
   - Ensure that changes to application state (e.g., text updates, status changes) are reflected in real-time.

- **Loading States and Path Dependencies:**
   - Validate loading states and path dependencies to ensure proper content changes are triggered.

- **SweetAlert2 Integration:**
   - Test the integration of SweetAlert2 for confirmation dialogs during interactions.

## Author

- [Carlos Valente](https://github.com/CFMVCarlos)