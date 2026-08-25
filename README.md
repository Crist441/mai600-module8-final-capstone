# MAI 600 Module 8 Final Capstone — Local RAG-Grounded PMO Risk Assistant

## Project Overview

A local, retrieval-augmented AI assistant that answers project-management-office (PMO) risk
governance questions grounded in a fictional company's own policy documents ("Apex Process
Solutions"), citing its sources rather than answering from the model's own memory. This is the
final version of the project started in the Module 6 proposal and continued in the Module 7
progress report.

## Problem Being Solved

PMO governance questions (what triggers escalation, how a RAID log differs from a RACI matrix,
when a change request should be rejected) have organization-specific, sometimes counter-intuitive
answers. A general-purpose model answering from unguided memory can confuse similar-sounding
concepts or invent a plausible but wrong threshold. This assistant grounds every answer in the
organization's actual policy text and cites the source, so a project manager can verify it before
acting.

## System Type

**Hybrid: RAG (primary) + a real, executed LoRA fine-tuning experiment (secondary, carried
forward from Module 7).** RAG is the primary approach for the core grounding problem; the
fine-tuning experiment is documented as real evidence for *why* RAG was chosen over fine-tuning
for this project, not as a competing production system.

## Tools and Models Used

- **Local LLM serving:** [Ollama](https://ollama.com) 0.32.5, running on the student's own laptop
  (no Colab, no external API)
- **Generation model:** `llama3.2:3b`
- **Embedding model:** `nomic-embed-text`
- **Retrieval:** cosine similarity over Markdown-section chunks, top-4 (widened from Module 7's
  top-2 — see Improvement from Prototype)
- **Fine-tuning (Module 7, carried forward):** `distilgpt2` + LoRA via `peft`
- **Evaluation / charts:** pandas, matplotlib

## Setup Instructions

1. Install [Ollama](https://ollama.com) and pull the two models used:
   ```
   ollama pull llama3.2:3b
   ollama pull nomic-embed-text
   ```
2. Start the Ollama server (`ollama serve`, or the Ollama desktop app) so the local API is
   available at `http://localhost:11434`.
3. `pip install -r requirements.txt`

## How to Run

- **Script:** `python src/run_pipeline.py` re-embeds the 10 knowledge-base documents and
  regenerates answers for all 10 test cases in `data/test_cases.csv`, saving results to
  `results/`.
- **Notebook:** `notebooks/module8_final_capstone.ipynb` walks through the same pipeline cell by
  cell with explanations, matching the structure of the Module 7 notebook it extends.
- **Interactive app (optional, high-code track):** `streamlit run app/streamlit_app.py` opens a
  chat-style demo in the browser — type a PMO question (or click one of the 3 example buttons,
  including a compound question) and get a real, cited answer from the same pipeline used for
  `results/`. Nothing in the app is simulated; every answer is a live call to local Ollama, so the
  first question takes ~2 minutes (embedding the 10-document knowledge base once) and each
  question after that takes ~30-70s (CPU-only generation).

## Data / Document Description

`data/sample_documents/` contains 10 fictional, classroom-safe Markdown policy documents (6
carried forward from Module 6/7, 4 new for this final version — see the article's Data
Description section for detail on why the 4 new documents were chosen and how they enable real
compound-question testing). `data/test_cases.csv` contains 10 test questions: 8 single-document
and 2 compound (each requiring two documents at once).

## Evaluation Method

Each of the 10 test questions was run through the real pipeline (embed → retrieve top-4 → generate
→ record). Retrieval hit rate, top-1 source match, and citation match are computed automatically
from the actual retrieved/generated data. Groundedness, format adherence, completeness,
helpfulness, and accuracy are hand-scored 1–5 (Claude-Code-assisted against a fixed rubric, spot
checked against the source documents) — the same five dimensions and method Module 7 used, so the
before/after comparison is apples-to-apples.

## Results Summary

See `results/summary_metrics.json`, `results/evaluation_scores.csv`, and
`results/improvement_comparison.csv` for the full numbers. In short: both previously-failing and
newly-designed compound questions now retrieve chunks from all required documents at top-4 (a
direct fix of the failure documented in Module 7), and Module 7's weakest single-document question
is now answered completely — but this final, harder test set also surfaced two genuine new
failures (one prompt-construction bug in the test harness, fixed and re-run; one real model
reasoning error on a compound question) that Module 7's easier 6-question set could not have
caught. See the article's Results, Evaluation, and Discussion sections for the full, honest
breakdown.

## Known Limitations

- CPU-only response time (mid-30s to over a minute per answer) is workable for drafting/review,
  not a live chat interface.
- The knowledge base (10 documents, 51 chunks) is still small; broader coverage would need more
  documents and more test questions before this could be trusted for real PMO use.
- Hand-scored quality dimensions are AI-assisted, not independently double-scored by a second
  human rater — see `ai_usage_disclosure.md`.
- Q10 (a compound question) shows a real, disclosed reasoning error: the model misapplied a
  Risk-to-Issue rule to a scenario where the triggering condition had already occurred.
- This system is a classroom prototype, not validated for real production PMO decisions. All
  answers should be reviewed by a human before acting on them.

## AI Usage Disclosure

See `ai_usage_disclosure.md`.

## GitHub Repository

**https://github.com/Crist441/mai600-module8-final-capstone**

Note: the Windows path to this assignment folder is too long for `git` to initialize reliably in
place (Windows' path-length limit), so this repository was built and committed in a short local
path and pushed to GitHub from there — the files here are identical to what's on GitHub. A
`mai600-module8-final-capstone-submission.zip` backup also sits in the parent `Submit/` folder,
per the assignment's "ZIP file as a backup" allowance.
