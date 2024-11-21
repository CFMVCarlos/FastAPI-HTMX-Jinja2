from app import templates  # Importing templates from your application's context
from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

router = APIRouter()

# --------------------------------------------------------------------------------
# Redirects to the index page
# --------------------------------------------------------------------------------
@router.get("/", summary="Redirects to the index page")
def read_root(request: Request) -> Response:
    """
    This route handles requests to the root URL. It sets up some example conditions
    and passes them along with a list of people to the 'index.html' template.
    
    Args:
        request (Request): The FastAPI request object.
    
    Returns:
        Response: A rendered HTML response using the 'index.html' template.
    """
    # Example conditions
    bool_condition1, bool_condition2, bool_condition3 = (
        True,
        False,
        False,
    )  # Replace these with your actual conditions as needed

    # Example list of people
    people = [
        {"name": "Tom", "age": 10},
        {"name": "Charles", "age": 5},
        {"name": "Pam", "age": 7},
    ]

    # Render the 'index.html' template with context
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "bool_condition1": bool_condition1,
            "bool_condition2": bool_condition2,
            "bool_condition3": bool_condition3,
            "some_list": people,
        },
    )


# --------------------------------------------------------------------------------
# Deletes the root and returns a successful response
# --------------------------------------------------------------------------------
@router.delete("/")
def delete_root() -> HTMLResponse:
    """
    Handles DELETE requests to the root URL. Returns a simple HTTP response with
    status code 200 to indicate success.
    
    Returns:
        HTMLResponse: An empty response with status code 200.
    """
    return HTMLResponse(status_code=200)

