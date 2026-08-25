# AI Usage Disclosure

## AI Tools Used

- ChatGPT: Not used for this module.
- Claude: Not used directly for this module.
- Gemini: Not used.
- GitHub Copilot: Not used.
- Claude Code: Used extensively — pipeline code, document authoring, evaluation scoring assistance, README/article drafting.
- Hugging Face: `peft`/`transformers` libraries used in Module 7's LoRA experiment, carried forward unchanged into this submission.
- Ollama: Used for all embeddings (`nomic-embed-text`) and generation (`llama3.2:3b`), run locally on the student's own laptop.
- LM Studio: Not used.
- Other: None.

## How I Used AI

Claude Code was used to: (1) widen the Module 7 knowledge base from 6 to 10 documents by
drafting 4 new fictional PMO policy documents in the same style and register as the original
6 (which I reviewed and approved before they were used); (2) write the Module 8 retrieval
pipeline code (`src/rag_pipeline.py`), which is a direct, minimally-modified extension of the
Module 7 notebook's own chunking/embedding/retrieval/generation functions, widened from top-2
to top-4 retrieval; (3) design 4 new test questions, including 2 compound questions that
deliberately span two documents, to directly re-test the compound-question retrieval failure
documented in Module 7; (4) run the pipeline for real against my local Ollama installation and
capture the actual retrieved chunks, generated answers, and response times — no result in
`results/` is simulated or hand-written; (5) apply the same evaluation rubric Module 7 used
(retrieval hit, citation match, groundedness, format adherence, completeness, helpfulness,
accuracy) to score the 10 real generated answers; (6) draft the README, improvement comparison
table, and the final APA-style article from those real results; (7) build the optional
`app/streamlit_app.py` demo interface (high-code track) so the pipeline can be tried interactively
instead of only read from CSVs — it calls the same `src/rag_pipeline.py` functions used for the
real evaluation run, with no separate or simulated logic.

## Prompts Used

Representative prompts given to Claude Code during this module:
- "Adapt the Module 7 RAG pipeline to widen retrieval from top-2 to top-4 and re-test the
  compound RAID/RACI question that failed before."
- "Write 4 new PMO policy documents in the same style as the existing 6, designed so two of
  them can be used together in a compound question."
- "Run the pipeline for real against local Ollama and save the actual outputs — do not
  fabricate results."
- "Score these 10 real generated answers using the same rubric as Module 7 and explain each
  score."

## What I Verified Myself

I reviewed all 4 new policy documents for factual consistency with the original 6 before they
were used in the pipeline. I reviewed the real generated answers in `results/generated_outputs.csv`
against the expected sources and expected answer notes in `data/test_cases.csv` before accepting
the evaluation scores. This review is what caught a real bug: Q7's first answer looked wrong (it
described the document's general purpose instead of answering the specific question), and tracing
it back to `data/test_cases.csv` showed an unquoted comma inside the question text had shifted the
CSV columns, so the model had actually been given a truncated question. I fixed the CSV (quoted
the field) and re-ran Q7 in isolation to get the corrected result reported in `evaluation_scores.csv`. I confirmed the response-time and retrieval numbers came from the actual
`benchmark_results.csv` and `retrieved_chunks.csv` outputs of this run, not from Module 7's
numbers being reused. I checked that the LoRA fine-tuning evidence carried forward from Module 7
(`checkpoints/`) is presented as unchanged, real, already-executed work — not re-labeled as new.

## Failures or Limitations

Claude Code's automated citation-match and groundedness scoring (checking whether the expected
source ID literally appears in the answer text) is a proxy, not a full read of every answer; I
spot-checked the flagged cases before trusting the summary metrics. The hand-scored quality
dimensions (completeness, helpfulness, accuracy) were scored by Claude Code against a fixed
rubric rather than by me reading and scoring all 10 answers independently — this is a real
limitation of the evaluation, disclosed rather than hidden, consistent with how Module 7 also
used AI-assisted scoring.

## Academic Integrity Statement

I confirm that AI was used as a learning and support tool, not as a replacement for my own work.
The project domain (PMO risk governance), the underlying Module 6/7 design decisions, and the
review of every generated document and result are my own.
