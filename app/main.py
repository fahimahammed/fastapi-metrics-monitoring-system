from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.config import SYSTEM_METRICS_INTERVAL
from app.metrics.system_metrics import start_system_metrics_collector
from app.middleware.metrics_middleware import MetricsMiddleware
from app.routers import api, health

app = FastAPI()

app.middleware("http")(MetricsMiddleware())
app.include_router(api.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "FastAPI Metrics App"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.on_event("startup")
async def startup_event():
    start_system_metrics_collector(SYSTEM_METRICS_INTERVAL)