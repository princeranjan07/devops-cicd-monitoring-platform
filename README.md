
# DevOps Portfolio Demo: CI/CD + Metrics + Alerting + Rollback

This repository contains a minimal but realistic DevOps showcase project designed to demonstrate core skills:
containerization, CI/CD, observability, alerting, regression detection, and rollback.

The goal is simple: show **how you deliver**, not just which tools you know.

---

## 1. Overview

This project includes:

- A small **FastAPI** application exposing metrics
- **Prometheus** + **Grafana** stack provisioned via Docker Compose
- **p99 latency SLO** with an alert rule
- A reproducible **regression → alert → rollback** scenario
- A clean, transparent CI pipeline

Everything runs locally. No cloud account required.

Architecture:

```
FastAPI app → /metrics → Prometheus → Grafana dashboards → Alert rules
```

---

## 2. Demo (How to Run)

### Start the full monitoring stack

```bash
make up
# or
docker compose up -d
```

### Services

- App: http://localhost:8080/api/hello
- Metrics: http://localhost:8080/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default login: admin / admin)

---

## 3. Before / After Metrics (Regression → Fix)

This repo includes two versions of the `hello` endpoint:

- **Normal**: fast responses (baseline p99 ~0.05–0.1s)
- **Slow** (optional): artificial latency using `time.sleep(0.25)`
  (p99 ~0.8–1.2s depending on load)

Procedure:

1. Enable the slow version (comment/uncomment in `app/main.py`)
2. Run load:
   ```bash
   hey -z 20s -q 50 http://localhost:8080/api/hello
   ```
3. Observe **p99** spike in Grafana
4. Alert triggers (based on rule in `alert.rules.yml`)
5. Revert to the fast version
6. Run load again and watch p99 return to normal

### Example (replace with your actual screenshots)

| Metric | Before | Regression | After Fix |
|-------|--------|------------|-----------|
| p99 latency | ~0.09s | ~0.85s | ~0.09s |
| MTTR (manual fix) | — | ~5–10 minutes | — |
| Lead time for release | ~2 minutes | ~2 minutes | ~2 minutes |

---

## 4. CI/CD Pipeline

The pipeline (see `ci.yml`) demonstrates:

- Build container image
- Install dependencies
- Run tests
- Generate SBOM
- Push image to registry (GHCR or others)
- Optional: Terraform plan/apply hooks for real environments

Technologies used:

- Docker Buildx
- GitHub Actions runner
- SBOM generation (`anchore/sbom-action`)

---

## 5. Infrastructure & Configuration
Key features:

- Prometheus auto-scrape and alert provisioning
- Grafana dashboards provisioned via code (no manual setup)
- Clean Docker Compose separation: app, Prometheus, Grafana

---

## 6. Alerting & SLO

### SLO

- **Latency SLO:** p99 < 800ms
- **Alert:** triggers if p99 exceeds threshold for 10 minutes
  (defined in `alert.rules.yml`)

---

## 7. Rollback Scenario

This project illustrates a simple rollback flow:

1. Deployment introduces latency regression
2. Alert fires
3. Engineer reverts the change
4. Metrics return to normal
5. Dashboard screenshots prove improvement

---

## 8. How to Customize for Interviews

Replace placeholders with your data:

- Real p99 numbers from your run
- Real MTTR
- Screenshots of dashboards and CI
- Add a short runbook under `docs/` (optional)

---

## 9. License

MIT
# devops-cicd-monitoring-platform
Docker, CI/CD , monitoring and alerting portfolio project
