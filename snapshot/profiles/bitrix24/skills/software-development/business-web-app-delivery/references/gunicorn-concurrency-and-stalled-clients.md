# Gunicorn concurrency and stalled-client resilience

Use this runbook when a containerized Django/WSGI application is nominally healthy but intermittently stops answering, especially when Gunicorn logs `WORKER TIMEOUT` together with `Error handling request (no URI read)`.

## Diagnostic interpretation

A default Gunicorn command can start only one synchronous worker. A TCP client that connects but does not complete an HTTP request can occupy that worker until timeout. With no other worker/thread available, application routes and the healthcheck can become unavailable even though:

- the container remains `running`;
- Docker reports no restart;
- memory usage is low;
- PostgreSQL is healthy.

Do not infer OOM merely from Gunicorn's generic `was sent SIGKILL! Perhaps out of memory?` wording. Check `docker inspect` (`State.OOMKilled`) and `docker stats` before accepting that hypothesis.

## Tight reproduction probe

Establish one raw TCP connection to the published application port, send no request bytes, then issue a short-timeout request to `/health/` from a second connection.

Expected RED for a single sync worker:

1. raw socket connects and remains open;
2. `/health/` times out;
3. closing the raw socket makes `/health/` return HTTP 200 again.

This directly tests the failure mode; a normal curl loop does not.

## Minimal production correction

Give the service bounded concurrent request capacity. A proven small internal-CRM baseline is:

```dockerfile
CMD ["gunicorn", "service_crm.wsgi:application", "--bind", "0.0.0.0:8000", "--worker-class", "gthread", "--workers", "2", "--threads", "4", "--timeout", "60", "--graceful-timeout", "30", "--keep-alive", "5", "--access-logfile", "-"]
```

Treat the exact worker/thread counts as a starting point, not a universal formula. Tune for CPU, memory, request latency, database connection limits, and workload. The durable requirement is that one incomplete client cannot consume all serving capacity.

Add a regression test that parses the deploy command and requires:

- `--worker-class gthread`;
- at least two workers;
- at least two threads.

Watch the test fail against the unsafe default before changing production configuration.

## Deployment and verification

1. Rebuild and recreate only the web service; preserve the database volume.
2. Wait for explicit container health.
3. Confirm the live PID 1 command contains the intended worker class, worker count, thread count, and timeouts.
4. Re-run the raw-socket probe. Expected GREEN: `/health/` returns HTTP 200 while the incomplete connection remains open.
5. Verify localhost and LAN routes, expected authentication redirects, and the real PostgreSQL-backed Django check/migration state inside the container.
6. Run the targeted regression test and full suite.
7. Check restart count, `OOMKilled`, resource usage, and fresh logs for new `CRITICAL`/`ERROR` entries.

## Pitfalls

- Restarting the container can hide the symptom without correcting the serving-capacity defect.
- Raising the timeout alone lengthens the outage when all sync workers are occupied.
- A healthy database does not prove the web worker can accept another request.
- A host-side Django check may use SQLite defaults; run production-state checks inside the web container when Compose supplies PostgreSQL settings.
- Access logging improves incident evidence but is not the concurrency fix by itself.
