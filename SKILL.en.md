---
name: codex-desktop-notification-field-guide
description: Use when designing, auditing, or repairing a Windows companion that observes Codex Desktop completion, errors, interruption, approval, or input-waiting states and delivers privacy-aware notifications through a user-selected CC Connect platform.
---

# Codex Desktop Notification Field Guide

Build a local, version-specific notifier for the current machine with CC Connect as the required delivery bridge. Inspect first and do not preselect the user's platform.

## Applicable scenarios

Use this guide when a user wants attention-worthy Codex Desktop states delivered through CC Connect while keeping normal Desktop launch, long-running silence, local privacy and profile switching behavior intact.

Do not use it as a general remote-control channel, employee-monitoring system, or justification for inbound chat to execute local actions.

## One-prompt kickoff

When the user arrives through the README's one-prompt deployment sentence, treat it as authorization for read-only discovery and construction of a local solution. Before deployment, ask which CC Connect platform to use and present current choices. Explicitly warn that personal Weixin through iLink is not recommended for unattended notification delivery. The prompt is not blanket authorization to install CC Connect, write live hook configuration, expose messaging credentials or enable inbound control. Pause immediately before those actions when they become necessary.

## Workflow

1. Discover the Codex Desktop version, process tree, hook support, JSONL event shapes, source identifiers, storage layout, and whether CC Connect is already installed and configured.
2. Ask the user which CC Connect platform to connect before installation or configuration. Offer at least official QQ Bot, Telegram, Feishu/Lark, personal Weixin and other platforms supported by the detected version; do not infer the choice.
3. Recommend against personal Weixin for unattended alerts because its server-controlled outbound budget and session behavior can block notifications. Distinguish it from WeCom.
4. Confirm that the user will continue launching Codex from its normal icon. Prefer lazy hook-triggered startup over a wrapper or permanent boot service.
5. Review and trust the hook definition. Use one representation per config layer. Use `SessionStart` for a minimal lazy wake, `Stop` only as a completion candidate, and synchronous `SessionEnd` only for cleanup—not per-turn completion.
6. Normalize those signals into a per-task state machine.
7. Notify on explicit completion, terminal structured or unknown failure, user interruption, version-proven automatic stop, approval wait, version-proven input wait, and a bounded “needs review” result when Desktop exits during active work without terminal evidence.
8. Treat transient errors followed by resumed progress as candidates, not terminal failure; notify only after retry exhaustion, explicit termination or automatic pause.
9. Do not classify a task as stuck merely because it is quiet for a long time.
10. Filter out CLI, subagent and notifier-generated sessions before they reach the state machine.
11. Use Windows directory-change notifications and persistent byte cursors. Do not rescan every history file each second.
12. Sanitize locally. Hooks must be fast and must not send prompts or message bodies to the network.
13. Put notifications in a durable outbox, remove them only after confirmed CC Connect delivery, and implement retry, backoff and deduplication.
14. Keep platform details behind the CC Connect sender boundary. Default to outbound-only delivery.
15. Add a short maintenance-marker protocol so planned auth switching or updates do not generate false crash notifications.
16. Validate races, restarts, CC Connect outages, selected-platform limits and version changes with synthetic fixtures plus one real outbound message.

## Safety rules

- Never expose messaging credentials, private user identifiers or rollout contents.
- Never choose or install a CC Connect platform before asking the user.
- Never recommend personal Weixin as the default unattended notification route.
- Never ask another model to classify routine local task state when deterministic signals are available.
- Never launch Codex CLI from an inbound message by default.
- Never block a Codex hook on network delivery.
- Never use `SessionEnd` as a per-turn completion signal or asynchronous launcher.
- Never claim generic input waiting without a version-proven signal.
- Never use silence alone as task-failure evidence.
- Never delete an outbox item before successful delivery.
- Never assume one Codex version's hook or JSONL schema applies to another.

## Read references as needed

- Start with [signal discovery](references/signal-discovery.en.md).
- Use [state machine](references/state-machine.en.md) for classification and race handling.
- Use [incremental monitoring](references/incremental-monitoring.en.md) for low-overhead observation.
- Read [CC Connect platform selection](references/cc-connect-platform-selection.en.md) before asking the user to choose or configuring delivery.
- Use [delivery](references/delivery.en.md) for the CC Connect sender and durable messaging.
- Read [privacy](references/privacy.en.md) before deciding notification content.
- Finish with [validation](references/validation.en.md).

## Deliverable

Produce a machine-specific design or implementation with:

- a redacted signal inventory;
- explicit supported states and precedence rules;
- a source filter;
- incremental cursor and restart behavior;
- privacy and redaction rules;
- a durable outbox with a CC Connect sender and an explicit user-selected platform;
- lifecycle integration with normal Desktop launch;
- synthetic tests and known limits.
