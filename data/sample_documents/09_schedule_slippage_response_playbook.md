# Apex Process Solutions — Schedule Slippage Response Playbook

**Document type:** Fictional company policy (continuity with Modules 4–7)
**Source:** Self-created fictional example for classroom use — no real company, client, or
confidential information

## Purpose

This playbook defines the required steps once a task or milestone is confirmed behind its
baseline schedule, so the response is consistent across PMs and projects.

## Required steps once a task is confirmed behind baseline

1. **Confirm, do not assume.** Verify the task is actually behind baseline using the
   project schedule tool, not a verbal update. A task that is "probably going to slip" is
   a Risk in the RAID log, not yet a schedule slippage.
2. **Quantify the slip.** Record the number of working days behind baseline and whether it
   is on the critical path. A slip on a non-critical-path task with float remaining does
   not trigger the remaining steps below.
3. **Assess downstream impact.** Identify every milestone or client-committed date that
   depends on the slipped task, using the RAID log's Dependency entries as the source of
   truth for what depends on what.
4. **Decide: recover, replan, or escalate.** Recovery (adding resources or working
   overtime) is preferred if it fits within the Budget Variance Escalation Policy's
   thresholds. Replanning (moving the date) requires client communication. If neither is
   possible without breaching a client-committed date, escalate per the PMO Risk
   Management Policy's escalation rule.
5. **Log the outcome.** Update the task's status and, if escalated, write the escalation
   note following the PMO Escalation & Steering Committee Communication Guide's five-part
   structure.

## Example

*"The data migration task is 6 working days behind baseline and sits on the critical path
for the go-live milestone."* Steps 1–2 are already satisfied by this statement. Step 3
requires checking which milestones depend on data migration. If recovery would add cost
above the 10% budget variance threshold, step 4 requires escalation, not a quiet recovery
attempt.

## Why this matters for AI-assisted PMO tools

This playbook explicitly references three other governance documents (RAID log,
budget variance policy, escalation guide), so it is a good test of whether a model can
follow a multi-step procedure without skipping the assess-impact step or jumping straight
to escalation.
