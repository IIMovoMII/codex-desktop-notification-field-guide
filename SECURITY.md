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

Inbound command execution is outside the default design. Any implementation that adds it requires a separate security review.
