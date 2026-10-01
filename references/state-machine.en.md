# State classification and deduplication

[中文](state-machine.md)

Combine evidence by task and turn. Normalize error text, hooks, and process changes instead of sending a message from each source.

## States and evidence

| Result | Required evidence | Next action |
| --- | --- | --- |
| Running | New activity or no terminal evidence yet | Wait for events; silence never establishes a stuck task |
| Awaiting approval/input | An explicit, currently active request | Notify once per request; clear on response or resumption |
| Settling candidate | Stop, possible exit, or pending late records | Await independent terminal evidence; allow cancellation |
| Completed | Explicit success for this turn | Close the turn and commit one terminal notification |
| Failed | Explicit turn failure or exhausted retries | Close the turn and send a sanitized error category |
| User interrupted | Explicit user cancellation/pause evidence | Distinguish from automatic stopping |
| System stopped | Proven non-user stop evidence | Explain that attention is needed without inventing a user action |
| Unknown outcome | Observation cannot continue and settling yields no terminal evidence | Ask for review without inventing a failure cause |

Mark generic input waiting unsupported without evidence. Waiting longer is not a new request. If a queued wait alert has already been resolved, cancel it or turn it into a historical summary according to the agreed policy.

## Stop races

Neither `Stop` nor `stop_hook_active` alone proves completion. Another matching hook may continue the turn. Subsequent activity cancels the old candidate; only independent success, failure, or interruption evidence determines the outcome.

A short settling window collects late evidence; it does not mean “declare success after a few seconds.” With only Stop and a running Desktop, continue observing. If observation must end, report an unknown outcome. SessionEnd does not replace a per-turn terminal event.

## Error recovery and ordering

Separate a single failed tool operation, final Codex turn failure, and bridge delivery failure. A 503 or timeout may be undergoing automatic retries. Clear the candidate when recovery leads to success and notify the final outcome only.

Prefer structured status, error codes, and recovery relationships. Text-based classification must not mistake a quoted error in a reply for an actual failure. Categories can include auth, quota, server, network, model, tool, data format, and unknown. An unknown cause does not prevent reporting a proven failure.

Establish task/turn membership and causal order before applying locally tested conflict rules. A universal “any error wins over success” rule can let an old recoverable error override later success. Late terminal evidence for an old turn must not clear a newer turn.

If stronger evidence arrives after delivery, retain the original record and optionally send one correlated correction. Do not silently rewrite sent history or repeatedly create new alerts.

## Process exit and maintenance

When Desktop's main application disappears, create exit candidates only for currently active tasks. Drain late writes briefly. Cancel when the process returns and the task continues; otherwise resolve from terminal evidence or report unknown. An auxiliary-service restart must not create alerts for every task.

An auth switcher or updater can write a short-lived maintenance marker before exit with owner, scope, and expiry. Suppress only planned-exit candidates, not explicit errors, interruptions, or wait requests. Clear it after maintenance and expire it automatically.

## Stable identity and commit ordering

Keep one terminal notification slot per turn, for example:

~~~text
terminal_key = task_identity + turn_identity + "terminal"
waiting_key  = task_identity + turn_identity + request_identity
~~~

State labels, titles, excerpts, error wording, and duplicated source events must not create another terminal slot. Update classification before delivery; a post-delivery correction has its own correlated identity. Without a stable turn ID, establish a persistent recoverable substitute instead of generating a new random identity on every replay.

Only the current active turn participates in exit inference. Retire superseded unfinished turns so one exit cannot fan out into old abnormal alerts. Preserve genuine queued or delivered historical notices; retirement does not mean deletion.

Cursors, decisions, outbox, and deduplication ledger must recover without missing records. Use a shared transaction or persist a pending decision before idempotent enqueue. “Save state, then queue” is still lossy without recovery of the gap.

Local deduplication does not guarantee one remote delivery; see the uncertainty window in [delivery](delivery.en.md).
