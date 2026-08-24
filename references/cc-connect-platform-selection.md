# CC Connect 平台选择

[English](cc-connect-platform-selection.en.md)

[CC Connect](https://github.com/chenhg5/cc-connect)是本指南固定的消息桥，但具体通讯平台由用户决定。只读盘点后、安装或绑定前，必须先询问。

## 必问问题

> 你希望把 Codex Desktop 提醒发到哪个 CC Connect 平台：QQ 官方机器人、Telegram、飞书／Lark、个人微信、企业微信，还是当前版本支持的其他平台？

只列出检测到的 CC Connect 版本真实支持的平台，并说明搭建成本、网络条件和限制。旧绑定不能代替用户选择。

## 常见选择

| 平台 | 连接方式与条件 | 建议 |
| --- | --- | --- |
| [QQ 官方机器人](https://github.com/chenhg5/cc-connect/blob/main/docs/qqbot.md) | 官方接口与 WebSocket；无需公网 IP；需要开发者认证 | 用户主要使用 QQ 时优先考虑 |
| [Telegram](https://github.com/chenhg5/cc-connect/blob/main/docs/telegram.md) | Bot API 长轮询；无需公网 IP；需要可访问 Telegram | 通用且简单 |
| [飞书／Lark](https://github.com/chenhg5/cc-connect/blob/main/docs/feishu.md) | 长连接；无需公网 IP；需要应用权限 | 适合稳定个人或团队流程 |
| [QQ OneBot](https://github.com/chenhg5/cc-connect/blob/main/docs/qq.md) | 还需 NapCat 等 OneBot 组件 | 说明额外组件和非官方风险后再选 |
| [个人微信](https://github.com/chenhg5/cc-connect/blob/main/docs/weixin.md) | iLink、二维码登录 | **不推荐无人值守提醒** |
| 企业微信或其他内置平台 | 取决于当前版本 | 按对应官方说明单独评估 |

## 为什么不推荐个人微信

必须把几类证据分开，不能拼成一个“固定十条”的结论：

- 某个本机环境曾观察到累计约十条未回复提醒后发送受限。这只是特定时间、账号和版本的现场现象，不能推广成平台规则。
- [问题 #770](https://github.com/chenhg5/cc-connect/issues/770)记录的是长内容／分段发送出现 `ret=-2` 中断，**并不能证明大约十条消息的上限**。
- [问题 #1087](https://github.com/chenhg5/cc-connect/issues/1087)曾把长时间未活动后的失败归因于 `context_token` 持久化或过期；这是历史诊断，不应继续当作最终根因。
- 后来合并的 [PR #1643](https://github.com/chenhg5/cc-connect/pull/1643)通过实测把 `ret=-2 prepare failed` 解释为账号级主动发送预算／限流：约 24 小时五到六条独立消息可能触发，默认安全预算设为四条；受限期间继续重试还可能延长惩罚。二维码重新登录会形成新账号／预算，但这不是可靠无人值守恢复方案。

数字仍可能随微信服务端与 CC Connect 版本变化，稳定结论只有一个：个人微信不适合必须可靠到达的无人值守提醒。个人微信和企业微信不是同一平台，后者要单独评估。

如果用户仍坚持使用个人微信：记录已知限制、检查当前版本的额度保护、尽量合并通知、对拒绝投递保留本地队列、测试多条消息，并明确不承诺持续可靠到达。

## 绑定闭环

1. 查看已安装版本与项目，不显示令牌。
2. 展示真实候选和个人微信警告，等待用户选择。
3. CC Connect 未安装时，说明来源、文件、权限与卸载方式并获得确认。
4. 建立专用通知项目或选择现有项目，并确认它是专用还是共享实例。
5. 用户通过本地界面录入凭据；对话中不接收秘密。
6. 把提醒端限制为单向发送，即使 CC Connect 支持交互式代理。
7. 发送一条合成通知，要求用户确认可见。
8. 记录平台、CC Connect 版本和脱敏投递编号。

绑定失败时不启用“已部署”状态：保留本地队列，显示认证、额度、网络或目标会话类别，让用户修复或改选平台。先打通一个平台，再增加第二个。
