from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["Redirection"])


@router.get("/old-route", summary="Redirect from old to new route")
async def old_route():
    """
    Redirect requests from an old route to a new route.
    """
    return RedirectResponse(url="/new-route")


@router.head("/old-route", summary="Head request for old route redirection")
async def old_route_head():
    """
    Handle HEAD requests for the old route, redirecting to the new route.
    """
    return RedirectResponse(url="/new-route")


@router.get("/new-route", summary="New route endpoint")
async def new_route():
    """
    Respond to requests at the new route.
    """
    return {"message": "This is the new route!"}


@router.head("/new-route", summary="Head request for new route")
async def new_route_head():
    """
    Handle HEAD requests for the new route.
    """
    return Response(content=None, media_type="application/json")
