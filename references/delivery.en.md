# Delivery through CC Connect

Reliable notification delivery is a queueing problem with CC Connect as the required bridge and a user-selected CC Connect platform.

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
cc_connect_platform
schema_version
~~~

Do not include prompts, tool arguments, credentials or raw rollout records.

Use atomic state updates or a small transactional database. After a crash, every accepted-but-unconfirmed item should be safe to retry.

## CC Connect sender contract

The local CC Connect sender should expose:

- health check;
- send one normalized notification;
- classify retryable versus permanent failure;
- report accepted delivery; preserve a provider delivery identifier only when the selected CC Connect path actually provides one;
- redact its own error details;
- report quota or authorization status.

The Codex state machine should not know platform-specific request shapes. The sender translates the normalized notification into the selected CC Connect project and session.

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

Remove or mark an item delivered only after the selected CC Connect command or API reports success. A generic success response such as `status=ok` is sufficient evidence of acceptance when that is all the bridge exposes; do not invent a provider message identifier. If a provider cannot offer idempotency, keep a restart-stable local deduplication key and tolerate the narrow uncertainty after a network timeout. The key must not depend on rendered title or summary text.

## Rate and reply limits

Messaging platforms can impose:

- daily quotas;
- per-minute quotas;
- limits after several unanswered messages;
- binding requirements;
- message-length limits;
- account-review or bot-policy restrictions.

Measure the selected CC Connect platform and encode its limits in the sender boundary. Do not generalize one platform's behavior to another. Personal Weixin is not recommended for this workload; see [CC Connect platform selection](cc-connect-platform-selection.en.md).

If notifications can be coalesced without losing meaning, combine several terminal results into a digest only when the user explicitly prefers it.

## CC Connect boundary

When using CC Connect:

- manage its lifecycle independently from task classification;
- verify that the bridge is bound to the intended outbound conversation;
- store its credentials in a restricted runtime directory;
- treat bridge stdout as untrusted and redact before logging;
- health-check it before draining the outbox;
- keep the queue when the bridge is offline.

Do not make the monitor dependent on an interactive QR flow after every restart. Binding should be a deliberate first-use operation with a clear expired-state recovery path.

Prefer a dedicated CC Connect project and fixed destination for notifications. The sender should forward the normalized payload through a proven outbound path without asking another model to expand it, and must never treat CC Connect logs, prompts or agent replies as notification content. Reuse an existing project only after proving that a notification cannot trigger an extra agent conversation; otherwise create a dedicated project. The real test should compare the received text with the local outbox payload.

## Optional inbound boundary

Notification-only is the smallest implementation, but it is a user choice rather than a mandatory repository policy. Ask whether the user wants only notifications or also wants secured inbound control. The notification pipeline must remain independent either way.

Inbound control would require a separate security design:

- authenticated sender allowlist;
- replay protection;
- explicit command grammar;
- user confirmation for sensitive actions;
- audit log;
- rate limiting;
- no arbitrary shell execution.

If inbound control is selected, implement and review those controls as a separate module. Otherwise ignore inbound content. Never enable arbitrary shell execution merely because CC Connect supports interactive sessions.

## Changing CC Connect platforms

Keep the outbox's normalized notification schema independent of the platform. To move from one messenger to another:

1. pause delivery;
2. ask the user to choose and configure the new CC Connect platform;
3. choose how to handle queued items;
4. switch the CC Connect platform and destination transactionally;
5. send a synthetic test;
6. disable the old platform credential when the user no longer needs it;
7. resume the queue.

State detection and JSONL cursors should not change.
