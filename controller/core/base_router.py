from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Configure Jinja2 template directory
templates = Jinja2Templates(directory="views")

# Simple hello world route
@router.get("/", response_class=HTMLResponse)
def hello_world(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
