from fastapi import Request
import time

from app.metrics.http_metrics import http_requests_total, http_request_duration_seconds

class MetricsMiddleware:
    async def __call__(self, request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        return response