# Privacy

The monitor sits beside private conversations and messaging credentials. Its safest design is data minimization.

## Threat model

Consider:

- accidental source-control inclusion;
- verbose hook or bridge logs;
- prompt text copied into notifications;
- exception traces containing local paths or tokens;
- another local user reading runtime state;
- a compromised messaging adapter;
- inbound messages triggering local execution;
- synthetic tests built from real conversations;
- support bundles that include the outbox.

## Data classes

| Data | Default handling |
| --- | --- |
| Task state | Allowed |
| Sanitized task title | Allowed when useful |
| Model name | Optional; user preference |
| Short final response excerpt | Opt-in and locally redacted |
| Error category/status | Allowed |
| Raw error body | Local only; redact before sending |
| Prompt or conversation body | Do not collect by default |
| Tool arguments/results | Do not send |
| Local absolute path | Replace with a generic label |
| Messaging credential | Protected local store only |
| OAuth/API credential | Outside notifier scope |

## Minimal hook event

A hook record should contain only what is required to wake and correlate:

~~~text
schema_version
event_kind
task_key
turn_key
source
timestamp
sanitized_status
~~~

Write it locally with restricted permissions. Do not make a network call from the hook.

## Redaction

Before an error or optional result excerpt leaves the machine:

- remove authorization headers and known token formats;
- strip query strings and signed URL fragments;
- replace home-directory prefixes;
- remove email addresses and user identifiers unless explicitly needed;
- cap length;
- normalize control characters;
- prefer a structured status code over raw provider text.

Redaction should be deterministic and tested with synthetic secrets. If classification succeeds without a body, discard the body rather than trying to redact it perfectly.

## Local storage

Store runtime state under a dedicated current-user directory with restrictive ACLs. Separate:

- cursors and task-state metadata;
- outbox;
- adapter credentials;
- redacted operational logs.

Use rotation and retention. A delivered notification does not need to remain forever. Keep enough redacted metadata for deduplication and diagnosis, then expire it.

## Logging

Default logs should contain:

- component;
- event category;
- task key hash;
- transition;
- adapter result class;
- timing.

They should not contain:

- message bodies;
- prompt text;
- credentials;
- complete local paths;
- raw JSONL records.

Provide a temporary diagnostic mode only when necessary, with an automatic expiry and a clear warning.

## Repository hygiene

Public fixtures must be written from scratch. Do not “anonymize” a real conversation and assume every identifier was removed.

CI should scan for:

- absolute Windows user paths;
- common secret formats;
- messaging identifiers;
- assigned app-secret values;
- accidental auth files.

Manual review remains required because pattern matching cannot identify every private host or account value.
