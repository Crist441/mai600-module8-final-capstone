import json
import os
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(REPO, "results")
IMAGES = os.path.join(REPO, "images")

outputs = pd.read_csv(os.path.join(RESULTS, "generated_outputs.csv"))

# Hand-scored (Claude-Code-assisted, rubric-based, spot-checked) quality dimensions.
# Methodology matches Module 7: same five 1-5 dimensions.
scores = {
    "Q1":  {"groundedness": 5, "format_adherence": 5, "completeness": 5, "helpfulness": 5, "accuracy": 5,
            "observation": "Correct, complete, cited."},
    "Q2":  {"groundedness": 5, "format_adherence": 5, "completeness": 5, "helpfulness": 5, "accuracy": 5,
            "observation": "Correct, all four RACI roles defined, cited."},
    "Q3":  {"groundedness": 5, "format_adherence": 5, "completeness": 5, "helpfulness": 5, "accuracy": 5,
            "observation": "States the decision rule directly -- this was Module 7's weakest question (vague answer); now clear and complete."},
    "Q4":  {"groundedness": 5, "format_adherence": 5, "completeness": 5, "helpfulness": 5, "accuracy": 5,
            "observation": "Correct, complete, cited."},
    "Q5":  {"groundedness": 5, "format_adherence": 5, "completeness": 5, "helpfulness": 5, "accuracy": 5,
            "observation": "All three escalation conditions listed correctly."},
    "Q6":  {"groundedness": 5, "format_adherence": 5, "completeness": 5, "helpfulness": 5, "accuracy": 5,
            "observation": "Five-part structure listed in the correct order."},
    "Q7":  {"groundedness": 3, "format_adherence": 5, "completeness": 1, "helpfulness": 1, "accuracy": 2,
            "observation": "REAL FAILURE: retrieved and cited the correct document, but answered a different question (the document's general purpose) instead of the specific Risk-to-Issue trigger asked about. Retrieval worked; generation did not answer the question."},
    "Q8":  {"groundedness": 5, "format_adherence": 5, "completeness": 5, "helpfulness": 5, "accuracy": 5,
            "observation": "Correctly quotes the first required step."},
    "Q9":  {"groundedness": 5, "format_adherence": 5, "completeness": 5, "helpfulness": 5, "accuracy": 5,
            "observation": "COMPOUND FIX CONFIRMED: retrieved both RAID and RACI chunks (failed at top-2 in Module 7) and correctly explained both, citing both sources by name."},
    "Q10": {"groundedness": 3, "format_adherence": 3, "completeness": 2, "helpfulness": 2, "accuracy": 2,
            "observation": "REAL FAILURE: both expected documents were retrieved, but the answer misapplies the Risk-to-Issue rule (says 'not yet an Issue, since the date has not passed' when the question states the vendor date WAS missed), omits the 10% budget-variance threshold, and the citation line names only one of the two required sources."},
}

for tid, s in scores.items():
    for k, v in s.items():
        outputs.loc[outputs["test_id"] == tid, k] = v

def expected_set(row):
    return set(row["expected_source"].split(";"))

def retrieved_set(row):
    return set(row["retrieved_sources"].split(";"))

outputs["retrieval_hit_top4"] = outputs.apply(lambda r: int(expected_set(r).issubset(retrieved_set(r))), axis=1)
outputs["top1_in_expected"] = outputs.apply(lambda r: int(r["top1_source"] in expected_set(r)), axis=1)

def citation_match(row):
    answer = row["generated_answer"]
    return int(all(src in answer for src in expected_set(row)))

outputs["citation_match"] = outputs.apply(citation_match, axis=1)

eval_cols = [
    "test_id", "question", "question_type", "expected_source", "top1_source",
    "retrieval_hit_top4", "top1_in_expected", "citation_match",
    "groundedness", "format_adherence", "completeness", "helpfulness", "accuracy",
    "response_time_seconds", "observation",
]
evaluation_scores = outputs[eval_cols]
evaluation_scores.to_csv(os.path.join(RESULTS, "evaluation_scores.csv"), index=False)

summary_metrics = {
    "num_tests": int(len(evaluation_scores)),
    "num_single_doc_tests": int((outputs["question_type"] == "single").sum()),
    "num_compound_tests": int((outputs["question_type"] == "compound").sum()),
    "retrieval_hit_rate_top4": round(float(evaluation_scores["retrieval_hit_top4"].mean()), 3),
    "top1_source_match_rate": round(float(evaluation_scores["top1_in_expected"].mean()), 3),
    "citation_match_rate": round(float(evaluation_scores["citation_match"].mean()), 3),
    "avg_groundedness": round(float(evaluation_scores["groundedness"].mean()), 2),
    "avg_format_adherence": round(float(evaluation_scores["format_adherence"].mean()), 2),
    "avg_completeness": round(float(evaluation_scores["completeness"].mean()), 2),
    "avg_helpfulness": round(float(evaluation_scores["helpfulness"].mean()), 2),
    "avg_accuracy": round(float(evaluation_scores["accuracy"].mean()), 2),
    "avg_response_time_s": round(float(outputs["response_time_seconds"].mean()), 2),
    "compound_retrieval_hit_rate": round(float(evaluation_scores.loc[evaluation_scores["question_type"] == "compound", "retrieval_hit_top4"].mean()), 3),
}

with open(os.path.join(RESULTS, "summary_metrics.json"), "w", encoding="utf-8") as f:
    json.dump(summary_metrics, f, indent=2)

print(json.dumps(summary_metrics, indent=2))
print("\nSaved evaluation_scores.csv and summary_metrics.json")
