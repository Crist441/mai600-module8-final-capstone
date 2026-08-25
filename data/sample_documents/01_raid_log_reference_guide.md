# RAID Log Reference Guide

**Document type:** PM reference / best-practice guide
**Source:** Standard project management practice (not company-confidential)

## What a RAID log is

A RAID log is a single tracking document used by project managers to record four
categories of project information:

- **R — Risks:** Uncertain future events that could negatively affect the project if
  they occur (e.g., "the primary vendor may miss the delivery date").
- **A — Assumptions:** Things the team believes to be true for planning purposes, but
  which have not been confirmed (e.g., "we are assuming the client's IT team will
  provision test environments by Week 3").
- **I — Issues:** Problems that have already happened and need active resolution
  (e.g., "the retry-logic bug is currently blocking the demo").
- **D — Dependencies:** Tasks, deliverables, or decisions that this project relies on
  from another team, vendor, or project (e.g., "go-live depends on Security signing
  off the penetration test").

A RAID log is not a general status journal, a meeting-notes document, or a generic
activity timeline. Each entry belongs to exactly one of the four RAID categories, and
each entry should record: a short description, the owner, the date raised, the
current status, and the planned response (mitigation for a risk, resolution plan for
an issue, confirmation plan for an assumption, or tracking status for a dependency).

## Example RAID log entries

| Category | Entry | Owner | Status |
|---|---|---|---|
| Risk | Source database export may be slower than the migration window allows | Data Lead | Monitoring |
| Assumption | Client's technical contact remains available through go-live | PM | Unconfirmed |
| Issue | Retry-logic bug duplicating records in the staging table | Dev Lead | In progress |
| Dependency | Security sign-off required before production deployment | Security Team | Pending |

## Why this matters for AI-assisted PMO tools

A local language model asked to explain a RAID log without grounding in this
definition may describe it as a generic activity log or status journal — a fluent
but incorrect answer, because "RAID" is also a common acronym in unrelated fields
(for example, "Redundant Array of Independent Disks" in storage technology). Any
AI system operating in this domain should retrieve and cite this definition rather
than rely on the model's own unguided recall of the term.
