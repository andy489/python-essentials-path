# Demo Server

A FastAPI server used for the HTTP clients and APIs exercises.

## Project structure

```
demo-server/
├── server.py           # App entry point — creates the FastAPI app and registers routers
├── models.py           # Pydantic models (Item)
├── state.py            # Shared in-memory state: items database, flash messages, Jinja2 env
├── routers/
│   ├── items.py        # GET/POST/PUT/PATCH/DELETE /api/items, /upload-files
│   ├── html_pages.py   # /items/new, /about
│   ├── auth.py         # /api/login, /protected, /protected-endpoint, /jwt-protected-route
│   ├── cookies.py      # /api/cookies
│   ├── redirection.py  # /old-route, /new-route
│   └── simulation.py   # /flaky, /slow-response
└── templates/
    ├── new_item.html
    └── about.html
```

## Setup

Navigate to this directory in your terminal:

```
cd demo-server
```

### Option A — Install globally

**Linux/macOS:**
```bash
python3 -m pip install -r requirements.txt
```

**Windows:**
```bash
python -m pip install -r requirements.txt
```

### Option B — Use a virtual environment (recommended)

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Deactivate the environment when you're done:
```bash
deactivate
```

## Running the server

**Linux/macOS:**
```bash
python3 server.py
```

**Windows:**
```bash
python server.py
```

The server runs at `http://127.0.0.1:8000`.

Open `http://127.0.0.1:8000/docs` to browse the auto-generated Swagger documentation.
