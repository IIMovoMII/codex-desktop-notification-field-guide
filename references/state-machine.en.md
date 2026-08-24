# State machine

The state machine converts imperfect, out-of-order evidence into one user-facing result per task.

## Normalized events

Translate version-specific hooks and JSONL records into a small internal vocabulary:

~~~text
task_seen
turn_started
progress
completion_candidate
structured_error
unknown_error
user_interrupted
approval_requested
input_requested
desktop_started
desktop_exited
maintenance_started
maintenance_ended
~~~

Each event should carry:

- task key;
- turn key when available;
- event key;
- source;
- local timestamp;
- sanitized evidence category;
- schema version.

Avoid carrying prompt or response bodies through the state engine.

## Task states

One useful model is:

~~~mermaid
stateDiagram-v2
    [*] --> Observed
    Observed --> Running: turn_started
    Running --> WaitingApproval: approval_requested
    Running --> WaitingInput: input_requested
    WaitingApproval --> Running: activity_resumed
    WaitingInput --> Running: activity_resumed
    Running --> Settling: completion_candidate or desktop_exited
    Settling --> Completed: completion_confirmed
    Settling --> Failed: error_confirmed
    Settling --> Interrupted: interruption_confirmed
    Settling --> SystemStopped: automatic_stop_confirmed
    Settling --> NeedsReview: exit_without_terminal_evidence
    Running --> Failed: structured_error
    Running --> Interrupted: user_interrupted
    Running --> SystemStopped: automatic_stop
    Completed --> [*]
    Failed --> [*]
    Interrupted --> [*]
    SystemStopped --> [*]
    NeedsReview --> [*]
~~~

Adapt names to observed events. The important properties are explicit terminal states and a short, bounded settling state for late evidence.

## Precedence

Define deterministic precedence for conflicting signals. An example:

1. explicit structured failure;
2. explicit user interruption;
3. explicit version-proven automatic stop;
4. explicit successful completion;
5. validated unknown terminal failure;
6. process disappearance is only a weak candidate; after bounded settling without terminal evidence, finalize as `NeedsReview`, not `Failed`.

The correct order depends on observed Codex semantics. Record why an event wins and test both arrival orders.

Classify sanitized error families such as auth/permission, endpoint, rate limit, server, network/proxy/DNS/TLS/WebSocket, model, tool/permission, data shape and unknown. A transient 503 or timeout is only an error candidate while Codex is retrying. If progress resumes and the turn completes, clear it and notify completion only. Finalize failure or `SystemStopped` only after retry exhaustion, explicit termination or automatic-pause evidence. Never label a system stop as user interruption; use `NeedsReview` when the actor cannot be proven.

## Waiting states

Approval and input waits are actionable, not failures.

Notify once when the task enters the waiting state. If it resumes and later requests attention again, issue a new notification only when the request has a distinct event key or turn key.

Do not infer waiting merely because no new bytes arrive. Require an explicit hook, structured JSONL record or another version-proven signal.

There is no assumed universal generic input-request hook. If the installed version does not expose a proven signal, report input-wait notification as unsupported instead of guessing.

## No timer-based stuck state

Long silence is normal for some tasks. Therefore:

- do not transition from Running to Failed or Stuck based only on elapsed time;
- do not send repeated reminders while a task remains quiet;
- do monitor the health of the local observer separately;
- allow a user-configurable reminder only as an explicit product feature, disabled by default and labeled as a timer, not failure detection.

## Settling window

Hooks, file writes and process events can arrive in different orders. Use a short bounded window after a completion candidate or Desktop exit:

- continue consuming already queued events;
- re-read only changed files;
- allow stronger evidence to replace a weaker candidate;
- finalize once the window closes or an unambiguous terminal event arrives.

This is event convergence, not a long-task timeout.

If Desktop restarts and the same task resumes before an exit candidate is finalized, cancel that candidate. Otherwise, when the bounded drain ends with no terminal evidence, emit “Desktop exited; result unknown, please review” and enter `NeedsReview`.

## Idempotency and deduplication

Derive a stable notification key from fields such as:

~~~text
task_key + turn_key + terminal_state + source_event_key
~~~

Persist emitted keys. Replaying a hook, restarting the monitor or rereading a late JSONL line must not generate a duplicate.

Do not deduplicate purely on human-readable text; two different turns can have the same title and message.

## Planned maintenance

A cooperating local tool can write a short-lived marker containing:

- maintenance ID;
- start time;
- expected maximum duration;
- allowed process set;
- no credential or route detail.

When Desktop exits during a valid marker, suppress crash classification but continue processing explicit task errors. Expired markers must not hide genuine later failures.

## State persistence

Persist only what restart recovery needs:

- current non-terminal state;
- cursor references;
- last event key;
- emitted notification keys;
- settling deadline;
- maintenance marker reference.

Use atomic writes and schema versions. On corrupt state, rebuild from a bounded recent event window rather than scanning all history blindly.
