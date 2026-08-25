# Signal discovery

Build the notifier around evidence from the installed Codex version, not a remembered event schema.

## Runtime inventory

Record:

- operating system, desktop environment and Codex Desktop versions;
- Desktop executable path and process tree;
- whether the app combines ChatGPT and Codex surfaces;
- Codex home and rollout roots expressed with generic paths;
- hook configuration location and supported hook names;
- JSONL record types emitted during a controlled task;
- SQLite metadata needed for task title or project identity;
- source fields that distinguish Desktop, CLI and subagents;
- installed CC Connect version, configuration location and candidate platforms.

Do not print credentials, prompt bodies or conversation text.

## Controlled observation set

Create disposable, non-sensitive tasks that each exercise one outcome:

1. normal short completion;
2. explicit tool error;
3. transport or server error;
4. user interruption;
5. approval request;
6. user-input request;
7. Desktop exit during a task;
8. long-running work with no event for an extended period;
9. CLI task;
10. subagent task.

Capture only event structure, field names, ordering and timing. Replace titles, identifiers, paths and bodies with synthetic values before turning observations into fixtures.

## Hooks

Use the current [official Hooks reference](https://learn.chatgpt.com/docs/hooks) as the baseline. Review the active hook source and trust state; use either `hooks.json` or inline `[hooks]` in one layer to avoid a merge warning. Changed non-managed definitions may require review again.

For every hook supported by the installed build, determine:

- when it fires;
- whether Codex waits for it;
- input delivery format;
- exit-code behavior;
- timeout behavior;
- environment inherited by the hook;
- whether it fires for Desktop, CLI or both;
- whether it can start a background helper without blocking.

Use `SessionStart` for a minimal lazy wake. Matching command hooks for one event run concurrently: another `Stop` hook may still request continuation, and `stop_hook_active` does not prove all peers have settled. Treat `Stop` only as a completion candidate, return valid JSON without requesting continuation, and let later activity cancel that candidate. Do not copy the final assistant message by default; if the user opts in, write only a locally bounded and redacted excerpt. `SessionEnd` does not fire merely because the user switches tasks, may occur after close/archive/delete or a long idle period, and always runs synchronously even when configured as async. Use it only for cleanup, never per-turn completion or lazy async startup.

Hooks should not:

- call the messaging network;
- parse large history files;
- wait for another process;
- read prompt content unnecessarily;
- start Codex CLI.

## JSONL

Map:

- session metadata;
- task source identifier;
- turn start and completion records;
- structured error fields;
- interruption records;
- approval and input requests;
- assistant final-output boundaries;
- late records appended after a stop signal;
- archived-file behavior.

Do not assume the first line is the only metadata source. Prefer structured, version-proven events over matching human-readable error text. Keep the parser tolerant of unknown records and strict about malformed records that affect a decision. Treat JSONL and SQLite layouts as internal formats: gate parser changes by Codex version and degrade unsupported classifications to “needs review” instead of guessing.

## Process evidence

Discover the exact process set that means Desktop is alive. Process evidence can:

- wake reconciliation when the app starts;
- suppress startup before Desktop exists;
- begin a bounded settling period after exit;
- stop the local monitor when no pending work remains.

Process disappearance alone cannot classify the task as failed. Operating-system updates, user exit and planned auth switching can all close Desktop intentionally.

After a bounded final drain, an active task with Desktop gone and no terminal evidence must close as “needs review.” If the app restarts and the same task resumes before finalization, cancel that candidate.

## Source filtering

Find a stable, version-proven way to accept only user-facing Desktop tasks. Possible evidence includes:

- a session source field;
- parent task relationship;
- process ancestry;
- project or surface metadata.

Do not filter by title text. Build synthetic fixtures for Desktop, CLI and subagent events and assert that only intended tasks reach notification state.

## CC Connect delivery discovery

CC Connect is required. Before installation or configuration, inspect whether it is already present and read [CC Connect platform selection](cc-connect-platform-selection.en.md). Then present the supported choices and ask the user which one to connect.

For each candidate CC Connect platform, determine:

- whether the platform supports outbound bot messages;
- binding or authorization flow;
- credential storage needs;
- daily or burst quotas;
- reply gates;
- message-length limits;
- retry semantics;
- duplicate-delivery behavior;
- whether CC Connect can report confirmed acceptance.

Do not infer the platform from an old binding. Do not recommend personal Weixin for unattended notifications; explain its outbound budget and session limitations, distinguish it from WeCom, and require an explicit choice if the user insists.

## Discovery output

Produce:

- a versioned signal table;
- redacted synthetic fixtures;
- a supported-state table;
- known ambiguous cases;
- source-filter rules;
- monitor lifecycle evidence;
- selected CC Connect platform, capability and quota notes;
- assumptions that must be retested after upgrade.
