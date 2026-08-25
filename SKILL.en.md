---
name: codex-desktop-notification-field-guide
description: Use when designing, auditing, or repairing a machine-specific Codex Desktop companion that combines lifecycle, incremental event, and process evidence to deliver user-selected task notifications through CC Connect.
---

# Codex Desktop Notification Field Guide

Build a local, version-specific notifier for the current machine with CC Connect as the required delivery bridge. The user chooses the platform, notification scope, and inbound behavior.

## Applicable scenarios

Use this guide when a user wants attention-worthy Codex Desktop states delivered through CC Connect while keeping any normal Desktop launch path, long-running silence, local privacy, and profile switching behavior intact.

Do not expand the notifier into employee monitoring or remote control unless the user explicitly selects and scopes that feature.

## Product-brief status and implementation freedom

This repository is a product brief and experience pack for agents, not a ready-to-install application or a mandatory architecture. Inspect the current operating system, Codex build, and existing components, then choose suitable hooks, filesystem events, process observers, tray UI, service manager, or other mechanisms. Add, remove, or replace states, interfaces, platforms, and inbound features to match the user's request.

Windows paths and mechanisms are validated examples. Use native equivalents elsewhere. Do not ask for facts that can be inspected safely; ask only for choices that cannot be inferred and materially change the product.

## One-prompt kickoff

When the user arrives through the README's one-prompt sentence, treat it as authorization for read-only discovery and construction of a local solution. It is not blanket authorization to install CC Connect, bind an account, write live hook configuration, expose credentials, or enable inbound control. Explain impact and obtain confirmation immediately before those actions.

## Workflow

1. Discover the operating system, Codex Desktop build, process tree, hook support, structured append-event shapes, source identifiers, storage layout, and existing CC Connect state without exposing secrets or conversation text.
2. Ask one focused set of questions about the unknown choices: states to notify, allowed content, messaging platform, dedicated or shared CC Connect, immediate process-start versus first-task startup, and whether inbound interaction is wanted. Do not repeat discoverable environment questions.
3. Present only platforms supported by the detected CC Connect build. Recommend against personal Weixin for unattended alerts and distinguish it from WeCom.
4. Agree on the smallest useful feature set; the remaining modules are composable, not mandatory for every implementation.
5. Decouple lifecycle from the launch entry point. Prefer trusted global lifecycle hooks for lazy startup; use native process events or an equivalent mechanism when the user requires startup as soon as the app process appears. Do not require a wrapper command.
6. Review and trust hook definitions and use one representation per config layer. Matching command hooks for one event run concurrently: another `Stop` hook may still request continuation. Treat `Stop` only as a settling candidate, never completion proof by itself; `stop_hook_active` does not prove all peers finished. Use synchronous `SessionEnd` only for cleanup.
7. Normalize version-proven structured events and process context into a per-task state machine. Filter CLI, subagent, notifier-generated, and out-of-scope ChatGPT sessions first.
8. Implement only the states the user selected, but give each one evidence, precedence, recovery, deduplication, and acceptance criteria.
9. Treat transient errors followed by progress as candidates. Emit a terminal failure, automatic stop, or interruption only after independent terminal evidence.
10. Any activity after `Stop` cancels its settling candidate. Completion requires an independent terminal record; if observation ends without one, report “needs review” instead of using a timer to guess success.
11. Keep only the current unfinished turn per session and retire superseded turns silently. Use a restart-stable event key that does not change with title or message rendering, so one incident cannot fan out into repeated alerts.
12. Do not classify a task as stuck merely because it is quiet for a long time.
13. Use native filesystem events and persistent byte cursors. Handle partial records, replacement, truncation, overflow, and restart without rescanning every history file each second.
14. Sanitize locally. Hooks stay fast and do not perform network delivery.
15. Put notifications in a durable outbox and mark them sent only after CC Connect returns success. Retry transient failures with backoff and make permanent failures visible locally.
16. Keep dedicated and shared CC Connect lifecycle separate; never stop a shared instance merely because Desktop exits.
17. Let the user choose notification-only or inbound-enabled behavior. If inbound is enabled, isolate allowed senders, actions, confirmation, replay protection, audit, and rate limits from the notifier path.
18. Add a short maintenance-marker protocol so planned auth switching or updates do not generate false crash notifications.
19. Validate concurrency orders, restarts, changed render text, launch methods, CC Connect outages, selected-platform limits, privacy, and version changes with synthetic fixtures plus one real outbound message.

## Safety rules

- Never expose messaging credentials, private user identifiers or rollout contents.
- Never choose or install a CC Connect platform before asking the user.
- Never recommend personal Weixin as the default unattended notification route.
- Never ask another model to classify routine local task state when deterministic signals are available.
- Never map inbound chat directly to local commands without explicit user scope and a separate control boundary.
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

Produce a machine-specific design or implementation covering the user's selected scope, with at least:

- a redacted signal inventory;
- explicit supported states and precedence rules;
- a source filter;
- incremental cursor and restart behavior;
- privacy and redaction rules;
- a durable outbox with a CC Connect sender and an explicit user-selected platform;
- entry-point-independent lifecycle integration;
- synthetic tests and known limits.

Waiting states, inbound control, multiple platforms, and graphical UI may be omitted when the user did not select them; if included, close their full evidence, security, and recovery loops.
