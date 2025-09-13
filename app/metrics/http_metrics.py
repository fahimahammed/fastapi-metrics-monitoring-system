from prometheus_client import Counter, Histogram

from app.config import METRIC_PREFIX, HTTP_DURATION_BUCKETS

http_requests_total = Counter(
    f'{METRIC_PREFIX}http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    f'{METRIC_PREFIX}http_request_duration_seconds',
    'HTTP request durations',
    ['method', 'endpoint'],
    buckets=HTTP_DURATION_BUCKETS
)