import random, time
from fastapi import FastAPI, Request
from prometheus_client import Histogram, Counter, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
from prometheus_client import multiprocess, Gauge
from starlette.responses import Response

app = FastAPI(title="demo-api")

# Hystogram p99
REQUEST_LATENCY = Histogram(
    "http_latency_seconds",
    "Request latency seconds",
    ["path","method","status"],
    buckets=(0.01,0.02,0.05,0.1,0.2,0.3,0.5,0.8,1.2,2.0)
)

REQS = Counter("http_requests_total","Requests",["path","method","status"])

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/api/hello")
def hello():
    start = time.perf_counter()

    if random.random() < 0.1:
        time.sleep(0.35)
    dur = time.perf_counter() - start
    REQUEST_LATENCY.labels("/api/hello","GET","200").observe(dur)
    REQS.labels("/api/hello","GET","200").inc()
    return {"hello":"world","latency":dur}

# «Bad» version — enable for demo:
# @app.get("/api/hello")
# def hello():
#     start = time.perf_counter()
#     time.sleep(0.25)
#     dur = time.perf_counter() - start
#     REQUEST_LATENCY.labels("/api/hello","GET","200").observe(dur)
#     REQS.labels("/api/hello","GET","200").inc()
#     return {"hello":"slow","latency":dur}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
