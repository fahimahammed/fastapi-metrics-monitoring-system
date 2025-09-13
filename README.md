# FastAPI Metrics Monitoring System

## Project Overview

The **FastAPI Metrics Monitoring System** is designed to provide real-time observability into both system and application-level performance metrics. Using **Prometheus metrics format**, it tracks CPU, memory, request rates, latency, and other vital metrics, making it suitable for production-grade monitoring.

The system enables developers and operators to:

* Track system resource utilization
* Monitor HTTP request patterns
* Identify bottlenecks and performance issues
* Integrate seamlessly with Prometheus-based monitoring infrastructure

## Technical Stack

### Core Framework

* **FastAPI**: Main web framework
* **Python 3.8+**: Runtime environment
* **Uvicorn**: ASGI server for production deployment

### Monitoring Stack

* **prometheus\_client**: Python library for metrics collection
* **Prometheus**: Metrics storage and querying (external)

### Additional Libraries

* **psutil**: System resource monitoring
* **asyncio**: Async operations support
* **Middleware**: Custom FastAPI middleware for HTTP metrics

---

## Architecture

### Application Structure

```
fastapi-metrics-app/ 
├── app/ 
│   ├── main.py                  # FastAPI entry point
│   ├── metrics/ 
│   │   ├── __init__.py
│   │   ├── system_metrics.py     # CPU, memory, threads, GC metrics
│   │   └── http_metrics.py       # HTTP request counters and histograms
│   ├── middleware/ 
│   │   └── metrics_middleware.py # Tracks HTTP request lifecycle
│   ├── routers/ 
│   │   ├── api.py               # Sample data endpoints
│   │   └── health.py            # Health check endpoint
│   └── config.py                # Config management
├── requirements.txt
└── README.md
```

#### Metrics Endpoint

* `/metrics` exposes all Prometheus metrics
* Returns `Content-Type: text/plain; version=0.0.4`

---

## Implementation Details

### System Metrics

| Metric                              | Description              | Prometheus Type |
| ----------------------------------- | ------------------------ | --------------- |
| `process_cpu_seconds_total`         | Total CPU time used      | Counter         |
| `process_resident_memory_bytes`     | Physical memory used     | Gauge           |
| `process_virtual_memory_bytes`      | Virtual memory allocated | Gauge           |
| `process_start_time_seconds`        | Process start time       | Gauge           |
| `process_open_fds`                  | File descriptor count    | Gauge           |
| `python_gc_objects_collected_total` | Collected GC objects     | Counter         |
| `python_threads`                    | Active threads count     | Gauge           |

### HTTP Metrics

| Metric                          | Description               | Labels                         | Type      |
| ------------------------------- | ------------------------- | ------------------------------ | --------- |
| `http_requests_total`           | Total HTTP requests       | method, endpoint, status\_code | Counter   |
| `http_request_duration_seconds` | Request latency histogram | method, endpoint               | Histogram |
| `http_request_size_bytes`       | Request payload size      | method, endpoint               | Histogram |
| `http_response_size_bytes`      | Response payload size     | method, endpoint               | Histogram |

### Middleware

* Tracks request lifecycle:

  ```python
  start = time.time()
  response = await call_next(request)
  duration = time.time() - start
  ```
* Updates Prometheus metrics after request completes
* Supports **async/await** for non-blocking monitoring

### Endpoints

| Endpoint   | Method | Description                          |
| ---------- | ------ | ------------------------------------ |
| `/`        | GET    | Root endpoint with a welcome message |
| `/health`  | GET    | Health check (returns status OK)     |
| `/metrics` | GET    | Prometheus metrics exposition        |
| `/data`    | POST   | Sample data processing               |
| `/data`    | GET    | Sample data retrieval                |

---

## Configuration

* **Metric collection interval**: Adjustable via `config.py`
* **Histogram buckets**: Customizable per endpoint
* **Metric labels**: Standardized across all metrics
* **Prometheus naming**: Follows best practices

Example in `config.py`:

```python
SYSTEM_METRICS_INTERVAL = 10

HTTP_DURATION_BUCKETS = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, float("inf")]

METRIC_PREFIX = ""
```

---

## Deployment Guide

### Using Docker & Docker Compose

* Build and run:

```bash
docker-compose up --build
```

* Access endpoints:

- FastAPI app: http://localhost:8000
- Prometheus: http://localhost:9090
- API Docs: http://localhost:8000/docs
- Metrics: http://localhost:8000/metrics

---

## Prometheus Metrics Reference

**Sample Metrics Output:**

```
# HELP process_cpu_seconds_total Total user and system CPU time
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 12.34

# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/data",status_code="200"} 42
```

---

## Monitoring & Alerts

* Prometheus queries can be used for alerts:

```prometheus
# High CPU utilization alert
rate(process_cpu_seconds_total[5m]) > 0.8
```

* Track 95th percentile latency per endpoint:

```prometheus
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))
```
