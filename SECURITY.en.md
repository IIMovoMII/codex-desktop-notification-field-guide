# Security policy

This field guide describes software that observes private local task state and sends messages through an external channel.

## Never publish

- bot secrets, tokens, binding codes or recipient identifiers;
- real prompts, responses or rollout files;
- private channel endpoints;
- local usernames or home paths;
- OAuth or API credentials from Codex;
- logs containing authorization headers or signed URLs.

## Reporting a security issue

Use a GitHub private security advisory for a vulnerability in this guide or its validator. Do not open a public issue containing secrets or private task content.

If a messaging credential or recipient identifier was exposed:

1. revoke or rotate the credential;
2. invalidate the binding where supported;
3. remove the value from visible content and Git history;
4. review channel and local bridge logs;
5. disclose only a redacted timeline.

## Design boundary

- Keep messaging secrets in a restricted local directory or the platform's native secret store.
- Hooks write minimal local events and do not access the network.
- Recommended minimal notifications omit prompts, tool arguments, results, and full responses unless the user opts into a redacted excerpt.
- Inbound control is an optional user-selected module. If enabled, require an authenticated sender allowlist, replay protection, a narrow command grammar, confirmation for sensitive actions, audit logging, rate limiting, a kill switch, and a separate security review. Notification-only implementations should ignore inbound content.
- Redact delivery queues and logs and define a retention period.
- Require user review before installing live hooks or binding a platform account.

Public fixtures must be synthetic; do not publish a lightly renamed private conversation.
