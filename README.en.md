<div align="center">

# Codex Desktop Notification Field Guide

**Let Codex work on your computer. Let updates reach your phone.**

[![Type](https://img.shields.io/badge/type-agent_field_guide-6f42c1)](#what-this-is)
[![Bridge](https://img.shields.io/badge/bridge-CC_Connect-0078D4)](https://github.com/chenhg5/cc-connect)
[![License](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

[中文](README.md) · [Agent instructions](SKILL.en.md) · [Auth switching guide](https://github.com/IIMovoMII/codex-auth-switching-field-guide)

</div>

## What this is

You leave a long task running in Codex Desktop and step away. Could QQ, Telegram, or Feishu tell you when it finishes, stops with an error, or needs your attention?

This repository collects practical lessons for building that notifier. It is a **product brief for coding agents, not ready-to-install software**. Give Codex the link, let it inspect your computer, and have it build and verify a solution for your needs.

Delivery goes through [CC Connect](https://github.com/chenhg5/cc-connect). You choose the language, script or app interface, and feature set.

## What you can build

| Your need | Possible feature |
| --- | --- |
| Know when a task ends while away | Completion, terminal-error, and user-interruption alerts |
| Avoid leaving a task waiting for you | Approval and input-request alerts, where the installed version exposes reliable evidence |
| Keep opening Codex however you normally do | Automatic following without a special launch command |
| Cope with a network or messenger outage | A local outbox with an agreed catch-up policy |
| Switch between official accounts and relay APIs | Independent notifier settings and suppression of planned-restart alerts |
| Continue a particular conversation from your phone | Optional remote control with explicit conversation targeting and permitted actions |

**Local decisions without another model call.** State detection and message preparation can run locally without extra model tokens. Messenger delivery still needs a network connection. Remotely continuing a Codex task uses that task's model allowance as usual.

**Suitable for long-lived runs.** Active turns retain bounded evidence, and terminal turns release full replies so monitor memory does not grow with every historical task.

**Suitable for long tasks.** Hours of silence should not be mistaken for a stuck task.

## Deploy in one prompt

Copy this into Codex:

~~~text
Read SKILL.en.md at https://github.com/IIMovoMII/codex-desktop-notification-field-guide and build and verify Codex Desktop notifications for my environment and needs.
~~~

The agent should inspect the environment first and ask only for choices you need to make: destination, notification states, reply excerpts, and remote control. It should discover the OS, versions, and existing configuration itself where possible.

“Deploy” means asking an agent to implement the solution locally. This repository contains no installer.

## Choose a messenger

QQ Bot Official, Telegram, Feishu/Lark, and other platforms can be selected according to the installed CC Connect version. Reuse an existing bridge or configure a dedicated one. Proving one platform first makes verification simpler.

**Personal Weixin is not recommended for unattended alerts.** Upstream reports describe proactive-send budgets and throttling whose behavior varies by account, version, and server changes. One observed message count is not a universal limit. Evaluate personal Weixin and WeCom separately. See [platform selection](references/cc-connect-platform-selection.en.md).

## Agree on two behaviors

- **When to start:** starting on the first task event usually needs less background presence. Being ready as soon as Codex opens requires native process observation. Either choice can preserve normal launch habits.
- **What happens after exit:** stopping with Codex defers unsent messages until the next run. Alternatively, let only the sender continue for a bounded period. An offline computer, shutdown, or platform rejection prevents any promise of immediate delivery.

Messages can contain only a state and task name, or a short excerpt if you choose. Controlling an **existing Desktop conversation** is a separate extension: target selection and continuation must be verified. Simply enabling CC Connect chat does not establish that capability.

## Lessons kept in this guide

The [agent instructions](SKILL.en.md) cover four recurring problems: missed startup, incorrect state classification, duplicate alerts, and queues that flush only after the next launch. Implementation details and tests live there; this page explains what you can build.

Most field evidence comes from Windows. Other systems can reuse the ideas with native equivalents and fresh validation. Retest after Codex or CC Connect updates; this is not a claim of compatibility with every version or platform.

A recent real incident is included as a lesson: Windows can reuse a stopped service's old PID for an unrelated process, and an old log line can make a dead bridge look ready. A reliable implementation should verify the executable identity and process creation time, then re-check interface readiness whenever it wakes; a PID or a historical “started” line is not proof of a live service.

## Contributing

Bring versioned, reproducible lessons while preserving implementation freedom. Do not upload real conversations, configuration, or bot credentials. See [contributing](CONTRIBUTING.en.md) and [security](SECURITY.en.md).

[MIT license](LICENSE).
