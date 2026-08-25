# RACI Matrix Reference Guide

**Document type:** PM reference / best-practice guide
**Source:** Standard project management practice (not company-confidential)

## What a RACI matrix is

A RACI matrix is a role-assignment tool that clarifies who does what on a task or
deliverable. Each person or role involved in a task is assigned exactly one of four
labels for that task:

- **R — Responsible:** The person who actually performs the work.
- **A — Accountable:** The person with final decision-making authority and
  ownership of the outcome. Ideally only one Accountable person per task.
- **C — Consulted:** People who must be consulted (two-way communication) before
  the task is finalized, but who do not perform the work or make the final call.
- **I — Informed:** People who need to be kept up to date (one-way communication)
  on progress or outcomes, but are not involved in doing or approving the work.

A RACI matrix is a role/responsibility tool, not a risk-tracking tool, a timeline,
or an activity log — that distinction matters because RAID and RACI are often
confused by name.

## Example RACI matrix

| Task | Dev Lead | PM | Client Sponsor | QA |
|---|---|---|---|---|
| Fix retry-logic bug | R | A | I | C |
| Approve change request | C | R | A | I |
| Confirm go-live readiness | C | A | I | R |

## Why this matters for AI-assisted PMO tools

Because "RAID" and "RACI" share three of four letters and both apply to project
governance, a language model answering from unguided memory can conflate the two,
invent an incorrect expansion of one acronym, or drop one of the four RACI roles.
Grounding the answer in this reference document reduces that risk.
