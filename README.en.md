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

> This guide provides product goals, state lessons, and acceptance criteria rather than one mandatory codebase. Windows is the validated example; other systems can use native equivalents.

The design emerged from a practical need: start Codex through any normal entry point, leave a long task running, and receive a message when it completes, fails, pauses, or needs attention. The companion must not depend on a special shortcut or wrapper.

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

The core product is a local task notifier. If chat-based control is also wanted, inbound permissions, confirmation, and auditing can be added as a separate optional feature.

## Deploy in one prompt

Copy this sentence into a new Codex task:

~~~text
Codex, read https://github.com/IIMovoMII/codex-desktop-notification-field-guide in full, starting with `SKILL.en.md`, then build and validate a CC Connect-backed Codex Desktop notifier for my machine and requirements.
~~~

This is “deployment” by delegation, not a preconfigured bot installer. If the selected CC Connect platform, account or permission is missing, the agent should ask only for the necessary choice and keep credentials outside the conversation.

## Choose the scope you need

The smallest useful version can send only completion and error alerts. Add approval/input waits, a status UI, multiple platforms, or secure inbound interaction only when needed. Describe the states you care about, how much content a message may contain, the platform, whether to reuse an existing CC Connect instance, and whether startup should follow the app immediately or wait for the first task; the machine can provide its own OS, paths, event formats, and installed state.

Every version should still use evidence-based states, minimize disclosed content, merge duplicate alerts, and preserve results through temporary delivery failures.

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
| System stop/automatic pause | explicit non-user stop evidence | Yes; use “needs review” when the cause is uncertain |
| Waiting for approval | explicit approval request | Yes |
| Waiting for input | explicit input request or version-proven equivalent | Yes |
| Desktop exits with an active task but no result | no maintenance marker and no terminal evidence after settling | Yes, as “needs review,” not as failure |
| Long-running silence | no terminal evidence | No |
| Planned restart | maintenance marker from a cooperating tool | No crash alert |
| Observer health failure | untrusted hook, incompatible parser, outbox or bridge failure | Show locally; send a health alert when delivery remains available |

Do not create a “probably stuck” notification from a timer alone. Codex tasks can legitimately run for hours. A timeout may be useful for monitoring the notifier itself, but not for judging the task.

## Core design rules

1. **Observe Desktop directly.** Do not require a wrapper or bind the design to one icon or entry point.
2. **Use hooks as hints, not absolute truth.** Normalize them and corroborate terminal decisions when needed.
3. **Tail only appended bytes.** Persist per-file cursors and use native filesystem events for wakeups.
4. **Filter the source early.** Ignore CLI tasks, subagents and monitor-generated activity to prevent loops.
5. **Model transitions per task.** Completion, failure, pause and waiting are states, not keywords.
6. **Prefer structured errors.** Text matching is a fallback for version gaps; unknown failures still deserve a notification.
7. **Send only what is needed by default.** Keep full prompts and conversations local; include a redacted, length-limited reply excerpt only when the user explicitly opts in.
8. **Queue before sending.** Remove a notification only after the channel confirms success.
9. **Fix the bridge, choose the platform.** Delivery always uses CC Connect, while state detection remains independent from the selected CC Connect platform.
10. **Coordinate planned maintenance.** An auth switcher or updater can write a short-lived marker so a planned restart is not reported as a crash.

## Guide map

| Read this | When you need to |
| --- | --- |
| [Signal discovery](references/signal-discovery.en.md) | Inspect hooks, JSONL, processes and source identifiers |
| [State machine](references/state-machine.en.md) | Combine signals without timer-based false alarms |
| [Incremental monitoring](references/incremental-monitoring.en.md) | Watch file changes with low overhead and durable cursors |
| [CC Connect platform selection](references/cc-connect-platform-selection.en.md) | Ask the user which platform to connect and explain why personal Weixin is not recommended |
| [Delivery](references/delivery.en.md) | Design the outbox, retries, CC Connect sender and optional inbound boundary |
| [Privacy](references/privacy.en.md) | Minimize and redact local and remote data |
| [Validation](references/validation.en.md) | Test state races, failures, restarts and channel outages |

## Follow Codex from any launch method

Whether Codex is opened from a shortcut, command, file association, or restore flow, no special launcher or wrapper is required. The default design can start lazily on the first Codex lifecycle event and stop after Desktop exits, terminal events settle, and queued messages are handled.

If the notifier must already be ready when the Codex window appears, choose process-level lifecycle integration instead. The two choices trade startup timing against background presence; see [incremental monitoring](references/incremental-monitoring.en.md) for implementation options.

## CC Connect platform choice

CC Connect is required for this guide. You explicitly choose the platform during setup; an old configuration already present on the machine does not make that choice for you.

| Choice | Practical guidance |
| --- | --- |
| QQ Bot Official | Preferred for users who want QQ and can complete QQ developer verification; upstream uses the official API and requires no public IP |
| Telegram | Good when Telegram is reachable; upstream uses long polling and requires no public IP |
| Feishu/Lark | Good for stable personal or team workflows; upstream uses a WebSocket connection and requires no public IP |
| QQ via OneBot | Possible, but requires a third-party OneBot implementation and has a different risk profile from official QQ Bot |
| Personal Weixin via iLink | **Not recommended for unattended notification delivery** |
| WeCom or another supported platform | Offer when it matches the user's actual account and installed CC Connect version |

**Why personal Weixin is not recommended:** CC Connect has documented account-level proactive-send limits and throttling whose exact behavior varies by account, version, and service-side changes. Unattended alerts need predictable delivery, so QQ Bot Official, Telegram, or Feishu is a better default. See the [platform-selection notes](references/cc-connect-platform-selection.en.md) for evidence and version details.

Personal Weixin and WeCom are different CC Connect platforms. The warning above targets personal Weixin through iLink; evaluate WeCom separately.

Configure one chosen platform and prove one real outbound notification before adding another.

You can choose notification-only or inbound-enabled behavior. Notification-only can ignore ordinary messages. If inbound control is enabled, keep it behind a separate boundary with explicit senders, allowed actions, confirmations, replay protection, audit, and rate limits; never turn arbitrary text directly into a local command.

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

## Scope

The guide targets local Codex Desktop notifications and can be adapted across operating systems and one-way or two-way scenarios. Its field evidence is primarily Windows-based; other platforms should replace file events, process observation, credential storage, and lifecycle integration with native equivalents. Exact hook events, process names, and JSONL schemas remain version-sensitive.

## Security

Messaging credentials, user IDs, private conversation text and local absolute paths must never enter the repository. The monitor should redact errors and send only the minimum useful result. See [SECURITY.en.md](SECURITY.en.md).

## Contributing

Bring reproducible signals, race conditions, state fixtures and delivery patterns. Include Codex version context and a validation method. See [CONTRIBUTING.en.md](CONTRIBUTING.en.md).

## License

[MIT](LICENSE). Messaging platform terms, quotas and credential handling remain the operator's responsibility.
