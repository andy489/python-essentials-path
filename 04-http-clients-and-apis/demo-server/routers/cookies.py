from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Cookies"])


@router.get("/api/cookies", summary="Get back cookies from the request")
async def get_cookies(request: Request):
    """
    Send cookies with the request and get them from the response.
    """
    response = JSONResponse(content={"message": "ok"})
    for cookie_name, cookie_value in request.cookies.items():
        response.set_cookie(key=cookie_name, value=cookie_value)
    return response
