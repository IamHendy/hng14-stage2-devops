# Job Processing System

A microservices job processing application built with FastAPI, Node.js, and Redis,
fully containerized with Docker and deployed via a CI/CD pipeline.

## Architecture

- **Frontend** (Node.js/Express) — Job submission and status dashboard on port 3000
- **API** (Python/FastAPI) — Job creation and status endpoints on port 8000
- **Worker** (Python) — Picks up and processes jobs from Redis queue
- **Redis** — Shared message queue between API and Worker

## Prerequisites

- Docker >= 24.0
- Docker Compose >= 2.0
- Git

## Quick Start

### 1. Clone the repository

git clone https://github.com/IamHendy/hng14-stage2-devops.git
cd hng14-stage2-devops

### 2. Create your environment file

cp .env.example .env

Edit .env and fill in your values.

### 3. Build and start the stack

docker compose up --build

### 4. Verify everything is running

docker compose ps

You should see all four services: redis, api, worker, frontend — all healthy.

### 5. Access the application

Open your browser at http://localhost:3000

Click "Submit New Job" and watch it process in real time.

## Testing the API manually

Submit a job:
curl -X POST http://localhost:3000/submit

Check job status (replace JOB_ID with the id from above):
curl http://localhost:3000/status/JOB_ID

Check API health:
curl http://localhost:3000/health

## Successful startup looks like

redis-1    | Ready to accept connections tcp
api-1      | Uvicorn running on http://0.0.0.0:8000
worker-1   | Processing job ...
frontend-1 | Frontend running on port 3000

## Stopping the stack

docker compose down

## Environment Variables

See .env.example for all required variables.

## CI/CD Pipeline

The GitHub Actions pipeline runs on every push:

lint -> test -> build -> security scan -> integration test -> deploy

- Lint: flake8 (Python), eslint (JavaScript), hadolint (Dockerfiles)
- Test: pytest with Redis mocked, coverage report uploaded as artifact
- Build: Images built and pushed to local registry, tagged with git SHA and latest
- Security scan: Trivy scans all images for CRITICAL vulnerabilities
- Integration test: Full stack spun up, job submitted and polled to completion
- Deploy: Rolling update on pushes to main only

## Project Structure

hng14-stage2-devops/
├── api/                  # FastAPI backend
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
├── worker/               # Job processor
│   ├── Dockerfile
│   └── app.py
├── frontend/             # Node.js dashboard
│   ├── Dockerfile
│   ├── app.js
│   └── views/
├── docker-compose.yml
├── .env.example
└── .github/
    └── workflows/
        └── pipeline.yml
