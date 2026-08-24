---
name: codex-desktop-notification-field-guide
description: Use when designing, auditing, or repairing a Windows companion that observes Codex Desktop completion, errors, interruption, approval, or input-waiting states and delivers privacy-aware notifications through CC Connect, QQ, or another messaging adapter.
---

# Codex Desktop Notification Field Guide

Build a local, version-specific notifier for the current machine. Do not install an assumed bot stack.

## Workflow

1. Discover the Codex Desktop version, process tree, hook support, JSONL event shapes, source identifiers, storage layout and selected delivery channel.
2. Confirm that the user will continue launching Codex from its normal icon. Prefer lazy hook-triggered startup over a wrapper or permanent boot service.
3. Treat hooks as low-latency hints, JSONL appends as durable evidence, and process liveness as supporting context.
4. Normalize those signals into a per-task state machine.
5. Notify on explicit completion, structured or unknown failure, user interruption, approval wait and input wait.
6. Do not classify a task as stuck merely because it is quiet for a long time.
7. Filter out CLI, subagent and notifier-generated sessions before they reach the state machine.
8. Use Windows directory-change notifications and persistent byte cursors. Do not rescan every history file each second.
9. Sanitize locally. Hooks must be fast and must not send prompts or message bodies to the network.
10. Put notifications in a durable outbox, remove them only after confirmed delivery, and implement retry, backoff and deduplication.
11. Keep channel logic behind an adapter. Default to outbound-only delivery.
12. Add a short maintenance-marker protocol so planned auth switching or updates do not generate false crash notifications.
13. Validate races, restarts, channel failures and version changes with synthetic fixtures.

## Safety rules

- Never expose messaging credentials, private user identifiers or rollout contents.
- Never ask another model to classify routine local task state when deterministic signals are available.
- Never launch Codex CLI from an inbound message by default.
- Never block a Codex hook on network delivery.
- Never use silence alone as task-failure evidence.
- Never delete an outbox item before successful delivery.
- Never assume one Codex version's hook or JSONL schema applies to another.

## Read references as needed

- Start with [signal discovery](references/signal-discovery.md).
- Use [state machine](references/state-machine.md) for classification and race handling.
- Use [incremental monitoring](references/incremental-monitoring.md) for low-overhead observation.
- Use [delivery](references/delivery.md) for channel adapters and durable messaging.
- Read [privacy](references/privacy.md) before deciding notification content.
- Finish with [validation](references/validation.md).

## Deliverable

Produce a machine-specific design or implementation with:

- a redacted signal inventory;
- explicit supported states and precedence rules;
- a source filter;
- incremental cursor and restart behavior;
- privacy and redaction rules;
- a durable, channel-neutral outbox;
- lifecycle integration with normal Desktop launch;
- synthetic tests and known limits.
