# Metrics collection interval (in seconds)
SYSTEM_METRICS_INTERVAL = 10

# Histogram buckets for HTTP request duration (in seconds)
HTTP_DURATION_BUCKETS = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, float("inf")]

# Prometheus metric naming prefix (for standardization)
METRIC_PREFIX = ""