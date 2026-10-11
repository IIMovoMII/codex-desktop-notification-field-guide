# Validation and troubleshooting

[中文](validation.md)

Validate the selected features, not every possible extension. Label evidence by stage: files written, command passed, Desktop loaded, real state detected, message visible on the phone.

## Minimum acceptance path

1. Use synthetic events for classification, deduplication, recovery, and content filtering.
2. Execute the installed hook command in the actual shell. Check exit status, stdout, Unicode/spaces/special characters in paths, and helper survival.
3. When convenient for the user, actually close and reopen Desktop from normal entry points and complete hook trust. Verify first-event startup with one monitor. Test at least two real local entry points; process-triggered designs also need startup without a hook.
4. Trigger a selected normal state and compare the outbox, bridge acceptance, and phone-visible content. Verify errors, interruption, and waits according to selected scope.
5. Test pending messages at exit, a temporary outage, and restart against the chosen exit/catch-up policy.
6. If account switching is in scope, use the existing switch workflow and accept each mode after restart. Do not change accounts or disrupt live tasks merely to test.

Manually invoking a hook from the current window is not a real Desktop cold start. Correct files do not establish that an old process reloaded them or that hooks are trusted.

## High-value boundary cases

| Area | Meaningful cases |
| --- | --- |
| Startup | Temporarily invisible process, partial metadata, concurrent hooks, alive-but-unready service, CLI/subagent, missing config, lock release after helper exit |
| Process identity | PID reused by another process, legacy state without an identity version, stale “API started” log after service exit; confirm relaunch rather than a false online result |
| State | Concurrent Stop continuation, candidate cancellation, transient 503 then success, final failure, completion/interruption order, late old turn, long silence |
| Waiting | Duplicate request, response/resume, resolved-but-unsent alert, new request |
| Exit | Main app exit, auxiliary restart, multiple windows, marker expiry, late writes, reopening |
| Persistence | Partial line, replacement, truncation, path aliases, overflow, sleep/resume, crash between cursor/state/enqueue |
| Delivery | Unready endpoint, timeout, quota, expired auth, crash after acceptance, backlog drain, destination change, shared-instance survival |
| Content | Synthetic secrets, paths, long text, quotes/newlines, changed titles without duplicate notices |
| Resources | Synthetic long replies, many completed turns, and long idle runs; verify bounded active evidence, released terminal bodies, and measured CPU/memory |
| Inbound, if selected | Explicit target, duplicate titles, stale mapping, busy task, unauthorized/replayed message, real continuation of the original task |

Test different orders to expose actual races, not the presence of implementation function names. Use synthetic privacy values. Measure idle CPU, bytes read, startup latency, and queue age instead of claiming unmeasured “zero overhead.”

## Targeted troubleshooting

| Symptom | Evidence first | Acceptance after repair |
| --- | --- | --- |
| Hook `exit code 1`, no application log | Actual shell, syntax, paths, imports, stdin decoding | Reproduce in the same execution context, then test SessionStart/Stop |
| `SessionEnd` says an async hook is running synchronously, or exits with code 1 | The event is always synchronous with a short timeout; inspect for network, resident, or heavy work | Move heavy work to an event that supports async execution; keep `SessionEnd` quick local cleanup and verify a real exit |
| Hooks written but not invoked | Active layer, trust, loaded definition | Real triggering, not file inspection alone |
| Process alive but no messages | Process identity, endpoint readiness, queue timing/errors | Real connection and synthetic delivery in that instance |
| `doctor` says online but hooks no longer relaunch | Identity version, executable, and creation time in state; a recent startup line is not enough | PID-reuse fixture is rejected and the next valid hook self-recovers |
| Batch arrives after restart | Sender lifetime, backoff, exit policy | Catch-up at the agreed time |
| Many notices for one incident | Current turn, terminal slot, ledger, uncertain delivery | Replay/restart without creating new local notices |
| Unknown events after upgrade | Version and minimal field differences | Verify affected states after adapter update |

Find the cause before changing behavior. Automate recovery for naturally recurring conditions; a one-time configuration mistake does not justify continuous full scans. A broken bridge cannot reliably carry its own health alert, so keep local diagnosis available.

## Limits of field evidence

| Reference environment | Available evidence | Does not establish |
| --- | --- | --- |
| Windows, Codex core 0.159.2, CC Connect 1.5.0 | Local reference implementation's startup/state/outbox regression tests and actual PowerShell hook-command tests | A runtime shipped in this repo or compatibility across all systems/builds |
| Windows, CC Connect 1.5.0 | Historical QQ delivery, local socket-path failure, and shortened-path verification | Readiness from path existence or a universal runtime-independent length limit |
| Deployment with corrected hook command | Command-level verification | Unperformed Desktop reload, trust, or cold-start checks |

These are sources of experience, not certification of downloadable software. This repository contains neither the runtime nor its full runtime fixture suite.

## Maintenance and handoff

Provide local status/diagnosis, targeted retry, pause/resume, update, and uninstall paths in the chosen interface. Bound logs, queues, and recovery-copy retention. On upgrade, retest affected parsing, hook execution, startup, and delivery; do not inspect the whole system for every notice.

State what is verified, unsupported, pending binding/restart, and recoverable. The document validator checks structure, local links, bilingual reference coverage, and limited privacy patterns. It does not prove translation semantics, external links, hook protocols, or runtime behavior.
