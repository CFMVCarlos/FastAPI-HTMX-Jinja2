<div align="center">

# ⚡ FastAPI + HTMX + Jinja2 Showcase

An interactive, high-performance reference application demonstrating server-driven UI, real-time hypermedia streams, and advanced frontend state patterns without heavy client-side JavaScript frameworks.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![HTMX](https://img.shields.io/badge/HTMX-1.9%2B-3366CC?style=flat-square&logo=htmx&logoColor=white)](https://htmx.org/)
[![Jinja2](https://img.shields.io/badge/Jinja2-3.1-B41717?style=flat-square&logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0%2B-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Tests](https://img.shields.io/badge/Tests-31%20Passed-brightgreen?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org/)

[Features](#-key-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Testing & Benchmarking](#-testing--benchmarks) • [Author](#-author)

</div>

---

## 📖 Overview

Modern web architectures often default to complex Single Page Application (SPA) setups when server-driven hypermedia could deliver a cleaner, faster, and more maintainable user experience. 

This repository serves as a practical, comprehensive blueprint for pairing **FastAPI** with **HTMX** and **Jinja2**:
- **Zero Heavy Frontend Build Step:** Pure HTML fragments dynamically swapped into place.
- **Bi-directional Real-Time Capabilities:** Full-duplex WebSockets and live Server-Sent Events (SSE).
- **Graceful Lifecycle & State Management:** Request queuing, header inspection, loading indicators, and out-of-band DOM mutations.

---

## ✨ Key Features

### 1. 🔄 Server-Driven Content Swaps & Mutations
- **Color Class Toggling:** Targeted element swap (`hx-target="#p1"` & `hx-swap="outerHTML"`) with instant server-rendered styling.
- **Isolated Fragment Appending:** Appends newly rendered HTML fragments directly inside parent containers (`beforeend`).
- **Out-of-Band Swaps (`hx-swap-oob`):** Modifies multiple disparate DOM nodes in a single HTTP response (e.g., updating a header notification banner while returning inline content).
- **Selective DOM Querying (`hx-select`):** Extracts targeted elements from broader server responses.

### 2. ⚡ Real-Time Streaming & Full-Duplex Channels
- **Server-Sent Events (SSE):** Push continuous unidirectional updates (`/extensions/stream`) using `EventSourceResponse` without client polling.
- **High-Performance WebSockets:** Real-time multi-client broadcast messaging manager with O(1) string interpolation and sub-millisecond dispatch times.

### 3. 🎯 Advanced HTMX Controls & Synchronization
- **Request Queue Synchronization (`hx-sync`):** Eliminates race conditions across slow asynchronous endpoints by enforcing orderly queue processing (`this:queue last`).
- **Header-Based Triggers (`HX-Trigger`):** Server inspects caller headers (`request.headers.get("HX-Trigger")`) to dispatch targeted conditional responses.
- **Server Event Emitters:** Server sends custom trigger events back to client listeners upon hitting internal counter thresholds.
- **Permission-Gated Mutations:** Demonstrates server-level authorization gates returning `204 No Content` until explicit state flips.

### 4. 🎨 UI Feedback & Jinja2 Templating
- **Loading Indicators & Async Delays:** Declarative state spinners (`data-loading-states`) that auto-disable buttons while requests are in flight.
- **SweetAlert2 & Native Modals:** Integrates native browser confirmations and promise-based modal dialogs prior to dispatching HTTP calls.
- **Jinja2 Logic:** Server-side conditional branches, loop evaluation, and component inclusion (`{% include "extra_html.html" %}`).

---

## 🚀 Quick Start

### Prerequisites
- Python `3.10+`
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

### 1. Clone the repository
```bash
git clone https://github.com/CFMVCarlos/FastAPI-HTMX-Jinja2.git
cd FastAPI-HTMX-Jinja2
```

### 2. Install dependencies
```bash
uv pip install -r requirements.txt
# Or with standard pip:
# pip install -r requirements.txt
```

### 3. Run the development server
```bash
uv run uvicorn app.main:app --reload
```

Open your browser and navigate to:
- **Interactive UI:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🏛️ Architecture

```
FastAPI-HTMX-Jinja2/
├── app/
│   ├── main.py                     # Application entry point, middleware, exception handlers
│   ├── api/
│   │   └── services/
│   │       └── builtin_service.py  # Decoupled HTML fragment generators & business logic
│   └── routers/
│       ├── root.py                 # Index page route & template context rendering
│       ├── builtin.py              # Core HTMX endpoints (DOM swaps, headers, sync)
│       └── extensions.py           # Real-time channels (WebSockets, SSE, loading states)
├── static/
│   ├── css/                        # Custom animations, transitions, and indicators
│   ├── js/                         # Vendor JavaScript libraries (HTMX core)
│   └── img/                        # Assets & indicators
├── templates/
│   ├── index.html                  # Main showcase dashboard styled with Tailwind CSS
│   └── extra_html.html             # Jinja2 component include demo
└── tests/
    ├── __init__.py
    ├── test_app.py                 # Full pytest suite (31 tests covering all endpoints)
    └── benchmark.py                # High-concurrency WebSocket broadcast stress benchmark
```

---

## 🧪 Testing & Benchmarks

### Running the Test Suite
The project includes automated tests verifying endpoint status codes, XSS escaping, SSE generators, WebSocket dispatches, and Jinja2 template rendering.

```bash
uv run pytest
```

```
====================== 31 passed in 0.85s =======================
```

### High-Concurrency WebSocket Benchmark
The repository includes a dedicated benchmark in [`tests/benchmark.py`](tests/benchmark.py) to measure broadcast latency across 10,000 concurrent WebSocket connections:

```bash
uv run python tests/benchmark.py
```
```
Time taken for 100 broadcasts to 10,000 connections: ~0.12 seconds
```

---

## 👤 Author

**Carlos Valente**
- GitHub: [@CFMVCarlos](https://github.com/CFMVCarlos)
- Profile: [Carlos Valente](https://www.boot.dev/u/carlosfmv)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.