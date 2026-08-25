# Incremental monitoring

Low overhead comes from reacting to filesystem changes and remembering exactly how far each relevant file has been read.

## Event-driven wakeups

Use the operating system's native filesystem event mechanism through a well-tested library or a small native wrapper—for example `ReadDirectoryChangesW` on Windows, FSEvents on macOS, or inotify on Linux. Watch only discovered rollout roots.

A change notification says “something changed,” not what the final task state is. Use it to schedule a bounded incremental read.

Expect:

- duplicate notifications;
- coalesced notifications;
- rename pairs;
- queue overflow;
- changes before a watcher is fully attached.

A periodic lightweight reconciliation should repair missed wakeups. It should compare directory metadata and known cursors, not parse every historical line.

## Cursor model

For each file, persist:

- stable file identity when available;
- normalized relative path;
- last byte offset;
- observed size and modification time;
- trailing partial-line bytes;
- session/task identity discovered from metadata;
- parser schema version.

Read in binary mode, split complete newline-delimited records, and keep an incomplete tail until the next append. Decode with the proven file encoding.

## Rotation, truncation and replacement

If:

- size is smaller than the cursor;
- file identity changes;
- the prefix hash no longer matches;
- a rename produces a new path;

then do not continue from the old offset. Reclassify the file, determine whether it is a new session or replacement, and rebuild from a safe bounded point.

Never silently seek to the end of an unknown replacement; that can miss its terminal event.

## Startup reconciliation

At monitor startup:

1. load cursor state;
2. inventory only relevant roots;
3. identify files changed since the last clean shutdown;
4. validate identity and cursor bounds;
5. read new bytes;
6. attach watchers;
7. repeat a narrow reconciliation to close the startup race.

For first use, establish a baseline without notifying on every old completed task. Mark historical terminal events as seen, then notify only for work active after the baseline boundary.

## Process lifecycle

The monitor must follow Codex Desktop regardless of whether the user launches it from an icon, Start menu, terminal, updater, protocol link or another normal entry point. Two valid product choices are:

- lazy lifecycle: a trusted Codex lifecycle hook starts the single-instance monitor on the first observable event;
- immediate lifecycle: an operating-system process event or user-approved login observer starts the monitor as soon as Desktop appears.

Ask which guarantee the user wants. Do not require a wrapper command. The monitor can exit when:

- no Desktop process remains;
- no relevant task is settling;
- the outbox is durably saved;
- the delivery bridge has no required local cleanup.

Use an idempotent single-instance lock so several hooks or process events do not launch several monitors. Restore the persisted event ledger before accepting new events so restart races cannot duplicate alerts. A manual health command remains useful for repair and diagnosis, but normal Desktop launch should not depend on it.

If the notifier owns a dedicated CC Connect process, it may stop that process after the outbox settles. If it shares an existing CC Connect instance, it must only disconnect and must never terminate the shared process. If no trusted lifecycle hook or process observer exists, explicitly offer a user-approved login-time observer or manual start and state the reduced guarantee; do not claim automatic following works.

## CPU and disk budget

Measure:

- filesystem wakeups per active turn;
- bytes read per append;
- periodic reconciliation duration;
- idle CPU;
- state-file write frequency;
- startup catch-up time.

Batch cursor persistence sensibly while ensuring that a crash only replays a small, deduplicated window.

No task-status logic should scan unchanged files once per second.

## SQLite use

Use SQLite only for metadata that is not safely available elsewhere, such as a task title. Open read-only when possible, respect WAL semantics and use bounded retry for transient locks.

Do not query full message bodies merely to build a notification. Cache a sanitized title once discovered.

## Parser evolution

Unknown JSONL record types should normally be ignored and counted. A changed record that affects terminal classification should fail safely into an “unknown evidence” path and be captured as a redacted fixture for review.

Version the parser and record which Codex build produced each fixture.
