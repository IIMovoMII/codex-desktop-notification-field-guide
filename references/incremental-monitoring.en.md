# Incremental monitoring and lifecycle

[中文](incremental-monitoring.md)

Following Desktop should not depend on a particular icon. First choose between starting after the first valid event and starting when the Desktop process appears.

## Startup choices

| Choice | Approach | Acceptance boundary |
| --- | --- | --- |
| Task-triggered | A trusted global hook starts a helper | No guarantee of a running monitor before an event or when hooks do not run |
| Process-triggered | Native process events, a service manager, or a lightweight login observer | Cover different launch paths and Desktop already running when the observer starts |

A special wrapper is not entry-point-independent integration. Explain any persistent observer and resume-from-sleep behavior according to the user's choice.

## Hook startup case

Windows testing exposed two independent issues: a single early process snapshot can miss startup, and quoted executable paths that work in cmd need a call operator in PowerShell. A reference flow:

1. Persist a minimal hook event, hand off quickly, and bound work per launch.
2. Serialize helper startup using a user-scoped OS mutex/file lock. Do not delete a lock merely because its file is over 30 seconds old; the owner may still be working.
3. Retry Desktop and session-metadata discovery within a deadline. Wait for an incomplete first record, reject a proven CLI/subagent source, and require a current process rather than only an old Desktop transcript.
4. Verify process identity and readiness. A PID file does not prove liveness; liveness does not prove watchers or the bridge are ready. Account for PID reuse across starts.
5. Retry transient startup failures a small number of times. Missing configuration, binding, or permission needs a visible reason. Later valid hooks can retry without infinite spawning.
6. Log the trigger, phase, duration, result, and error category without prompts, tokens, or raw exception bodies.

A startup lock only protects startup. Enforce single-instance ownership throughout monitor execution, including races with manual repair. Respect pause/disable state so hooks do not restart a deliberately disabled notifier.

“Wait up to 30 seconds for discovery, then attempt service startup three times” is an example, not a universal setting or a 30-second total-runtime guarantee.

## Test the actual command execution

Pin a verified interpreter and encoding, then quote for the actual shell. PowerShell needs `&` to invoke a quoted executable path; handle quotes, dollar signs, and other path characters literally. UTF-8 fixes encoding, not shell syntax.

Tests should match Desktop's shell, working directory, environment, and timeout. Python's `shell=True` normally uses cmd on Windows and cannot stand in for PowerShell. Ensure detached helpers do not inherit hook input/output pipes and survive normal hook exit, job-object cleanup, and intended timeout behavior. After changes, reload/trust the hooks and test a real cold start.

## Incremental reads and recovery

Use native file notifications or an equivalent event interface. Store file identity and committed byte position; read only new complete records. Coalesce duplicate wakeups, retain partial lines, and recover boundedly after replacement, truncation, or path aliases rather than using an invalid offset.

Establish an explicit first-install baseline to avoid replaying all history. With existing cursors, catch up missing new events. Reconcile the watcher-attachment race once, and reconcile after sleep or notification overflow. Do not wait for another new message before processing an existing backlog.

Commit a cursor only after its state and outbound decision are recoverable, using a transaction or replayable journal. Bound reads, concurrency, and log retention. If needed, reconcile active-file metadata infrequently; do not reread all bodies or infer failure from silence.

## Separate observation from sending

Identify the Desktop main application so an auxiliary service restart is not mistaken for app exit. With multiple windows, check remaining relevant instances. After confirmed exit, drain late events for a bounded period and let the [state machine](state-machine.en.md) determine the outcome.

Stopping observation and stopping delivery are separate decisions. Immediate exit defers pending messages; bounded sender-only finishing keeps a dedicated bridge alive briefly. Implement the selected policy through [delivery](delivery.en.md). A shared CC Connect instance is not owned by the notifier and must not be stopped with Desktop.
