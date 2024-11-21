# Importing necessary libraries and modules
import os
import sys
import uvicorn  # Uvicorn ASGI server for FastAPI
from fastapi import FastAPI  # FastAPI framework
from fastapi.staticfiles import StaticFiles  # To serve static files

# Adding the parent directory of the current script to the system path
# This allows importing modules from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importing the routers from the 'app.routers' module
# These routers define the endpoints for different parts of the application
from app.routers import builtin, extensions, root

# Getting the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initializing the FastAPI application
app = FastAPI()

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
