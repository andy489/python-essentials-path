from fastapi import APIRouter, HTTPException
import asyncio
import random

router = APIRouter(tags=["Simulation"])


@router.get("/flaky", summary="Simulate a flaky endpoint")
async def flaky_endpoint():
    """
    Simulate a flaky endpoint that randomly fails or succeeds.
    """
    if random.choice([True, False]):
        raise HTTPException(status_code=500, detail="Server Error")
    return {"message": "Success"}


@router.get("/slow-response", summary="Simulate a slow response")
async def slow_response():
    """
    Simulate a slow response from the server (5 seconds).
    """
    await asyncio.sleep(5)
    return {"message": "Response after delay"}
