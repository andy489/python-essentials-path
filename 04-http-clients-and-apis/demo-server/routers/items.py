from fastapi import APIRouter, Body, HTTPException, Response, UploadFile, File
from typing import List, Optional
import xml.etree.ElementTree as ET

from models import Item
from state import items_db

router = APIRouter(tags=["Items API"])


@router.get("/", summary="Retrieve a list of items")
@router.get("/api/items", summary="Retrieve a list of items")
async def read_items(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    max_price: Optional[float] = None,
):
    """
    Retrieve all of the items or a subset of items from the database based on pagination parameters and price parameters.

    - **offset**: (Optional) Starting position for fetching the items.
    - **limit**: (Optional) Maximum number of items to fetch.
    - **max_price**: (Optional) Maximum price for filtering items.

    Returns a list of items within the given range and below the given price.
    """
    filtered_items = items_db

    if max_price is not None:
        filtered_items = [item for item in items_db if item["price"] <= max_price]

    if offset is None:
        offset = 0
    if limit is None:
        limit = len(filtered_items) - offset

    return filtered_items[offset : offset + limit]


@router.post("/api/items", summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **price**: required
    """
    items_db.append(item.model_dump())
    return item


@router.post("/api/items/xml", summary="Create an item with XML")
async def create_item_xml(xml_body: str = Body(..., media_type="application/xml")):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **price**: required
    """
    try:
        root = ET.fromstring(xml_body)
        name = root.find("name").text
        price = root.find("price").text
        items_db.append({"name": name, "price": price})

        xml_response = f"""
        <response>
            <name>{name}</name>
            <price>{price}</price>
        </response>
        """
        return Response(content=xml_response, media_type="application/xml")
    except ET.ParseError:
        raise HTTPException(status_code=400, detail="Invalid XML")


@router.put("/api/items/{item_id}", summary="Update an item completely")
async def update_item(item_id: int, item: Item):
    """
    Update all fields of an existing item:

    - **name**: each item must have a name.
    - **price**: required.
    """
    if 0 <= item_id < len(items_db):
        items_db[item_id] = item.model_dump()
        return items_db[item_id]
    raise HTTPException(status_code=404, detail="Item not found")


@router.patch("/api/items/{item_id}", summary="Update specific fields of an item")
async def patch_item(item_id: int, item: Item):
    """
    Update specific fields of an existing item:

    - **name**: optional new name for the item.
    - **price**: optional new price for the item.
    """
    if 0 <= item_id < len(items_db):
        if item.name:
            items_db[item_id]["name"] = item.name
        if item.price:
            items_db[item_id]["price"] = item.price
        return items_db[item_id]
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/api/items/{item_id}", summary="Delete an item")
async def delete_item(item_id: int):
    """
    Delete an existing item:

    - **item_id**: the ID of the item to be deleted.
    """
    if 0 <= item_id < len(items_db):
        deleted_item = items_db.pop(item_id)
        return {"status": "Item deleted", "item": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/api/items/{item_id}", summary="Retrieve a single item")
async def get_item(item_id: int):
    """
    Retrieve a specific item based on its ID:

    - **item_id**: the ID of the item to be retrieved.
    """
    if 0 <= item_id < len(items_db):
        return items_db[item_id]
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/upload-files", summary="Upload multiple CSV files", tags=["Upload files"])
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload one or more CSV files to the server.

    - **files**: A list of CSV files to be uploaded.

    Returns a dictionary with the names of the uploaded files.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    filenames = []
    for file in files:
        await file.read()
        filenames.append(file.filename)

    return {"uploaded_files": filenames}
