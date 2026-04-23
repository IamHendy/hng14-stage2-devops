# Bug Fixes

All bugs found and fixed in the starter repository.

## Fix 1
- **File:** `api/main.py`
- **Line:** 8
- **Problem:** Redis host hardcoded as `localhost` — unreachable inside Docker network
- **Fix:** Changed to read from `REDIS_HOST` env var defaulting to `redis`

## Fix 2
- **File:** `api/main.py`
- **Line:** 13
- **Problem:** `r.brpop("job")` was incorrectly added inside `create_job()` — the API
  should only push jobs, never pop them. Popping is the worker's responsibility.
- **Fix:** Removed the `brpop` call entirely from `create_job()`

## Fix 3
- **File:** `api/main.py`
- **Line:** 13
- **Problem:** Queue name was `"job"` (singular) but worker used `"jobs"` (plural)
- **Fix:** Standardized queue name to `"jobs"` across all services

## Fix 4
- **File:** `api/main.py`
- **Line:** (new)
- **Problem:** No `/health` endpoint — HEALTHCHECK and integration tests had nothing to probe
- **Fix:** Added `GET /health` route returning `{"status": "ok"}`

## Fix 5
- **File:** `frontend/app.js`
- **Line:** 5
- **Problem:** API_URL hardcoded as `http://localhost:8000` — breaks inside Docker network
- **Fix:** Changed to read from `API_URL` env var defaulting to `http://api:8000`

## Fix 6
- **File:** `frontend/app.js`
- **Line:** (new)
- **Problem:** No `/health` endpoint for frontend container HEALTHCHECK
- **Fix:** Added `GET /health` route returning `{"status": "ok"}`

## Fix 7
- **File:** `worker/app.py`
- **Line:** 4
- **Problem:** Redis host hardcoded as `localhost` — unreachable inside Docker network
- **Fix:** Changed to read from `REDIS_HOST` env var defaulting to `redis`

## Fix 8
- **File:** `worker/app.py`
- **Line:** 3
- **Problem:** `signal` module imported but never used — no graceful shutdown handling
- **Fix:** Added SIGTERM and SIGINT handlers so Docker can stop the worker cleanly

## Fix 9
- **File:** `worker/app.py`
- **Problem:** `running = True` was placed inside `process_job()` function — reset
  the shutdown flag after every job, making SIGTERM handler useless
- **Fix:** Moved `running = True` to module level before signal handlers

## Fix 10
- **File:** `worker/app.py`
- **Problem:** No error handling in `process_job()` — any uncaught exception
  would silently kill the worker process
- **Fix:** Wrapped in try/except, sets job status to `failed` on error

## Fix 11
- **File:** `api/requirements.txt`
- **Problem:** Dependencies had no pinned versions — non-reproducible builds
- **Fix:** Pinned all versions: fastapi==0.111.0, uvicorn==0.29.0, redis==5.0.4

## Fix 12
- **File:** All services
- **Problem:** Windows CRLF line endings in all Python and JavaScript files
  caused flake8 to report trailing whitespace errors in CI
- **Fix:** Converted all files to LF using dos2unix, added .gitattributes
  to enforce LF line endings going forward
