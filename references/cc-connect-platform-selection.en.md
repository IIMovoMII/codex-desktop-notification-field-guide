# CC Connect and platform selection

[中文](cc-connect-platform-selection.md)

Inspect existing CC Connect versions, projects, and lifecycle first. Existing configuration can be reused, but it does not choose the platform, destination, or inbound behavior for the user.

## Ask for choices

Ask once about unresolved choices: destination, dedicated or shared bridge, and notification-only or control of existing Desktop conversations. Do not repeat established choices. Enter credentials through local UI or restricted configuration, not the conversation.

| Platform | Verify |
| --- | --- |
| [QQ Bot Official](https://github.com/chenhg5/cc-connect/blob/main/docs/qqbot.md) | Installed-version support, account eligibility, target session, and actual quota |
| [Telegram](https://github.com/chenhg5/cc-connect/blob/main/docs/telegram.md) | Bot credentials, recipient/group, network access, and inbound permissions |
| [Feishu/Lark](https://github.com/chenhg5/cc-connect/blob/main/docs/feishu.md) | App permissions, destination, and organization restrictions |
| [QQ OneBot](https://github.com/chenhg5/cc-connect/blob/main/docs/qq.md) | Additional OneBot implementation and account/runtime/maintenance cost |
| [Personal Weixin iLink](https://github.com/chenhg5/cc-connect/blob/main/docs/weixin.md) | Proactive-send limits; not recommended for unattended alerts |
| WeCom or other platforms | Consult installed-version documentation instead of inferring capability from the name |

These links track upstream main; match documentation to the installed release. Do not conflate QQ Bot Official with OneBot, or personal Weixin with WeCom.

## Why personal Weixin is not recommended

Merged upstream [PR #1643](https://github.com/chenhg5/cc-connect/pull/1643) reports proactive-send budgets/throttling and that repeated attempts during throttling can worsen it. This is time-specific upstream testing, not a permanent server contract. A local deployment also observed delivery stopping after a batch of unanswered messages.

Do not promise a fixed ten-message limit, a universal daily number, or guaranteed recovery from one reply. If selected, inspect current quota protection, retain pending messages, wait on throttling, and explain why this route is unsuitable for continuously reliable unattended alerts.

Other platforms also have limits. Verify quota by account, destination type, and current responses rather than transferring one platform's behavior to another.

## First installation and binding

| Starting point | Next step | Completion evidence |
| --- | --- | --- |
| No CC Connect | Use an upstream build for the chosen OS/scope; document runtime data and removal | Starts with an identifiable version |
| Existing shared instance | Establish project/destination, config ownership, and inbound behavior; integrate incrementally | Other uses keep working |
| No platform binding | User completes local login/credentials and required verification | A target session exists for an outbound attempt |
| Expired binding/credentials | Pause the destination and rebind without discarding the queue | Verify the same or explicitly changed destination |
| Configured but untested | Send one agreed non-sensitive notice | Visible on the phone and matches the outbox |

Generic bridge success does not establish user receipt. First-use testing verifies destination and visible content. On binding failure, hand off a pending-binding state and recovery action rather than claiming deployment success.

## Reuse and inbound behavior

Shared instances outlive Desktop, and existing project configuration must not be reset wholesale. Even a dedicated project needs an inbound-policy check: CC Connect can bridge to an agent bidirectionally; only using its send interface does not disable the other direction.

Let the user ignore ordinary inbound messages or choose controlled interaction. Do not copy examples with broad administrator access, or silently expand “send me alerts” into launching CLI agents. See [delivery](delivery.en.md) for existing Desktop conversation control.
