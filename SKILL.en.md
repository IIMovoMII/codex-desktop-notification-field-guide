---
name: codex-desktop-notification-field-guide
description: Build, review, or repair machine-specific Codex Desktop notifications through CC Connect, focusing on automatic lifecycle, state evidence, deduplication, and outbox recovery.
---

# Implementation notes for agents

[中文](SKILL.md)

## Purpose and scope

This is a field guide, not an executable installer or a specification to copy in full. Choose the implementation around the user's goals, installed versions, and local evidence. Language, UI, native mechanisms, and features are adaptable. This guide uses CC Connect as the messaging bridge; the user chooses the platform.

Local deterministic rules usually suffice for classification and delivery without starting Codex CLI or calling another model. Remote control of an existing Desktop conversation is an optional extension, distinct from CLI sessions managed by CC Connect.

## Inspect facts, then ask for choices

Start with [signal discovery](references/signal-discovery.en.md). Inspect the OS, versions, command interpreter, hooks, storage, and existing CC Connect. Do not ask for safely discoverable facts or expose credentials and conversations during inspection.

Ask only about unresolved choices that change the result:

- messaging platform and destination, and whether to reuse CC Connect;
- states to notify and whether to include an excerpt;
- startup on the first task event or as soon as Desktop appears;
- immediate exit with Desktop or bounded sender-only finishing; expiry or coalescing of old alerts;
- notifications only, or limited inbound actions on selected Desktop conversations.

Carry forward explicit choices and authorization without repeatedly asking permission for each step. Do not invent a missing platform, recipient, or remote-control scope. Enter credentials locally. Establish scope before installation, binding, or live hook changes, and preserve other programs' configuration.

## Implementation order

1. **Prove one signal chain.** Use non-sensitive completion/interruption cases to establish task and turn identities, terminal evidence, and source in this build. Mark unsupported states honestly instead of guessing from silence or prose.
2. **Handle startup and exit.** Use [incremental monitoring and lifecycle](references/incremental-monitoring.en.md) for first events, startup races, single-instance ownership, readiness, exit, and catch-up. Normal use should not require a wrapper launcher.
3. **Implement selected states.** Follow the [state machine](references/state-machine.en.md) for Stop continuation, transient errors, wait resolution, late terminal records, and duplicates. Timers must not turn quiet tasks into failures.
4. **Connect delivery.** Use [platform selection](references/cc-connect-platform-selection.en.md) and [delivery](references/delivery.en.md) for fixed destinations, a durable outbox, and explainable retries. Notifications use a verified outbound path without another agent rewriting the content.
5. **Respect local boundaries.** Use [privacy](references/privacy.en.md) to scope messages and logs. Profile switching should preserve hooks and independent runtime data; the notifier does not manage Codex authentication or rewrite history.
6. **Validate in stages.** Run relevant cases from [validation and troubleshooting](references/validation.en.md). Distinguish files installed, commands executed, Desktop loading the hooks, and messages received on the phone. One stage cannot prove the next.

## Common implementation traps

- `Stop` is only a settling candidate. Another concurrent hook may continue the turn; `stop_hook_active` does not prove completion. New activity cancels the candidate; independent terminal evidence confirms the outcome.
- One 503, tool error, or timeout does not prove turn failure. Separate Codex's retries, final termination, and notification-delivery failures.
- Byte cursors, task state, and notification decisions need recoverable commit ordering. Saving only the read position can lose a notification that was not yet queued.
- Deduplicate using stable task/turn identities. Terminal labels, titles, excerpts, and error wording do not identify a new event.
- Persistence means local retention. A stopped sender cannot retry. Define exit behavior before claiming catch-up.
- On Windows, test with Codex's actual shell. A cmd test does not establish PowerShell compatibility. Verify absolute paths, quoting, UTF-8, and detached-child survival.
- Installed hooks, trusted hooks, live processes, ready interfaces, and phone-visible delivery are different states. Keep queryable local diagnostics for failures.

## Handoff

Deliver the chosen local implementation, short usage notes, and repeatable diagnosis, disable, update, and uninstall procedures. Record versions, supported states, real tests passed, and checks still requiring a restart or user observation.

This pack's document validator does not validate your program. Without actual delivery evidence, report “pending acceptance.” Unselected platforms, remote control, and GUI features need not be implemented. Treat platform and version differences as local evidence, not permanent universal rules.
