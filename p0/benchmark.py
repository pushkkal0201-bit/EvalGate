"""Run a sequential in-process CPU benchmark against the provided demo API."""

import statistics
import time

from fastapi.testclient import TestClient

from main import app


def main():
    with TestClient(app) as client:
        samples = []
        for index in range(550):
            started = time.perf_counter()
            response = client.post("/v1/regression/paired", json={'baseline': [0, 0], 'candidate': [1, 1], 'samples': 100})
            elapsed = time.perf_counter() - started
            response.raise_for_status()
            if index >= 50:
                samples.append(elapsed)
    p95 = statistics.quantiles(samples, n=100, method="inclusive")[94]
    print(f"n={len(samples)} p50={statistics.median(samples) * 1000:.3f} ms p95={p95 * 1000:.3f} ms")


if __name__ == "__main__":
    main()
