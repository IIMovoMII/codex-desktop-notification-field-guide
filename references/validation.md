# Validation

Test signal classification, resource use, privacy and delivery as one system.

## Fixture set

Create synthetic, version-labeled fixtures for:

- normal completion;
- structured server error, including retryable service failures;
- malformed or unfamiliar error;
- user interruption;
- approval request and resume;
- input request and resume;
- completion followed closely by interruption;
- interruption followed closely by completion;
- late JSONL append after a hook;
- Desktop process exit during work;
- planned maintenance exit;
- long silent task;
- CLI task;
- subagent task;
- file truncation, replacement and partial line.

Fixtures must not come from private conversations.

## State assertions

Verify:

- one terminal notification per task turn;
- explicit failures are not overwritten by weaker completion candidates;
- waiting states notify once per distinct request;
- resumed work can later reach a terminal state;
- long silence does not notify;
- process exit alone does not invent an error;
- maintenance markers suppress only the intended crash signal;
- CLI and subagent activity is filtered;
- unknown terminal failures still produce a useful generic alert.

Run race cases in both event orders.

## Monitoring assertions

Verify:

- only appended bytes are parsed;
- partial lines survive restart;
- file replacement invalidates the old cursor;
- directory notification overflow triggers bounded reconciliation;
- first use does not replay all old tasks;
- monitor startup closes the watcher-attachment race;
- idle CPU and disk reads stay within a measured budget;
- multiple hooks still produce one monitor process;
- the monitor exits cleanly after Desktop and pending work stop.

## Delivery assertions

Verify:

- notification is durable before send;
- successful delivery removes or marks it once;
- temporary outage retries with backoff;
- permanent auth failure enters a visible dead-letter state;
- restart does not lose queued items;
- timeout uncertainty does not create uncontrolled duplicates;
- platform quota is honored;
- switching user-selected CC Connect platforms preserves or deliberately handles queued items;
- inbound chat content cannot launch Codex or local commands.

## Privacy assertions

Inject synthetic:

- API keys;
- OAuth-like tokens;
- signed URLs;
- email addresses;
- absolute home paths;
- long provider errors;
- tool arguments.

Assert they do not appear in:

- hook spool;
- task-state store;
- outbox;
- channel payload;
- normal logs;
- test snapshots.

## Lifecycle assertions

From a clean stopped state:

1. launch Codex using the normal Desktop or Start-menu entry;
2. trigger the first supported lifecycle hook;
3. confirm one background monitor and the required CC Connect process start;
4. complete a synthetic task and receive one notification;
5. exit Desktop;
6. confirm terminal events settle and helpers stop;
7. repeat after an auth/API profile switch.

The user should not need a wrapper command for normal use.

## Upgrade gate

After a Codex upgrade:

1. rerun signal discovery;
2. compare hook inputs and timing;
3. generate fresh redacted fixtures;
4. compare JSONL schemas and source identifiers;
5. rerun state and race tests;
6. verify process detection;
7. test one real outbound notification;
8. enable the updated parser only after the gate passes.

## Release evidence

Record:

- Windows and Codex versions;
- supported states;
- source-filter result;
- fixture and race-test result;
- idle resource measurements;
- retry and restart result;
- privacy scan result;
- selected CC Connect platform and known quota limits;
- known ambiguous states.

Do not include private task IDs, credentials, local paths or conversation bodies.
