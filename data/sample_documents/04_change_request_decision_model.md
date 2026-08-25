# Apex Process Solutions — Change Request Decision Model

**Document type:** Fictional company policy (continuity with Module 4/5 prompt sets)
**Source:** Self-created fictional example for classroom use — no real company, client, or
confidential information

## Policy

Apex Process Solutions' PMO applies the following rule set when a change request is
raised against an active project:

- **ACCEPT** when the request comes from the customer, cost/timeline impact has been
  evaluated, and it supports the project's stated objective.
- **REJECT** when the request arrives at the end of the project, implementation is
  nearly complete, or it threatens the project baseline (schedule, budget, or scope
  already committed to the client).
- **ESCALATE TO COMMERCIAL** when the request is not aligned with the objective
  described in the project's Statement of Work (SOW).

A change request can trigger more than one of these conditions at once (for example,
arriving late *and* being outside the SOW). When conditions conflict, the PM should
state which condition is being prioritized and why, rather than defaulting silently
to one outcome.

## Example

*"Meridian Bank has asked, two weeks before go-live, to add a completely new
reporting module that was never mentioned in the original SOW. The core integration
is 95% complete and in final testing."*

This example triggers both the REJECT condition (late-stage, threatens baseline) and
the ESCALATE condition (not in the SOW). A well-reasoned answer should name both
triggers rather than picking one arbitrarily or hedging between accept and reject.

## Why this matters for AI-assisted PMO tools

Module 5 of this course found that a local model prompted directly (without
retrieval) applied only one of the two applicable rules to this exact example and
gave a full-sentence answer instead of the requested single-word classification.
Grounding the classification step in this document is intended to make the decision
rule itself unambiguous to the model at generation time.
