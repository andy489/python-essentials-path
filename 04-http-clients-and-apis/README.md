# 04 – HTTP Clients and APIs

| # | Notebook | Topics |
|---|----------|--------|
| 01 | [HTTP Clients and APIs](01-http-clients-and-apis.ipynb) | Performing GET requests, sending data with POST, handling different response formats (JSON, XML, HTML), sessions, cookies, authentication, error handling, timeouts, redirects, and retry logic |

## Sections

| Section | Description |
|---------|-------------|
| Performing GET Requests | `requests.get()`, status codes, response data (content, text, headers, JSON), query parameters |
| Sending Data with POST Requests | Form data (`data=`), JSON bodies (`json=`), file uploads (`files=`), PUT / PATCH / DELETE methods |
| Handling Different Response Formats | Parsing JSON with `.json()`, XML with `ElementTree`, HTML with `BeautifulSoup` |
| Sessions, Cookies, and Authentication | Cookie-based auth, `requests.Session`, HTTP Basic Auth, JWT/Bearer tokens, HTTPS and SSL/TLS |
| Error Handling and Resilient Clients | `raise_for_status()`, timeouts, redirect history, retry logic with `urllib3.Retry` |

## Demo Server

The demo cells require the local FastAPI server running at `http://127.0.0.1:8000`.

```bash
cd demo-server
.venv/bin/uvicorn server:app --reload
```

## Requirements

```bash
pip install requests beautifulsoup4
```
