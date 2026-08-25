<div align="center">

# Codex Desktop Notification Field Guide

**A field-tested product brief for agents turning Codex Desktop task state into reliable CC Connect notifications.**

[![Field Guide](https://img.shields.io/badge/type-field%20guide-6f42c1)](#what-this-is)
[![Adaptation](https://img.shields.io/badge/adaptation-machine--specific-0078D4)](#scope)
[![Architecture](https://img.shields.io/badge/architecture-event--driven-0f766e)](#architecture)
[![Validation](https://github.com/IIMovoMII/codex-desktop-notification-field-guide/actions/workflows/validate.yml/badge.svg)](https://github.com/IIMovoMII/codex-desktop-notification-field-guide/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

[简体中文](README.md) · [Agent entrypoint](SKILL.en.md) · [Companion auth-switching guide](https://github.com/IIMovoMII/codex-auth-switching-field-guide)

</div>

## What this is

This repository is **not a bot package or a preconfigured messaging bridge**. It is a product brief and field guide, written primarily for coding agents building around the Codex Desktop version, event formats, and user requirements on one machine. The delivery bridge is deliberately fixed to [CC Connect](https://github.com/chenhg5/cc-connect); the user chooses the platform and whether inbound interaction is in scope.

> The repository describes outcomes, state lessons, and acceptance criteria—not one mandatory codebase. Adapt observation, UI, message content, and optional features to the local system. Windows mechanisms are validated examples, not the only cross-platform design.

The design emerged from a practical need: start Codex through any normal entry point, leave a long task running, and receive a message when it completes, fails, pauses, or needs attention. The companion must not depend on a special shortcut or wrapper. Long silence is allowed, and the monitor should not burn CPU scanning all history or expose prompts to a remote service.

## Concrete use cases

| Situation | What a machine-specific implementation should achieve |
| --- | --- |
| Long Codex Desktop tasks run while the user is away | Send one useful notification when the task actually completes or needs attention |
| API or relay work frequently encounters service, transport or authentication errors | Preserve structured error categories, fall back to an unknown-error alert and retry delivery safely |
| The user pauses a task midway | Distinguish an explicit interruption from failure or normal completion |
| Codex stops itself, exhausts retries, or pauses automatically | Notify a proven system stop separately; use “needs review” when the actor is uncertain |
| A task needs approval or more user input | Notify once for each distinct actionable request and stop repeating after the task resumes |
| Codex may be opened from a shortcut, command, file association, restore flow, or another normal entry | Use entry-point-independent lifecycle hooks or native process events so the observer follows Desktop startup and shutdown |
| Official OAuth and API profiles are switched on the same machine | Preserve hooks and monitor state, and suppress false crash alerts during marked maintenance |
| The messaging platform may change later | Keep detection independent from the selected platform while routing every outbound notification through CC Connect |
| A legitimate task is quiet for hours | Continue observing without timer-based “stuck” notifications |

This guide is not a remote-control channel, a general employee-monitoring system, a replacement for Codex's own UI, or permission for inbound chat messages to execute local commands.

## Deploy in one prompt

Copy this sentence into a new Codex task:

~~~text
Codex, read https://github.com/IIMovoMII/codex-desktop-notification-field-guide in full, starting with `SKILL.en.md`, then build and validate a CC Connect-backed Codex Desktop notifier for my machine and requirements.
~~~

This is “deployment” by delegation, not a preconfigured bot installer. If the selected CC Connect platform, account or permission is missing, the agent should ask only for the necessary choice and keep credentials outside the conversation.

## Align requirements before implementation

Do not ask for facts the agent can inspect, such as the operating system, Codex build, paths, local event shape, or CC Connect status. Ask only for choices that change the product: which states matter, how much content may be sent, the messaging platform, dedicated versus shared CC Connect, immediate app-start versus first-task startup, and whether secure inbound interaction is wanted.

The user may keep only completion and error alerts, or add approval/input waits, a status UI, multiple platforms, or remote control. Omit unwanted modules. Evidence quality, privacy, durable deduplication, and recovery still need to close the loop for every selected feature.

## Why one signal is not enough

Hooks are fast, but their event coverage and timing can vary. Matching command hooks for one event run concurrently, so a `Stop` observed by the notifier can still be followed by another `Stop` hook requesting continuation. `Stop` is therefore a settling candidate, never completion proof by itself. JSONL contains richer evidence, but reading every file repeatedly is wasteful. Process exit is useful, but it cannot explain why a task stopped. Reliable classification comes from combining small, independent signals.

## Architecture

~~~mermaid
flowchart LR
    H[Codex hooks] --> N[Local normalizer]
    J[Incremental JSONL tail] --> N
    P[Desktop process state] --> N
    N --> S[Per-task state machine]
    S --> D[Deduplication and privacy filter]
    D --> O[Durable outbox]
    O --> A[CC Connect sender]
    A --> Q[User-selected CC Connect platform]
~~~

Hooks wake the system quickly. Native filesystem events wake the incremental reader when files change; Windows directory notifications are one proven implementation. A lightweight periodic reconciliation protects against missed events; it does not scan all conversations or infer failure from elapsed time. The state engine remains platform-neutral internally, but the supported delivery path always ends at CC Connect.

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

1. **Observe Desktop directly.** Do not require a wrapper or bind the design to one icon or entry point.
2. **Use hooks as hints, not absolute truth.** Normalize them and corroborate terminal decisions when needed.
3. **Tail only appended bytes.** Persist per-file cursors and use native filesystem events for wakeups.
4. **Filter the source early.** Ignore CLI tasks, subagents and monitor-generated activity to prevent loops.
5. **Model transitions per task.** Completion, failure, pause and waiting are states, not keywords.
6. **Prefer structured errors.** Text matching is a fallback for version gaps; unknown failures still deserve a notification.
7. **Keep prompts local.** A hook should write the minimum sanitized event and return immediately.
8. **Queue before sending.** Remove a notification only after the channel confirms success.
9. **Fix the bridge, choose the platform.** Delivery always uses CC Connect, while state detection remains independent from the selected CC Connect platform.
10. **Coordinate planned maintenance.** An auth switcher or updater can write a short-lived marker so a planned restart is not reported as a crash.

## Guide map

| Read this | When you need to |
| --- | --- |
| [Signal discovery](references/signal-discovery.en.md) | Inspect hooks, JSONL, processes and source identifiers |
| [State machine](references/state-machine.en.md) | Combine signals without timer-based false alarms |
| [Incremental monitoring](references/incremental-monitoring.en.md) | Build low-overhead Windows watching and durable cursors |
| [CC Connect platform selection](references/cc-connect-platform-selection.en.md) | Ask the user which platform to connect and explain why personal Weixin is not recommended |
| [Delivery](references/delivery.en.md) | Design the outbox, retries, CC Connect sender and one-way channel boundary |
| [Privacy](references/privacy.en.md) | Minimize and redact local and remote data |
| [Validation](references/validation.en.md) | Test state races, failures, restarts and channel outages |

## Follow Codex from any launch method

The user may open Codex from a shortcut, command, file association, restore flow, or another normal entry. The integration must not depend on one shortcut. Prefer a reviewed, trusted global lifecycle hook for lazy startup:

1. the hook records a small local event;
2. it checks whether the local monitor is alive;
3. if needed, it starts the monitor; it starts CC Connect only when the notifier owns a dedicated instance;
4. it exits quickly;
5. the monitor later stops after Desktop has exited and pending terminal events have settled; a shared CC Connect instance remains running.

This is independent of where the app was launched, but it normally starts at the first supported lifecycle event. If the user needs startup at process creation, use native process events, a service manager, or a lightweight login observer that blocks efficiently instead of scanning every second. Review and trust hook definitions, and use either `hooks.json` or inline `[hooks]` in one layer. `SessionEnd` always runs synchronously and is not a per-turn completion signal.

## CC Connect platform choice

CC Connect is required for this guide. Before installing or configuring it, ask the user which platform they want. Do not silently choose the platform from what happens to be installed.

| Choice | Practical guidance |
| --- | --- |
| QQ Bot Official | Preferred for users who want QQ and can complete QQ developer verification; upstream uses the official API and requires no public IP |
| Telegram | Good when Telegram is reachable; upstream uses long polling and requires no public IP |
| Feishu/Lark | Good for stable personal or team workflows; upstream uses a WebSocket connection and requires no public IP |
| QQ via OneBot | Possible, but requires a third-party OneBot implementation and has a different risk profile from official QQ Bot |
| Personal Weixin via iLink | **Not recommended for unattended notification delivery** |
| WeCom or another supported platform | Offer when it matches the user's actual account and installed CC Connect version |

**Why personal Weixin is not recommended:** one source environment observed a limit after roughly ten accumulated unanswered notifications, but that is version- and account-specific, not a platform rule. [Issue #770](https://github.com/chenhg5/cc-connect/issues/770) concerns `ret=-2` during long or chunked output and does not prove a ten-message cap. [Issue #1087](https://github.com/chenhg5/cc-connect/issues/1087) contains an earlier context-token diagnosis. The later merged [PR #1643](https://github.com/chenhg5/cc-connect/pull/1643) reports empirical account-level outbound throttling at roughly five to six separate messages per 24 hours, introduces a default safe budget of four, and warns that retries during the penalty can extend it. Exact behavior can change, but this route is still a poor fit for reliable unattended delivery.

Personal Weixin and WeCom are different CC Connect platforms. The warning above targets personal Weixin through iLink; evaluate WeCom separately.

After the user chooses, keep a narrow local sender contract:

~~~text
send(notification) -> accepted; preserve an identifier when available
healthcheck() -> channel status
classify_failure(error) -> retryable or permanent
~~~

Platform quotas, reply gates and account policies belong in the CC Connect delivery boundary, not the Codex state machine. Configure one chosen platform and prove one real outbound notification before adding another.

Ask the user to choose notification-only or inbound-enabled behavior. Notification-only can ignore ordinary messages, as a local installation may already do. If inbound control is requested, make it a separate boundary with explicit senders, allowed actions, confirmations, replay protection, audit, and rate limits; never turn arbitrary text directly into a local command.

## Hard-won lessons

- `SessionEnd` always runs synchronously and is not a per-turn completion hook; keep it tiny and use it only for cleanup.
- Hook definitions require review/trust, and changed definitions may require review again.
- Completion and interruption events can race. Delay final classification briefly and use precedence rules.
- A process disappearing does not prove the active task failed.
- New JSONL records can arrive after an apparent stop event.
- Reading thread titles from SQLite is often enough; message bodies need not enter the notification pipeline.
- Polling file trees every second scales poorly and creates needless disk work. Directory notifications plus cursor-based tailing are calmer and more reliable.
- A durable outbox prevents a transient messenger outage from losing a task result.
- A bridge can support many platforms while one platform is still a poor fit; personal Weixin's outbound limits make it unsuitable as the default notification route.
- A `Stop` can race another concurrent `Stop` hook's continuation decision; wait for independent terminal evidence instead of declaring success after a fixed delay.
- Delivery deduplication needs a stable event key that survives restarts and does not change with title or summary rendering. Retire superseded turns silently so one Desktop exit cannot fan out into many error alerts.
- Account/API switching should preserve hooks and monitor settings because the auth switcher patches only its owned fields.

## Using this with a coding agent

Point an agent at [SKILL.en.md](SKILL.en.md). It should inspect the system, installed Codex build, local event shapes, and CC Connect state, then ask one focused set of questions about states, content, startup timing, platform, instance ownership, and inbound needs. It should explain the personal-Weixin warning, propose only the requested modules, generate synthetic fixtures, and obtain approval before installation or live hook writes.

## Scope

The guide targets local Codex Desktop notifications and can be adapted across operating systems and one-way or two-way scenarios. Its field evidence is primarily Windows-based; other platforms should replace file events, process observation, credential storage, and lifecycle integration with native equivalents. Exact hook events, process names, and JSONL schemas remain version-sensitive.

## Security

Messaging credentials, user IDs, private conversation text and local absolute paths must never enter the repository. The monitor should redact errors and send only the minimum useful result. See [SECURITY.en.md](SECURITY.en.md).

## Contributing

Bring reproducible signals, race conditions, state fixtures and delivery patterns. Include Codex version context and a validation method. See [CONTRIBUTING.en.md](CONTRIBUTING.en.md).

## License

[MIT](LICENSE). Messaging platform terms, quotas and credential handling remain the operator's responsibility.
