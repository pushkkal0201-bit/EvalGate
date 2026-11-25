# EvalGate

See the [architecture and release criteria](../docs/architecture.md).

## CPU-only quick start

From this directory, run `docker compose up --build` and open http://localhost:8000/docs.
For a local Python run, install `requirements.txt` in a Python 3.11 virtual environment and run
`uvicorn main:app`. Run tests with `python -m pytest -q`.

```sh
curl -fsS http://localhost:8000/v1/regression/paired \
  -H 'Content-Type: application/json' \
  -d '{"baseline": [0, 0], "candidate": [1, 1], "samples": 100}'
```

Set `API_KEY` in the environment before starting the server to require an `X-API-Key`
header on versioned endpoints. The default is intended for loopback development.
Health and metrics are accessible independently of the API key. Keep those endpoints
on a trusted network and terminate TLS at the ingress when using remote clients.
Versioned requests have an 8 MiB body limit.

## Observability

Set `GRAFANA_PASSWORD` and run
`docker compose -f compose.yaml -f compose.observability.yaml up --build`.
Prometheus scrapes `/metrics/`. Open Grafana at http://localhost:3000 and select
the EvalGate API dashboard for request rate and p95 latency per route. The
histogram labels use route templates and status codes. Request content is excluded.

## Kubernetes

Build with `docker build -t evalgate:local .` and load the image into your
local cluster or replace the manifest tag with a registry image digest. Create
a Secret named `evalgate-api` with key `api-key` in the target namespace, then
run `kubectl apply -f ../deploy/kubernetes.yaml`.
The manifest uses a single CPU-only replica and a ClusterIP service.
Configure Prometheus discovery for annotated pods in your cluster.

## Limitations

Paired bootstrap uses deterministic resampling and requires aligned examples. The API does not publish GitHub check statuses or invoke evaluation models.

## Verification on 2026-11-25

- 9 tests passed using the pinned project requirements on Python 3.12.14.
- The Python 3.11 Docker image built and passed a non-root, read-only container health smoke test. The build used the host CA bundle via the optional BuildKit secret `pip_ca` to trust the environment proxy.
- Docker Compose resolved the merged observability configuration. The Kubernetes YAML parsed and the workload and Service selectors matched. Live dashboard scraping and Kubernetes rollout were outside this verification pass.
- `python benchmark.py` measured **0.635 ms p50** and **0.817 ms p95** for 500 sequential in-process demo requests after 50 warm-ups on an AMD EPYC 9V74 host. This includes the test client and application request path. It excludes external providers, model inference, real network and concurrent load.
