# Security policy

[中文](SECURITY.md)

## Never publish

- bot secrets, tokens, binding codes or recipient identifiers;
- real prompts, responses or rollout files;
- private channel endpoints;
- local usernames or home paths;
- OAuth or API credentials from Codex;
- logs containing authorization headers or signed URLs.

## Reporting a security issue

Prefer GitHub private vulnerability reporting when enabled for this repository. Regardless of channel, do not publish secrets or real task content; start with affected versions, a minimal synthetic reproduction, and redacted field structure.

If messaging credentials were exposed, revoke or rotate the affected credentials, inspect bindings and use records as supported, then clean up public content and related Git history. If only a recipient identifier was exposed, assess its actual authority and privacy impact rather than treating the identifier itself as an authentication token.

## Design boundary

- Keep messaging secrets in a restricted local directory or the platform's native secret store.
- Hooks write minimal local events and do not access the network.
- Recommended minimal notifications omit prompts, tool arguments, results, and full responses unless the user opts into a redacted excerpt.
- The user chooses inbound behavior. If enabled, restrict senders and actions, with confirmation, replay protection, audit, rate limits, and a disable control. Do not turn arbitrary text directly into local commands.
- Redact delivery queues and logs and define a retention period.
- Require user review before installing live hooks or binding a platform account.

Public fixtures must be synthetic; do not publish a lightly renamed private conversation.
