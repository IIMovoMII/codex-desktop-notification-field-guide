# Delivery and backlog recovery

[中文](delivery.md)

The state machine produces notices; the CC Connect sender delivers them. Keep their failure categories separate.

## A notification's lifecycle

~~~text
Persist → attempt when due → bridge explicitly accepts → record locally
             ↘ transient failure: retain and back off
             ↘ action needed: retain and pause destination
             ↘ missing acknowledgement: outcome uncertain
~~~

Keep a stable local ID, task/turn correlation, state, sanitized content, event time, destination revision, attempt count, and next attempt time. Specify both CC Connect project and destination session rather than choosing the first active session.

The checked [CC Connect v1.5.0 send command](https://github.com/chenhg5/cc-connect/blob/17c61062c2f9ce9bcdd45a2082e491f9743a2770/cmd/cc-connect/send.go) prints generic success; its [internal API](https://github.com/chenhg5/cc-connect/blob/17c61062c2f9ce9bcdd45a2082e491f9743a2770/core/api.go) returns `status=ok`. Neither is a phone read receipt or a remote message ID that the adapter can require. Recheck the contract on upgrade.

A crash after acceptance but before local bookkeeping, or a timeout after remote receipt, creates uncertainty. Without remote idempotency, both zero loss and zero duplication cannot be guaranteed. Keep the same notification ID and use bounded retry or review according to the chosen policy; do not call indefinite retransmission safe.

## Bounded retries

Back off transient network/service failures with jitter and any platform retry-after value; persist the next attempt. Enforce a real send timeout so one hanging item cannot block the queue. Add a caller deadline where the chosen send path lacks one.

Separate invalid auth/target, temporarily exhausted quotas, network errors, and uncertain outcomes. Quotas may recover and are not always permanent failures. Retain unknown failures and surface them after limited attempts. Pause destinations requiring rebinding or configuration repair, then allow targeted recovery.

Drain due items in bounded batches with rate limits and fair scheduling. Avoid needlessly slow one-item-per-loop drains and unlimited recovery bursts. Preserve original event times and optionally label delayed delivery. Agree on expiry, coalescing, or discarding beforehand; never silently empty the queue.

## Why a restart releases many messages

Check four facts first: oldest pending time, last failure category, next retry time, and actual sender lifetime.

- Persisted but stopped with Desktop: the messages survived while retries waited for another run.
- Process alive but send path unavailable: inspect readiness, auth, network, destination, and local socket.
- Ready but not draining: inspect retry clocks, expired leases, scheduling, and dependence on fresh hook wakeups.
- Accepted but resent: inspect durable bookkeeping, notification identity, and ambiguous delivery.

A backlog alone does not establish a CC Connect bug or justify full-disk polling every second.

## Desktop exit policies

| Policy | Behavior |
| --- | --- |
| Stop strictly with Desktop | Preserve pending items until the next start; no retries after exit |
| Bounded sender-only finishing | Stop observation; keep the sender and dedicated bridge until empty or deadline |
| Independent delivery service | Retry after Desktop closes, with user acceptance of persistent background presence |

The guide does not choose for the user. Bounded finishing must handle offline state, shutdown, deadline expiry, Desktop reopening, and enqueue at the exit boundary. Retain remaining items and record why; do not wait indefinitely to “send everything.”

Connect/disconnect from shared CC Connect without terminating it or replacing shared configuration. Verify process identity before restarting a dedicated instance.

## Local API and message content

Prove that the outbound path sends the prepared payload directly, without a CC Connect agent rewriting it or console logs becoming notification text. Prefer argument arrays or stdin over shell interpolation, avoiding special-character and command-line length failures.

A Windows field incident had a connected bridge but a failing local socket path. Test creation, connection, and exchange with the actual runtime rather than checking a file or an old ready log. If shortening a path, distinguish an alias from migration and retain one data copy. Measured path lengths are not universal Windows limits.

## Optional inbound control

The user chooses notification-only or bidirectional behavior; this pack does not mandate default-deny inbound for every product. For existing Desktop conversations, display a short alias in notices and map it locally to a stable task ID. An explicit target followed by “continue” is more reliable than guessing the last-opened window.

Define senders, actions, targets, busy-state behavior, duplicate protection, and cancellation before enabling it. Do not concatenate arbitrary text into commands. A CC Connect CLI agent session is not an existing Desktop conversation. Verify that the installed continuation interface wakes the intended task, appends to its original history, and does not create the wrong session. Command availability alone proves none of that; mark unverified control as pending implementation.

## Platform changes and recovery

Pause the destination, complete the new binding through [platform selection](cc-connect-platform-selection.en.md), verify a synthetic notice, then switch. Let the user keep old queued items on the old destination, migrate them, or clear them. Version destinations to prevent sending old notices to a new group/account. No need to rebuild state classification or read cursors.
