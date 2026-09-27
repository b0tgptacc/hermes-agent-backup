# Gunicorn resilience for small containerized business apps

Use this reference when a Django/Gunicorn service is nominally healthy but intermittently stops answering requests, especially on a LAN or behind simple port publishing.

## Diagnostic signature

A material pattern is:

- Gunicorn runs its default single synchronous worker;
- logs contain repeated `WORKER TIMEOUT` together with `Error handling request (no URI read)`;
- the traceback is blocked in socket receive before a URI is parsed;
- the container is not OOM-killed and PostgreSQL remains healthy;
- requests recover after the worker is killed and respawned.

Do not treat Gunicorn's generic “Perhaps out of memory?” line as proof of OOM. Check container state, restart count, memory usage, and the actual stack location.

## Tight reproduction

Confirm the failure before changing configuration:

1. Open a TCP connection to the published Gunicorn port.
2. Send no HTTP request bytes.
3. While keeping that socket open, request `/health/` through a second connection with a short timeout.
4. Close the stalled socket and confirm health recovers.

With one sync worker, the second request can time out because the only worker is blocked before parsing a URI. This reproduction is specific, fast, reversible, and directly tests the observed symptom.

## Minimal production fix

For a small internal Django service, use bounded concurrency rather than the one-worker sync default. A proven baseline is:

```text
--worker-class gthread --workers 2 --threads 4 \
--timeout 60 --graceful-timeout 30 --keep-alive 5 \
--access-logfile -
```

Tune from measured workload and resource limits; the values are a resilient small-service baseline, not a universal capacity formula. Preserve explicit healthchecks and database dependency checks.

## Regression protection

Add a deployment-config test that parses the actual container command and requires:

- `gthread` worker class;
- at least two workers;
- at least two threads.

The static test prevents accidental reversion, but it does not replace the live socket reproduction.

## Verification gate

After rebuilding and recreating the web service:

1. Require both web and database containers to be healthy.
2. Repeat the stalled-socket probe; `/health/` must return HTTP 200 while the first connection remains incomplete.
3. Verify localhost and LAN routes produce the expected status or login redirect.
4. Run the full test suite, framework check, and migration drift/check inside the real containerized stack.
5. Inspect fresh logs for worker boot count, worker class, new timeouts, and request access lines.
6. Confirm restart count is unchanged and `OOMKilled=false`.

## Pitfalls

- Restarting the container alone masks the symptom; it does not remove the single-worker bottleneck.
- Increasing only the timeout makes outages longer when the worker is monopolized.
- A host curl to the LAN IP proves host routing and allowed-host policy, not cross-device reachability.
- A static Dockerfile test proves configuration intent, not runtime behavior; verify the live PID command line and socket behavior.
