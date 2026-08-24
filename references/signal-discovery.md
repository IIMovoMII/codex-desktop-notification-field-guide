# Signal discovery

Build the notifier around evidence from the installed Codex version, not a remembered event schema.

## Runtime inventory

Record:

- Windows and Codex Desktop versions;
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

For every hook supported by the installed build, determine:

- when it fires;
- whether Codex waits for it;
- input delivery format;
- exit-code behavior;
- timeout behavior;
- environment inherited by the hook;
- whether it fires for Desktop, CLI or both;
- whether it can be trusted to start a background helper.

A hook documented or configured as asynchronous may still be launched synchronously in a particular integration path. Measure elapsed impact. Keep hook work to a local append and optional idempotent process start.

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

Do not assume the first line is the only metadata source. Keep the parser tolerant of unknown records and strict about malformed records that affect a decision.

## Process evidence

Discover the exact process set that means Desktop is alive. Process evidence can:

- wake reconciliation when the app starts;
- suppress startup before Desktop exists;
- begin a bounded settling period after exit;
- stop the local monitor when no pending work remains.

Process disappearance alone cannot classify the task as failed. Windows updates, user exit and planned auth switching can all close Desktop intentionally.

## Source filtering

Find a stable, version-proven way to accept only user-facing Desktop tasks. Possible evidence includes:

- a session source field;
- parent task relationship;
- process ancestry;
- project or surface metadata.

Do not filter by title text. Build synthetic fixtures for Desktop, CLI and subagent events and assert that only intended tasks reach notification state.

## CC Connect delivery discovery

CC Connect is required. Before installation or configuration, inspect whether it is already present and read [CC Connect platform selection](cc-connect-platform-selection.md). Then present the supported choices and ask the user which one to connect.

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
