from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from state import flash_messages, items_db, jinja_env

router = APIRouter(tags=["Items HTML"])


@router.get("/items/new", summary="Serve a form for creating a new item")
async def new_item_form():
    """
    Serve an HTML page with a form to submit a new item's name and price.
    """
    messages = list(flash_messages)
    flash_messages.clear()

    rendered_template = jinja_env.get_template("new_item.html").render(
        flash_messages=messages
    )
    return HTMLResponse(content=rendered_template)


@router.post("/items/new", summary="Handle the items form submission")
async def create_item_from_form(name: str = Form(...), price: float = Form(...)):
    """
    Handle form submission to add a new item to items_db.
    """
    items_db.append({"name": name, "price": price})
    flash_messages.append(f"Item {name} added successfully!")
    return RedirectResponse(url="/items/new", status_code=303)


@router.get("/about", summary="Serve the about page")
async def about_page():
    """
    Serve an HTML page with information about the items webshop.
    """
    rendered_template = jinja_env.get_template("about.html").render()
    return HTMLResponse(content=rendered_template)
