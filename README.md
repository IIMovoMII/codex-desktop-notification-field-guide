<div align="center">

# Codex Desktop Notification Field Guide

**Turn Codex Desktop lifecycle signals into reliable, privacy-aware notifications without polling every conversation or asking another model to guess the state.**

[![Field Guide](https://img.shields.io/badge/type-field%20guide-6f42c1)](#what-this-is)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4)](#scope)
[![Architecture](https://img.shields.io/badge/architecture-event--driven-0f766e)](#architecture)
[![Validation](https://github.com/IIMovoMII/codex-desktop-notification-field-guide/actions/workflows/validate.yml/badge.svg)](https://github.com/IIMovoMII/codex-desktop-notification-field-guide/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

[简体中文](README.zh-CN.md) · [Agent entrypoint](SKILL.md) · [Companion auth-switching guide](https://github.com/IIMovoMII/codex-auth-switching-field-guide)

</div>

## What this is

This repository is **not a bot package or a preconfigured messaging bridge**. It is a field guide for building a local notification companion around the Codex Desktop version, event formats and messaging channel available on one machine.

The design emerged from a practical need: start Codex normally from the Desktop icon, leave a long task running, and receive a message when the task completes, fails, pauses or needs attention. Long silence is allowed. The monitor should not burn CPU scanning all history, expose prompts to a remote service, or launch Codex CLI in response to chat messages.

## Why one signal is not enough

Hooks are fast, but their event coverage and timing can vary. JSONL contains richer evidence, but reading every file repeatedly is wasteful. Process exit is useful, but it cannot explain why a task stopped. Reliable classification comes from combining small, independent signals.

## Architecture

~~~mermaid
flowchart LR
    H[Codex hooks] --> N[Local normalizer]
    J[Incremental JSONL tail] --> N
    P[Desktop process state] --> N
    N --> S[Per-task state machine]
    S --> D[Deduplication and privacy filter]
    D --> O[Durable outbox]
    O --> A[Channel adapter]
    A --> Q[QQ, CC Connect or another messenger]
~~~

Hooks wake the system quickly. Windows directory notifications wake the incremental reader when files change. A lightweight periodic reconciliation protects against missed events; it does not scan all conversations or infer failure from elapsed time.

## Events worth notifying

| State | Evidence standard | Notify? |
| --- | --- | --- |
| Completed | terminal completion event or validated stop state | Yes |
| Structured error | explicit error type/status/code | Yes |
| Unknown error | terminal failure with unclassified details | Yes, with a generic label |
| User pause/interruption | explicit interruption evidence | Yes |
| Waiting for approval | explicit approval request | Yes |
| Waiting for input | explicit input request or version-proven equivalent | Yes |
| Long-running silence | no terminal evidence | No |
| Planned restart | maintenance marker from a cooperating tool | No crash alert |

Do not create a “probably stuck” notification from a timer alone. Codex tasks can legitimately run for hours. A timeout may be useful for monitoring the notifier itself, but not for judging the task.

## Core design rules

1. **Observe Desktop directly.** Do not require the user to launch Codex through a wrapper.
2. **Use hooks as hints, not absolute truth.** Normalize them and corroborate terminal decisions when needed.
3. **Tail only appended bytes.** Persist per-file cursors and use Windows filesystem notifications for wakeups.
4. **Filter the source early.** Ignore CLI tasks, subagents and monitor-generated activity to prevent loops.
5. **Model transitions per task.** Completion, failure, pause and waiting are states, not keywords.
6. **Prefer structured errors.** Text matching is a fallback for version gaps; unknown failures still deserve a notification.
7. **Keep prompts local.** A hook should write the minimum sanitized event and return immediately.
8. **Queue before sending.** Remove a notification only after the channel confirms success.
9. **Make delivery replaceable.** State detection should not know whether the adapter uses CC Connect, an official QQ bot or another service.
10. **Coordinate planned maintenance.** An auth switcher or updater can write a short-lived marker so a planned restart is not reported as a crash.

## Guide map

| Read this | When you need to |
| --- | --- |
| [Signal discovery](references/signal-discovery.md) | Inspect hooks, JSONL, processes and source identifiers |
| [State machine](references/state-machine.md) | Combine signals without timer-based false alarms |
| [Incremental monitoring](references/incremental-monitoring.md) | Build low-overhead Windows watching and durable cursors |
| [Delivery](references/delivery.md) | Design the outbox, retries, adapters and one-way channel boundary |
| [Privacy](references/privacy.md) | Minimize and redact local and remote data |
| [Validation](references/validation.md) | Test state races, failures, restarts and channel outages |

## Starting with the normal Desktop icon

The user should keep launching Codex from the Desktop or Start menu. A safe integration can start lazily from a supported Codex lifecycle hook:

1. the hook records a small local event;
2. it checks whether the local monitor is alive;
3. if needed, it starts the monitor and delivery bridge in the background;
4. it exits quickly;
5. the monitor later stops after Desktop has exited and pending terminal events have settled.

This avoids a startup wrapper and avoids a permanent boot-time service. Exact hook names and synchronous/asynchronous behavior must be tested against the installed Codex build.

## Delivery channels

Keep a narrow adapter contract:

~~~text
send(notification) -> accepted delivery identifier
healthcheck() -> channel status
classify_failure(error) -> retryable or permanent
~~~

CC Connect can be one adapter when it supports the desired platform. An official QQ bot, webhook or another local bridge can be another. Platform quotas, reply gates and account policies belong in the adapter, not the Codex state machine.

Outbound-only is the safer default. Receiving a chat message should not launch Codex CLI or execute commands unless the user designs and secures a separate control plane.

## Hard-won lessons

- A hook can run synchronously even when its configuration looks asynchronous; measure actual behavior and keep the hook tiny.
- Completion and interruption events can race. Delay final classification briefly and use precedence rules.
- A process disappearing does not prove the active task failed.
- New JSONL records can arrive after an apparent stop event.
- Reading thread titles from SQLite is often enough; message bodies need not enter the notification pipeline.
- Polling file trees every second scales poorly and creates needless disk work. Directory notifications plus cursor-based tailing are calmer and more reliable.
- A durable outbox prevents a transient messenger outage from losing a task result.
- Delivery deduplication needs a stable event key, not just matching message text.
- Account/API switching should preserve hooks and monitor settings because the auth switcher patches only its owned fields.

## Using this with a coding agent

Point an agent at [SKILL.md](SKILL.md). It should inspect the installed Codex version and local event shapes, propose a state model, generate synthetic fixtures, then implement a notifier appropriate to the selected channel. It should not copy private rollout content into prompts or install a messaging service without explicit user approval.

## Scope

The guide focuses on Codex Desktop on Windows and local, one-way notifications. Exact hook events, process names and JSONL schemas are version-sensitive. Re-run discovery and tests after Codex upgrades.

## Security

Messaging credentials, user IDs, private conversation text and local absolute paths must never enter the repository. The monitor should redact errors and send only the minimum useful result. See [SECURITY.md](SECURITY.md).

## Contributing

Bring reproducible signals, race conditions, state fixtures and delivery patterns. Include Codex version context and a validation method. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). Messaging platform terms, quotas and credential handling remain the operator's responsibility.
