# Apex Process Solutions — Vendor and Contractor Risk Addendum

**Document type:** Fictional company policy (continuity with Modules 4–7)
**Source:** Self-created fictional example for classroom use — no real company, client, or
confidential information

## Purpose

This addendum extends the PMO Risk Management Policy to risks that originate outside the
project team — specifically, risks caused by a vendor, subcontractor, or third-party
supplier that Apex Process Solutions does not directly control.

## Logging rule

A vendor- or contractor-caused risk must be logged in the RAID log under the **Risk**
category (not Issue) while the vendor has not yet missed a committed date, and moved to
**Issue** the moment a committed vendor date is actually missed. The entry must name the
vendor's role (for example, "primary integration vendor"), not the vendor's company name
directly in client-facing extracts, to avoid disclosing vendor relationships to the wrong
audience.

## Escalation trigger specific to vendors

A vendor-caused risk must be escalated to the weekly PMO steering review, in addition to
the standard escalation rule in the PMO Risk Management Policy, whenever the vendor delay
is likely to cause a **downstream cost impact** — for example, rework hours, expedited
shipping, or a change request from the client to cover the gap. This is because vendor
risk is a common source of budget variance, and the Budget Variance Escalation Policy
should be checked whenever a vendor risk is logged.

## Example

*"The primary integration vendor has confirmed their API delivery will slip by two weeks.
Apex's own team can absorb a one-week slip without cost impact, but a two-week slip will
require contractor overtime to hold the client go-live date."* This should be logged as a
Risk (not yet an Issue, since the date has not passed) and cross-checked against the
Budget Variance Escalation Policy because of the likely overtime cost.

## Why this matters for AI-assisted PMO tools

Vendor risk sits at the intersection of two governance documents — the RAID log rules and
the budget variance rules — so a model that only retrieves one document at a time can miss
the cost-escalation trigger. This is a deliberate test of whether retrieval surfaces both
relevant documents for a compound vendor-cost question.
