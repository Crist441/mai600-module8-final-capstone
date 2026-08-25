# Fine-Tuning / Checkpoint Notes

A real LoRA fine-tuning experiment was run for this milestone (optional high-code path, guide
Section 8: "LoRA adapter demo"). This is a genuine, executed training run — every number below
comes from `checkpoints/finetune_training_log.json`, `checkpoints/finetune_comparison_results.csv`,
and `checkpoints/finetune_qualitative_scoring.csv`, not a simulation.

## Why fine-tuning was originally deprioritized

Per the Module 6 proposal, the problem this project targets is a **grounding** gap, not a **format
or style** gap: Module 5's benchmark already showed `llama3.2:3b` reproduces required output
formats correctly, and the Module 7 RAG evaluation confirmed this again (5.0/5 average Format
adherence). Fine-tuning is the right tool for a different failure mode — "the model doesn't follow
our house style/format consistently." This experiment tests that directly, on a task RAG had not
yet been asked to do: generating Apex Process Solutions' required 5-part escalation-note format
(`data/sample_documents/06_pmo_escalation_communication_guide.md`) from a brand-new, freeform risk
note, with no retrieval at generation time.

## What was actually run

- **Base model:** `distilgpt2` (82M parameters) — chosen to keep CPU-only training time reasonable.
- **Method:** LoRA via `peft` (`r=8`, `alpha=16`, `target_modules=["c_attn"]`, dropout 0.05).
  Trainable parameters: 147,456 of 82,060,032 (0.18%).
- **Data:** 20 real, self-authored examples (10 fictional PM risk/escalation scenarios, 2 differently
  worded freeform notes per scenario) — `data/finetune_train.jsonl` (14 rows) and
  `data/finetune_test.jsonl` (6 rows, from 3 scenarios held out entirely, not just reworded, so the
  test set is a genuine holdout). Script: `gen_finetune_dataset.py`.
- **Training:** 15 epochs, batch size 2, learning rate 3e-4, 105 steps, real wall-clock time
  **177.3 seconds** on a CPU-only laptop. Real loss curve: **4.61 → 3.40**, a clean, converging
  decrease (see `finetune_training_log.json` for all 105 logged steps).
- **A real bug was found and fixed during this work:** the first training attempt padded every
  example to a fixed length and computed the loss over the padding tokens too, which diluted the
  signal and produced a flat, non-converging loss curve (~7.0–7.5 throughout). Switching to
  `DataCollatorForLanguageModeling` (dynamic padding, loss masked to -100 on padding) fixed this —
  the corrected run is the one reported here.
- **Adapter saved:** `checkpoints/lora_adapter/` (591 KB,
  `adapter_model.safetensors` + `adapter_config.json`).

## Results — format adherence (automatic, exact header match)

| | Baseline (no fine-tune) | Fine-tuned |
|---|---|---|
| Headers found (of 5 required), avg over 6 test prompts | 0.0/5 | 0.0/5 |
| Headers in correct order when present | n/a | n/a |

**The literal 5-header escalation-note format was not learned** with this data/training budget —
neither model reproduced the exact `Headline:` / `Current status:` / ... header strings on any of
the 6 held-out test prompts, using greedy decoding. This is a real negative result, not a bug being
hidden: 14 training examples across 6 unique underlying scenarios was not enough repetition of the
literal header tokens for a rank-8 LoRA adapter on an 82M-parameter model to memorize the exact
format, even though the loss curve shows real learning happened.

## Results — topical relevance (hand-scored, 1–5)

Reading the actual generations (`finetune_comparison_results.csv`), the fine-tuned model did learn
something real: its answers are noticeably more grounded in the specific input topic than the
baseline's generic boilerplate. Hand-scored 1–5 ("does the output address the concrete situation
described, or is it generic filler?"), see `finetune_qualitative_scoring.csv`:

| | Baseline | Fine-tuned |
|---|---|---|
| Average topical relevance (6 test prompts) | 1.83/5 | 3.33/5 |

Example: for "budget is almost gone and we still have 2 months left," the baseline generated
unrelated text about a "2018 product release"; the fine-tuned model generated "the budget has been
delayed... funding will be used to fund further research... not to delay any additional work until
it can meet its goals or exceed their current target date" — clearly on-topic, even without
reproducing the required format. One baseline generation (FT6) also invented an unconfirmed "$1
million" compensation figure — a real hallucination the fine-tuned version did not repeat on the
same prompt.

## RAG vs. fine-tuning — decision

See `results/rag_vs_finetuning_decision.csv` for the full comparison. Conclusion: **RAG remains the
primary approach for this project.** It reached 5.0/5 format adherence with zero training, using
6 documents already on hand. This fine-tuning experiment is real, additional evidence — not just an
assumption — for why: even after a correctly-converging real training run, a small model with a
small hand-authored dataset could not reliably learn an exact output format, while genuinely
improving on a different, related capability (topical grounding). Fine-tuning is documented here as
a real, secondary experiment that supports the original Module 6 decision, not one that overturns
it.

## Limitations, honestly

- 82M-parameter `distilgpt2` and 14 training examples are both far below what a production
  fine-tune would use; this was scoped to fit CPU-only training time for a progress-milestone demo.
- Greedy decoding with no output-length control means some generations ramble or repeat; a stricter
  stopping criterion or a slightly larger model would likely help isolate whether the format failure
  is a data-quantity problem or a model-capacity problem — not yet tested.
- Before the final submission, if this is revisited: more training examples per scenario (aiming for
  literal-string repetition of the header tokens, since that is what greedy decoding needs to
  reliably reproduce) and possibly a slightly larger base model would be the next things to try.
