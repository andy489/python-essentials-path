from fastapi import APIRouter, Cookie, Depends, Form, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

import state

router = APIRouter(tags=["Authentication"])

security = HTTPBasic()
USERNAME = "username"
PASSWORD = "pass"


@router.post("/api/login", summary="User 'remember me' login")
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Authenticate a user with a username and password.

    - **username**: User's username.
    - **password**: User's password.
    """
    if username == "some_name" and password == "pass":
        state.user_id_hash = secrets.token_hex(16)
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(key="user_id", value=state.user_id_hash)
        return response
    return {"message": "Invalid credentials"}


def _verify_user_id(user_id: str = Cookie(None)):
    if state.user_id_hash != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/protected", summary="Access a protected route with a cookie")
async def cookie_protected_route(user_id_verified: str = Depends(_verify_user_id)):
    """
    Access a route that is protected by user ID verification.
    """
    return {"message": "You have access to this protected route"}


def _get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


@router.get("/protected-endpoint", summary="Access a basic auth protected route")
async def basic_auth_protected_route(
    user: HTTPBasicCredentials = Depends(_get_current_user),
):
    """
    Access a route protected by HTTP Basic Authentication.

    You need to provide HTTPBasic Authentication username and password to access this route.
    If you want to access it from the documentation, you can click on the Authorize button at the top of the page.
    """
    return {"message": "Welcome, authenticated user!"}


@router.get("/jwt-protected-route", summary="Access a JWT protected route")
async def jwt_protected_route(authorization: str = Header(None)):
    """
    Access a route protected by JWT (JSON Web Token) authorization.

    - **authorization**: JWT token in the authorization header.
    """
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        if token == "abcde123":
            return {"message": "Access to protected route granted"}
        raise HTTPException(status_code=401, detail="Invalid token")
    raise HTTPException(
        status_code=401, detail="Authorization header missing or invalid"
    )
