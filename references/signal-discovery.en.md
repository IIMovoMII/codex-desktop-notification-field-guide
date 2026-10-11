# Signal discovery

[中文](signal-discovery.md)

Establish what this machine can observe before promising notification states.

## Local inventory

Inspect the OS, Desktop and bundled core versions, process tree, session shell, hook sources and trust, event storage, and CC Connect version and lifecycle. Record fields, types, and ordering without printing credentials or conversations.

Separate Codex task/turn identity, notification identity, and CC Connect destination identity. Titles are display text, not routing or deduplication keys. Distinguish Desktop main tasks, CLI, subagents, and merged-app Chat/Work surfaces. Sharing a sidebar does not imply sharing a local event format.

## What hooks establish

Key points checked against the [OpenAI Hooks reference](https://learn.chatgpt.com/docs/hooks) on 2026-10-11:

| Signal | Use and limit |
| --- | --- |
| `SessionStart` and submission events | Can wake startup; do not establish background readiness |
| `Stop` | Matching command hooks run concurrently and another may continue the turn; only a settling candidate |
| `stop_hook_active` | Describes prior continuation, not whether other hooks have finished |
| `Interrupt`, approval, or input signals | Verify support locally; interruption and waiting require explicit evidence |
| `SessionEnd` | Session cleanup; always synchronous, not a per-turn completion hook. `async = true` does not make it background; its default timeout is short and it is suitable only for quick local cleanup |
| `transcript_path` | May be null; the transcript format is not a stable hook interface |

Non-managed hooks require trust; changing a definition may require review again. Inspect existing `hooks.json` and inline `[hooks]` in the same layer, reuse the active representation, and avoid duplicate installation or removing others' hooks.

Hooks write minimal events, optionally start a helper, and return promptly using the event's output contract. They do not perform network delivery, full-history scans, or model inference. Keep diagnostic text out of protocol stdout.

`SessionEnd` is a common misconfiguration point: do not start a resident monitor, send network messages, or wait for heavy cleanup there. If Codex reports that an asynchronous `SessionEnd` is still being run synchronously, or reports `hook exited with code 1`, move the heavy work to `SessionStart`, `Stop`, or another event that supports asynchronous execution. Keep `SessionEnd` bounded, quick, and local, then verify both a real Desktop cold start and a real exit.

## Build versioned evidence

Use non-sensitive tasks for selected states: completion, user interruption, recoverable and terminal errors, approval/input requests, and resumption. Record correlation fields, real ordering, late writes, and duplicates, then author synthetic fixtures from scratch.

Prefer public structured interfaces exposed by the installed version. If JSONL or SQLite is needed, define minimal fields and proven semantics, read index metadata only, and record parser capabilities and versions. Ignore unrelated new records; when a changed field affects classification, suspend that inference with a visible local reason while retaining other proven capabilities.

Test source filtering with one Desktop, CLI, and subagent case each. A Windows example using `source="vscode"` is not a permanent product contract. Explicitly exclude cloud sessions with no local evidence rather than searching private files to guess.

## Inventory result

Produce a small table of selected state, evidence, correlation fields, support, and remaining checks. Mark input waiting unsupported without a signal. Mark installed-but-unexecuted hooks as pending load/trust.

Observe the smallest missing case next. A small feature should not become a project to scan every historical conversation.
