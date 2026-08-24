# Delivery

Reliable notification delivery is a queueing problem with a replaceable channel adapter.

## Durable outbox

Persist a notification before attempting network delivery. A record can contain:

~~~text
notification_id
deduplication_key
created_at
task_title_redacted
state
summary_redacted
attempt_count
next_attempt_at
adapter_id
schema_version
~~~

Do not include prompts, tool arguments, credentials or raw rollout records.

Use atomic state updates or a small transactional database. After a crash, every accepted-but-unconfirmed item should be safe to retry.

## Delivery contract

An adapter should expose:

- health check;
- send one normalized notification;
- classify retryable versus permanent failure;
- return a provider delivery identifier when available;
- redact its own error details;
- report quota or authorization status.

The Codex state machine should not know platform-specific request shapes.

## Retry policy

For retryable failures:

- use bounded exponential backoff with jitter;
- honor a provider retry-after value;
- persist the next attempt time;
- cap rapid retries;
- keep the item in the outbox.

For permanent failures:

- retain a redacted dead-letter record;
- surface a local health warning;
- do not loop forever;
- never include the channel secret in the warning.

Remove or mark an item delivered only after confirmed acceptance. If a provider cannot offer idempotency, keep the local deduplication key and tolerate the narrow uncertainty after a network timeout.

## Rate and reply limits

Messaging platforms can impose:

- daily quotas;
- per-minute quotas;
- limits after several unanswered messages;
- binding requirements;
- message-length limits;
- account-review or bot-policy restrictions.

Measure the actual selected channel and encode these limits in the adapter. Do not generalize one platform's behavior to another.

If notifications can be coalesced without losing meaning, combine several terminal results into a digest only when the user explicitly prefers it.

## CC Connect and local bridges

When using CC Connect or another local bridge:

- manage its lifecycle independently from task classification;
- verify that the bridge is bound to the intended outbound conversation;
- store its credentials in a restricted runtime directory;
- treat bridge stdout as untrusted and redact before logging;
- health-check it before draining the outbox;
- keep the queue when the bridge is offline.

Do not make the monitor dependent on an interactive QR flow after every restart. Binding should be a deliberate first-use operation with a clear expired-state recovery path.

## Outbound-only boundary

The default adapter sends notifications and ignores inbound chat content.

Inbound control would require a separate security design:

- authenticated sender allowlist;
- replay protection;
- explicit command grammar;
- user confirmation for sensitive actions;
- audit log;
- rate limiting;
- no arbitrary shell execution.

Unless those controls are intentionally designed and reviewed, an inbound message must never launch Codex CLI or execute local actions.

## Changing channels

Keep the outbox's normalized notification schema independent of the platform. To move from one messenger to another:

1. pause delivery;
2. configure and validate the new adapter;
3. choose how to handle queued items;
4. switch the adapter ID transactionally;
5. send a synthetic test;
6. disable the old adapter credential;
7. resume the queue.

State detection and JSONL cursors should not change.
