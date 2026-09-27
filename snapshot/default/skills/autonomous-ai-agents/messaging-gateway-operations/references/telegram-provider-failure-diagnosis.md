# Diagnosing Telegram model-provider failures

Use when Telegram displays a generic message such as “The model provider failed after retries.” The visible message intentionally omits provider details; diagnose from gateway logs.

## Evidence sequence

1. Search gateway/agent logs by the numeric Telegram user or chat ID and the screenshot time window.
2. Correlate timestamps carefully. Telegram screenshots show the phone’s local time, while gateway logs use the server/profile timezone. Infer a timezone offset only when message text and ordering match; state the offset as an inference, not a fact.
3. Verify four layers separately:
   - inbound Telegram update was received;
   - the agent/model request started;
   - the provider returned or failed, including provider, model, HTTP/error class, retry count, and session ID;
   - the adapter attempted and completed user-visible delivery.
4. Check current gateway status and provider authentication without printing secrets.
5. Run isolated, minimal direct probes against the configured primary model and any proposed fallback. A successful current probe establishes recovery now; it does not prove the earlier failure’s exact upstream cause.
6. Inspect the effective fallback chain before changing it. Add a fallback only after its model/provider probe succeeds, then restart the gateway and verify a new PID, clean drain, Telegram reconnect, and hook load.
7. For a true end-to-end result, require a fresh inbound Telegram message from the affected chat and verify its corresponding outbound delivery. A CLI model probe or outbound-only send is not inbound E2E proof.

## Classification and reporting

- If inbound and outbound Telegram logging works but the model call fails, describe this as a provider/model-path failure, not a Telegram transport failure.
- A generic HTTP 404 with no “model not found” signal may be a transient provider routing error. Do not claim the model is invalid without evidence.
- Hermes fallback behavior is classifier-dependent. A configured fallback normally covers rate limits, 5xx/server errors, connection failures, and explicit model-not-found cases; it may not activate for a generic bare 404 classified as retryable unknown. Do not promise that adding a fallback specifically fixes such a 404.
- Persisted failed user turns and message-alternation repairs are secondary effects, not necessarily the root cause. Avoid deleting or resetting a user session unless corruption is demonstrated or the user accepts losing that context.
- Distinguish “currently healthy” from “E2E verified for the affected user.” Report the latter only after a new inbound turn succeeds.

## Safe remediation pattern

- Restore/refresh provider authentication when logs support an auth failure.
- Keep a working primary if the outage was transient; add a tested fallback for supported failover classes rather than changing the primary reflexively.
- Restart only when configuration changes require it. On Windows, if an in-process restart is refused because the caller descends from the gateway, use the validated one-shot Task Scheduler procedure in `references/windows-inprocess-gateway-restart.md` and remove temporary artifacts after verification.
