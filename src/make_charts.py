import json
import os
import pandas as pd
import matplotlib.pyplot as plt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(REPO, "results")
IMAGES = os.path.join(REPO, "images")

with open(os.path.join(RESULTS, "summary_metrics.json"), encoding="utf-8") as f:
    m8 = json.load(f)

# Module 8 evaluation chart
chart_data = pd.DataFrame({
    "Metric": ["Retrieval Hit\n(top-4)", "Top-1 Source\nMatch", "Citation\nMatch",
               "Groundedness\n(/5)", "Format\nAdherence (/5)", "Completeness\n(/5)",
               "Helpfulness\n(/5)", "Accuracy\n(/5)"],
    "Score": [
        m8["retrieval_hit_rate_top4"],
        m8["top1_source_match_rate"],
        m8["citation_match_rate"],
        m8["avg_groundedness"] / 5,
        m8["avg_format_adherence"] / 5,
        m8["avg_completeness"] / 5,
        m8["avg_helpfulness"] / 5,
        m8["avg_accuracy"] / 5,
    ],
})

plt.figure(figsize=(10, 5))
bars = plt.bar(chart_data["Metric"], chart_data["Score"], color="#4C72B0")
plt.ylim(0, 1.05)
plt.ylabel("Rate / Normalized Score")
plt.title(f"Module 8 Final Evaluation ({m8['num_tests']} test cases: "
          f"{m8['num_single_doc_tests']} single-doc + {m8['num_compound_tests']} compound)")
plt.xticks(rotation=20, ha="right")
for b, v in zip(bars, chart_data["Score"]):
    plt.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}", ha="center", fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(IMAGES, "evaluation_chart.png"), dpi=150)
plt.close()
print("Saved evaluation_chart.png")

# Improvement comparison chart: Module 7 (6 easy Qs) vs Module 8 (10 Qs incl. compound)
m7 = {
    "retrieval_hit_rate": 1.0,
    "citation_match_rate": 1.0,
    "avg_groundedness": 4.83,
    "avg_format_adherence": 5.0,
    "avg_completeness": 4.0,
    "avg_helpfulness": 4.33,
    "avg_accuracy": 4.67,
}
labels = ["Retrieval\nHit Rate", "Citation\nMatch", "Groundedness\n(/5)",
          "Format\nAdherence (/5)", "Completeness\n(/5)", "Helpfulness\n(/5)", "Accuracy\n(/5)"]
m7_vals = [m7["retrieval_hit_rate"], m7["citation_match_rate"],
           m7["avg_groundedness"] / 5, m7["avg_format_adherence"] / 5,
           m7["avg_completeness"] / 5, m7["avg_helpfulness"] / 5, m7["avg_accuracy"] / 5]
m8_vals = [m8["retrieval_hit_rate_top4"], m8["citation_match_rate"],
           m8["avg_groundedness"] / 5, m8["avg_format_adherence"] / 5,
           m8["avg_completeness"] / 5, m8["avg_helpfulness"] / 5, m8["avg_accuracy"] / 5]

import numpy as np
x = np.arange(len(labels))
width = 0.35
plt.figure(figsize=(11, 5.5))
plt.bar(x - width / 2, m7_vals, width, label="Module 7 (6 easy, single-doc Qs)", color="#8C8C8C")
plt.bar(x + width / 2, m8_vals, width, label="Module 8 (10 Qs, incl. 2 compound)", color="#C44E52")
plt.ylim(0, 1.15)
plt.ylabel("Rate / Normalized Score")
plt.title("Module 7 Prototype vs. Module 8 Final -- Harder, Larger Test Set")
plt.xticks(x, labels, rotation=15, ha="right")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGES, "improvement_chart.png"), dpi=150)
plt.close()
print("Saved improvement_chart.png")
