"""HTTP controls and request telemetry for the versioned API."""

import hmac
import os
import time

from prometheus_client import Histogram
from starlette.datastructures import Headers
from starlette.responses import JSONResponse

MAX_BODY_BYTES = 8 * 1024 * 1024
REQUEST_DURATION = Histogram(
    "api_request_duration_seconds",
    "Time to produce the response headers on a versioned API route.",
    ("route", "status"),
)


class RuntimeMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not scope["path"].startswith("/v1/"):
            await self.app(scope, receive, send)
            return

        started = time.perf_counter()
        status = None

        async def measure(response):
            nonlocal status
            if response["type"] == "http.response.start":
                status = response["status"]
                observe(status)
            await send(response)

        def observe(code):
            route = scope.get("route")
            REQUEST_DURATION.labels(getattr(route, "path", "unmatched"), str(code)).observe(
                time.perf_counter() - started
            )

        key = os.getenv("API_KEY", "")
        supplied = Headers(scope=scope).get("x-api-key", "")
        if key and not hmac.compare_digest(key.encode(), supplied.encode()):
            await JSONResponse({"detail": "Invalid API key"}, status_code=401)(scope, receive, measure)
            return

        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            chunk = message.get("body", b"")
            if len(body) + len(chunk) > MAX_BODY_BYTES:
                await JSONResponse({"detail": "Request body too large"}, status_code=413)(
                    scope, receive, measure
                )
                return
            body.extend(chunk)
            if not message.get("more_body"):
                break

        pending = True

        async def replay():
            nonlocal pending
            if pending:
                pending = False
                return {"type": "http.request", "body": bytes(body)}
            return await receive()

        try:
            await self.app(scope, replay, measure)
        except Exception:
            if status is None:
                observe(500)
            raise


def configure_runtime(app):
    app.add_middleware(RuntimeMiddleware)
