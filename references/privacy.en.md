# Privacy and data boundaries

[中文](privacy.md)

State decisions can stay local. Establish which content the user chose before sending it off the machine.

## Content choices

| Content | Suggested starting point |
| --- | --- |
| State, event time, stable notification alias | May be sent |
| Task title and model name | User choice; titles can also be private |
| Short reply excerpt | Process only if selected, with local redaction |
| Raw prompts, tool inputs/outputs, full errors/history | Not ordinary notification content |
| Messaging credentials and real recipient IDs | Restricted local configuration |
| Codex OAuth/API credentials | Not needed or managed by the notifier |

An excerpt is a content option and does not require another model call. Inbound task continuation is a separate data flow with separately stated scope.

## Minimal events and logs

Hooks normally retain correlation fields, event type, time, and necessary status. Reading JSONL may transiently decode a line containing message text; do not advertise that bodies never enter memory. Discard unneeded fields promptly instead of storing them in normal state, logs, or queues.

Prefer structured classification. When error text is required, remove auth headers, tokens, query/signature fragments, and personal identifiers/paths; cap length and clean control characters. Regex redaction cannot prove the absence of all secrets; collecting less is more dependable.

Cursors may need real paths and task IDs, which stay local. Logs use categories, timings, and non-revealing correlation values. Sent ledgers keep only deduplication information. Queued excerpts can remain sensitive, so restrict access and retention.

## Installation, migration, and removal

Keep notifier settings separate from Codex login profiles; account switching need not copy bot credentials. Patch only owned hook entries on installation, update, and removal.

Retain recovery material according to the user, usually one known-good copy or a field-level rollback record rather than unbounded backups. On removal, stop owned components, remove owned automatic entry points, then let the user retain or delete queue/binding data. Shared bridges and Codex history are outside the deletion scope.

## Public materials

Write fixtures from scratch rather than copying real conversations with renamed entities. Publish structure, methods, and synthetic cases. Versions and reproduction steps can be public; real configuration, auth, recipients, machine paths, and message bodies must not accompany the docs. Automated scans are limited screening; inspect the diff before publishing.
