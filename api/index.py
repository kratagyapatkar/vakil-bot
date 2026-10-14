"""
VakilBot App Service ('app')
Serves frontend static UI and communicates with internal 'backend' service
via Vercel service binding (BACKEND_URL).
"""

import os
import sys
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="VakilBot App Service",
    description="Frontend server and API gateway communicating with backend service via Vercel service bindings",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vercel service binding automatically injects BACKEND_URL for the 'backend' service
BACKEND_URL = os.environ.get("BACKEND_URL", "").rstrip("/")

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
async def serve_index():
    """Serve frontend index.html."""
    candidates = [
        os.path.join(FRONTEND_DIR, "index.html"),
        os.path.join(os.getcwd(), "frontend", "index.html"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")),
    ]
    for p in candidates:
        if os.path.exists(p):
            return FileResponse(p)
    return JSONResponse({"status": "running", "service": "app", "message": "Frontend not found"})


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy_to_backend(path: str, request: Request):
    """
    Forward client requests to the internal 'backend' service using the bound BACKEND_URL variable.
    """
    # If BACKEND_URL is available from Vercel service binding, call it via HTTP
    if BACKEND_URL:
        target_url = f"{BACKEND_URL}/api/{path}"
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    content=body,
                    params=request.query_params
                )
                excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
                forward_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}
                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    headers=forward_headers
                )
        except Exception as e:
            return JSONResponse(
                status_code=502,
                content={"error": f"Failed to communicate with internal backend service at {BACKEND_URL}: {str(e)}"}
            )

    # Local fallback when BACKEND_URL is not set (direct local import)
    try:
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        from main import app as local_backend_app
        # Re-dispatch internally to local_backend_app
        from starlette.testclient import TestClient
        client = TestClient(local_backend_app)
        body = await request.body()
        resp = client.request(
            method=request.method,
            url=f"/api/{path}",
            content=body,
            headers=dict(request.headers),
            params=request.query_params
        )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers)
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Local fallback error: {str(e)}"}
        )
