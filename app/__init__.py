"""
This module builds shared parts for other modules.
It focuses on managing templates using Jinja2.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

# Importing Jinja2Templates from FastAPI to render HTML templates
# This allows rendering dynamic content in HTML using Jinja2 template engine
from fastapi.templating import Jinja2Templates


# --------------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------------

# Creating an instance of Jinja2Templates.
# The 'templates' directory is where the HTML templates are stored.
templates = Jinja2Templates(directory="templates")  # Specify the templates directory
