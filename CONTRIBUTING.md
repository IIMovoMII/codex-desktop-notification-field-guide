# Contributing

Contributions should improve the observation and delivery method without turning this repository into a preconfigured bot for one machine.

## Good contributions

- a reproducible Codex hook or JSONL observation with version context;
- a synthetic fixture for a race or error case;
- a more reliable state transition;
- a lower-overhead monitoring technique;
- a privacy or redaction improvement;
- a channel-neutral delivery pattern;
- a measurable validation method.

## Please avoid

- bot secrets, binding codes, user IDs or private channel endpoints;
- real prompts, responses or rollout files;
- absolute local paths or usernames;
- instructions that allow inbound chat to execute arbitrary local actions;
- platform claims without current evidence;
- generated bulk text that has not been technically reviewed.

## Pull request checklist

1. Explain the observed problem and environment.
2. Distinguish measured behavior from inference.
3. Add or update a synthetic fixture description.
4. State how the change affects privacy and duplicate delivery.
5. Update both language pages when their shared meaning changes.
6. Run:

~~~text
python scripts/validate_pack.py
~~~

7. Confirm that no credential, identifier or private conversation appears in the diff.

By contributing, you agree that your contribution is licensed under the MIT License.
