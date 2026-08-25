# CC Connect platform selection

[CC Connect](https://github.com/chenhg5/cc-connect) is the required delivery bridge for this guide. The user still owns the platform choice. Ask before installing, binding or changing any channel.

## Required user choices

After read-only discovery, ask only for choices the machine cannot answer:

> Which CC Connect platform should receive Codex Desktop notifications: official QQ Bot, Telegram, Feishu/Lark, personal Weixin, WeCom, or another platform supported by the installed version?

Also ask whether to use a dedicated or existing CC Connect project, and whether the user wants notification-only operation or a separately secured inbound-control module.

Show only platforms that are actually supported by the detected CC Connect release. Explain the practical differences and wait for a selection. Do not infer the answer from stale config, an old binding or the user's operating system.

## Recommended order

| Platform | Connection and setup | Guidance |
| --- | --- | --- |
| [QQ Bot Official](https://github.com/chenhg5/cc-connect/blob/main/docs/qqbot.md) | Official API v2 over WebSocket; no public IP; developer verification required | Preferred QQ route when the user can register an official bot |
| [Telegram](https://github.com/chenhg5/cc-connect/blob/main/docs/telegram.md) | Bot API long polling; no public IP; requires Telegram network access | Good general-purpose choice |
| [Feishu/Lark](https://github.com/chenhg5/cc-connect/blob/main/docs/feishu.md) | WebSocket; no public IP; app setup and permissions required | Good stable choice for personal or team workflows |
| [QQ OneBot](https://github.com/chenhg5/cc-connect/blob/main/docs/qq.md) | Requires NapCat or another OneBot implementation | Offer only after explaining the extra component and non-official risk |
| [Personal Weixin](https://github.com/chenhg5/cc-connect/blob/main/docs/weixin.md) | Personal WeChat through iLink HTTP long polling and QR login | Do not recommend for unattended notifications |
| WeCom or another built-in platform | Depends on the installed release | Evaluate its official setup guide and the user's account situation |

The upstream repository supports more platforms than this shortlist. The shortlist is a decision aid, not a frozen capability list.

## Personal Weixin warning

Personal Weixin through iLink has server-controlled outbound and session constraints that conflict with reliable unattended notification delivery:

- One source environment observed delivery stop after roughly ten accumulated unanswered notifications. This is anecdotal and version/account-specific, not a platform rule.
- [Upstream issue #770](https://github.com/chenhg5/cc-connect/issues/770) reports `ret=-2` during long or chunked output; it does not establish a ten-message cap.
- [Upstream issue #1087](https://github.com/chenhg5/cc-connect/issues/1087) contains an earlier context-token persistence/expiry diagnosis, not the final established cause.
- [Merged upstream PR #1643](https://github.com/chenhg5/cc-connect/pull/1643) later reported empirical account-level outbound throttling at roughly five to six separate messages per 24 hours, introduced a default safe budget of four, and warned that retries during a penalty can extend it.

The exact number and recovery behavior can change across Weixin and CC Connect versions. The product conclusion remains: **do not select personal Weixin as the default for completion and error notifications that must arrive without user interaction.**

If the user explicitly insists:

1. explain the warning and record the choice;
2. verify the installed CC Connect version;
3. minimize messages and prefer a single final summary;
4. configure the upstream quota controls available in that version;
5. test beyond one happy-path message;
6. make local queue retention explicit when the platform refuses delivery;
7. never promise dependable unattended delivery.

Personal Weixin is not WeCom. WeCom uses a separate platform and protocol; assess it independently.

## Selection and binding flow

1. Inspect the installed CC Connect version and current projects without displaying tokens.
2. Present supported candidates and the personal-Weixin warning.
3. Wait for the user's explicit platform choice.
4. If CC Connect is absent, explain the upstream source, installation method, local files and permissions, then obtain confirmation before installation.
5. Create or select the user-approved dedicated or existing project and destination. A dedicated project is the safer default, not a hard requirement.
6. Let the user enter bot credentials through CC Connect's local UI or another local secret path; never ask for secrets in chat.
7. If inbound control was selected, restrict allowed senders and administrative commands; otherwise ignore inbound content.
8. Keep task classification and outbound notification delivery independent from any optional inbound agent session.
9. Send one synthetic notification and require visible confirmation from the user.
10. Record the platform, CC Connect version and verified delivery ID without storing the credential.

Configure one platform first. Add a second only after the first path, queue behavior and failure handling are proven.
