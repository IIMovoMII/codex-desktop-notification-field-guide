<div align="center">

# Codex Desktop Notification Field Guide

**Turn Codex Desktop lifecycle signals into reliable, privacy-aware notifications without polling every conversation or asking another model to guess the state.**

[![Field Guide](https://img.shields.io/badge/type-field%20guide-6f42c1)](#what-this-is)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4)](#scope)
[![Architecture](https://img.shields.io/badge/architecture-event--driven-0f766e)](#architecture)
[![Validation](https://github.com/IIMovoMII/codex-desktop-notification-field-guide/actions/workflows/validate.yml/badge.svg)](https://github.com/IIMovoMII/codex-desktop-notification-field-guide/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

[简体中文](README.md) · [Agent entrypoint](SKILL.en.md) · [Companion auth-switching guide](https://github.com/IIMovoMII/codex-auth-switching-field-guide)

</div>

## What this is

This repository is **not a bot package or a preconfigured messaging bridge**. It is a field guide for building a local notification companion around the Codex Desktop version and event formats available on one machine. The delivery bridge is deliberately fixed to [CC Connect](https://github.com/chenhg5/cc-connect); the user must choose the CC Connect platform before deployment.

The design emerged from a practical need: start Codex normally from the Desktop icon, leave a long task running, and receive a message when the task completes, fails, pauses or needs attention. Long silence is allowed. The monitor should not burn CPU scanning all history, expose prompts to a remote service, or launch Codex CLI in response to chat messages.

## Concrete use cases

| Situation | What a machine-specific implementation should achieve |
| --- | --- |
| Long Codex Desktop tasks run while the user is away | Send one useful notification when the task actually completes or needs attention |
| API or relay work frequently encounters service, transport or authentication errors | Preserve structured error categories, fall back to an unknown-error alert and retry delivery safely |
| The user pauses a task midway | Distinguish an explicit interruption from failure or normal completion |
| A task needs approval or more user input | Notify once for each distinct actionable request and stop repeating after the task resumes |
| Codex is always opened from the Desktop or Start-menu icon | Start the monitor lazily from a supported lifecycle hook and stop it with Desktop |
| Official OAuth and API profiles are switched on the same machine | Preserve hooks and monitor state, and suppress false crash alerts during marked maintenance |
| The messaging platform may change later | Keep detection independent from the selected platform while routing every outbound notification through CC Connect |
| A legitimate task is quiet for hours | Continue observing without timer-based “stuck” notifications |

This guide is not a remote-control channel, a general employee-monitoring system, a replacement for Codex's own UI, or permission for inbound chat messages to execute local commands.

## Deploy in one prompt

Copy this sentence into a new Codex task:

~~~text
Codex, follow https://github.com/IIMovoMII/codex-desktop-notification-field-guide to build a machine-specific Windows companion for Codex Desktop. Start with read-only discovery of the installed version, hook sources and trust, JSONL shapes, source filters, process lifecycle, CC Connect version and bindings. Ask me to choose a supported CC Connect platform and explain why personal Weixin is unsuitable for dependable unattended delivery. Keep normal Desktop/Start-menu launch: use a tiny trusted `SessionStart` hook for lazy wake, `Stop` only as a completion candidate, and synchronous `SessionEnd` only for cleanup. Combine version-proven incremental JSONL, hook and process evidence to identify completion, errors, user interruption, approval/input waits, and a bounded “needs review” result after unexplained Desktop exit; never infer stuck from silence. Use durable cursors, a per-turn state machine, maintenance markers, privacy redaction, a deduplicated retrying outbox and visible observer-health failures. Distinguish dedicated from shared CC Connect, remain outbound-only, and never let inbound chat launch Codex CLI. Obtain my approval before installation, binding or live hook writes, then validate races, privacy, recovery and one real notification through my chosen platform.
~~~

This is “deployment” by delegation, not a preconfigured bot installer. If the selected CC Connect platform, account or permission is missing, the agent should ask only for the necessary choice and keep credentials outside the conversation.

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
    O --> A[CC Connect sender]
    A --> Q[User-selected CC Connect platform]
~~~

Hooks wake the system quickly. Windows directory notifications wake the incremental reader when files change. A lightweight periodic reconciliation protects against missed events; it does not scan all conversations or infer failure from elapsed time. The state engine remains platform-neutral internally, but the supported delivery path always ends at CC Connect.

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

## Starting with the normal Desktop icon

The user should keep launching Codex from the Desktop or Start menu. A safe integration can start lazily from a supported Codex lifecycle hook:

1. the hook records a small local event;
2. it checks whether the local monitor is alive;
3. if needed, it starts the monitor; it starts CC Connect only when the notifier owns a dedicated instance;
4. it exits quickly;
5. the monitor later stops after Desktop has exited and pending terminal events have settled; a shared CC Connect instance remains running.

This avoids a startup wrapper and usually avoids a permanent boot-time service. Review and trust the definition, and use either `hooks.json` or inline `[hooks]` in one layer. `SessionEnd` always runs synchronously and is not a per-turn completion signal. If no trusted startup hook exists, explicitly offer a user-approved login-time observer or manual start and mark icon-based lazy startup unsupported.

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
send(notification) -> accepted delivery identifier
healthcheck() -> channel status
classify_failure(error) -> retryable or permanent
~~~

Platform quotas, reply gates and account policies belong in the CC Connect delivery boundary, not the Codex state machine. Configure one chosen platform and prove one real outbound notification before adding another.

Outbound-only is the safer default. Receiving a chat message should not launch Codex CLI or execute commands unless the user designs and secures a separate control plane.

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
- Delivery deduplication needs a stable event key, not just matching message text.
- Account/API switching should preserve hooks and monitor settings because the auth switcher patches only its owned fields.

## Using this with a coding agent

Point an agent at [SKILL.md](SKILL.en.md). It should inspect the installed Codex version, local event shapes and CC Connect state, then ask the user to choose a CC Connect platform before implementation. It should explain the personal-Weixin warning, propose a state model, generate synthetic fixtures and implement the notifier only after the platform choice. It should not copy private rollout content into prompts or install CC Connect without explicit user approval.

## Scope

The guide focuses on Codex Desktop on Windows and local, one-way notifications. Exact hook events, process names and JSONL schemas are version-sensitive. Re-run discovery and tests after Codex upgrades.

## Security

Messaging credentials, user IDs, private conversation text and local absolute paths must never enter the repository. The monitor should redact errors and send only the minimum useful result. See [SECURITY.md](SECURITY.en.md).

## Contributing

Bring reproducible signals, race conditions, state fixtures and delivery patterns. Include Codex version context and a validation method. See [CONTRIBUTING.md](CONTRIBUTING.en.md).

## License

[MIT](LICENSE). Messaging platform terms, quotas and credential handling remain the operator's responsibility.
