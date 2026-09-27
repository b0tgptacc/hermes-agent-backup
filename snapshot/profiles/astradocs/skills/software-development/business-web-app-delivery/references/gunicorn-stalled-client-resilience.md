# Gunicorn resilience to stalled clients

Use this runbook when a containerized Django/Gunicorn service appears intermittently down while the container and health status often recover on their own.

## Diagnostic signature

A high-signal pattern is:

- Gunicorn runs with its defaults: one `sync` worker;
- logs repeat `WORKER TIMEOUT` and `Error handling request (no URI read)`;
- memory usage is normal and the container was not OOM-killed;
- a client that opens TCP but does not complete an HTTP request makes `/health/` time out;
- closing that connection immediately restores health.

Do not treat Gunicorn's speculative `Perhaps out of memory?` message as proof of OOM. Verify container state (`OOMKilled`), memory, restart count, and the preceding stack trace. A stack blocked in socket `recv()` before a URI is read points to an incomplete or slow client, not application computation.

## Tight reproduction

Build a deterministic probe that:

1. opens a TCP connection to the published application port;
2. sends no HTTP bytes;
3. requests `/health/` through a second connection with a short timeout;
4. closes the stalled connection;
5. requests `/health/` again.

The pre-fix signal is: the concurrent health request times out and the post-close request returns HTTP 200. Run this before changing configuration so the loop is proven red-capable.

## Minimal production fix

For a small internal Django service, replace the single default sync worker with bounded concurrent capacity, for example:

```dockerfile
CMD ["gunicorn", "service_crm.wsgi:application", "--bind", "0.0.0.0:8000", "--worker-class", "gthread", "--workers", "2", "--threads", "4", "--timeout", "60", "--graceful-timeout", "30", "--keep-alive", "5", "--access-logfile", "-"]
```

Tune worker/thread counts to CPU, memory, request characteristics, and database connection limits. The durable requirement is not these exact numbers; it is that one incomplete connection cannot monopolize all serving capacity.

Add a regression test that parses the deployed command and requires a concurrent worker class plus explicit multi-request capacity. This static test does not replace the live stalled-client probe.

## Deployment and verification

1. Rebuild and recreate only the web service; preserve the database volume unless data recovery requires otherwise.
2. Wait for explicit web and database health.
3. Confirm the running PID 1 command contains the intended worker class, worker count, threads, and timeouts.
4. Re-run the exact stalled-client probe. The concurrent health request must return HTTP 200 while the stalled connection remains open.
5. Run the full test suite, framework check, migration drift/check, localhost route probe, and LAN/reverse-proxy route probe as applicable.
6. Verify restart count, `OOMKilled=false`, bounded memory, and clean post-deploy logs.
7. Keep access logging enabled or provide equivalent request observability so future network-triggered stalls can be diagnosed.

## Pitfalls

- Restarting the container without changing serving concurrency only clears the symptom.
- Raising the timeout alone leaves the only sync worker blocked for longer.
- Adding workers without checking database connection capacity can move the bottleneck to PostgreSQL.
- A local healthcheck can pass between stalls; reproduce under a held incomplete connection.
- HTTP 200 after the held socket is closed proves recovery, not resilience. The health request must succeed while the socket is still open.
