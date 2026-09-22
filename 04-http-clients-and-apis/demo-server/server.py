from fastapi import FastAPI
import uvicorn

from routers import auth, cookies, html_pages, items, redirection, simulation

app = FastAPI()

app.include_router(items.router)
app.include_router(html_pages.router)
app.include_router(auth.router)
app.include_router(cookies.router)
app.include_router(redirection.router)
app.include_router(simulation.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
