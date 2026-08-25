# Risk Probability × Impact Prioritization Framework

**Document type:** PM reference / best-practice guide
**Source:** Standard project management practice (not company-confidential)

## Purpose

This framework helps a PMO decide which of several open risks should be escalated
or addressed first, when time and attention are limited.

## Method

Each risk is rated on two independent scales:

- **Probability:** How likely is the risk to occur? (Low / Medium / High / Certain)
- **Impact:** If the risk occurs, how severe is the effect on schedule, budget,
  scope, or stakeholder confidence? (Low / Medium / High)

A risk with **Certain or High probability** combined with **High impact** should
generally be escalated before a risk with high probability but low/medium impact,
or a risk with high impact but low probability. A risk that is both low-probability
and low-impact can typically be monitored rather than escalated immediately.

This is a prioritization heuristic, not a strict formula — a PM should also weigh
how reversible the risk is, how much lead time is needed to respond, and how many
other workstreams the risk would affect if it occurred.

## Example application

| Risk | Probability | Impact | Priority |
|---|---|---|---|
| Client's primary technical contact leaving in one month | Certain | High (stalls all approvals) | Escalate first |
| Source export tool slower than planned | High | Medium (~1 week delay) | Monitor / plan mitigation |
| Low-severity library vulnerability in a minor UI component | Low | Low | Log and monitor |

## Why this matters for AI-assisted PMO tools

A model asked to prioritize risks should reference both probability and impact
explicitly for more than one risk, not just restate the risk with the most
alarming-sounding language. This document exists so a RAG system can ground a
prioritization answer in a consistent, explainable method rather than an
unstated internal judgment.
