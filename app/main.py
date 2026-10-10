# Importing necessary libraries and modules
import os
import sys
import uvicorn  # Uvicorn ASGI server for FastAPI
from fastapi import FastAPI, Request  # FastAPI framework
from fastapi.staticfiles import StaticFiles  # To serve static files
from fastapi.responses import JSONResponse  # Standardized JSON error response
import traceback

# Adding the parent directory of the current script to the system path
# This allows importing modules from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importing the routers from the 'app.routers' module
# These routers define the endpoints for different parts of the application
from app.routers import builtin, extensions, root

# Initializing the FastAPI application
app = FastAPI(
    title="High-Performance Backend",
    description="Refactored and modernized API architecture.",
    version="1.0.0"
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to catch unhandled errors and return a standardized JSON response.
    Never exposes stack traces to the client in production.
    """
    # For a real production app, we would log the traceback here instead of exposing it
    # logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An unexpected error occurred.",
            "code": 500
        },
    )


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Middleware to append security headers to all responses.
    This helps mitigate risks like MIME sniffing and Clickjacking.
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Including the routers for different parts of the application

app.include_router(root.router)       # Root router, handles main endpoints
app.include_router(extensions.router)  # Extensions router, handles additional features
app.include_router(builtin.router)     # Builtin router, handles built-in features

# Mounting the 'static' directory to serve static files
# This allows serving files from the 'static' folder in the project root
app.mount(
    path="/static",                   # URL path prefix for static files
    app=StaticFiles(directory="static"),  # The directory where static files are located
    name="static",                    # A name for the static file mount
)

# The main function to run the Uvicorn server
# This will start the application on the specified host and port
def main() -> None:
    uvicorn.run(app, host="localhost", port=8000)  # Running the app on localhost:8000

# Entry point for the script
# This runs the FastAPI app when the script is executed directly
if __name__ == "__main__":
    main()  # Calls the main function to start the server
