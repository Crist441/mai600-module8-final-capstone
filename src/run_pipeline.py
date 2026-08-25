import sys, os, time, json, csv

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))

from rag_pipeline import load_chunks, embed, retrieve, build_prompt, generate

KB_DIR = os.path.join(REPO, "data", "sample_documents")
TEST_CASES_PATH = os.path.join(REPO, "data", "test_cases.csv")
RESULTS_DIR = os.path.join(REPO, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

print("Loading chunks...")
chunks = load_chunks(KB_DIR)
print(f"Loaded {len(chunks)} chunks")

print("Embedding chunks...")
t0 = time.time()
for c in chunks:
    c["embedding"] = embed(c["text"])
print(f"Embedded {len(chunks)} chunks in {round(time.time()-t0,2)}s")

# Load test cases
test_cases = []
with open(TEST_CASES_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        test_cases.append(row)
print(f"Loaded {len(test_cases)} test cases")

results = []
retrieval_log_rows = []
benchmark_rows = []

for row in test_cases:
    test_id = row["test_id"]
    question = row["question"]
    print(f"\n=== {test_id} ===")
    t0 = time.time()
    q_emb = embed(question)
    retrieved = retrieve(q_emb, chunks, top_k=4)
    for rank, c in enumerate(retrieved, start=1):
        retrieval_log_rows.append({
            "test_id": test_id,
            "rank": rank,
            "doc_id": c["file"],
            "score": round(float(__import__("rag_pipeline").cos(q_emb, c["embedding"])), 4),
        })
    prompt = build_prompt(question, retrieved)
    gen_start = time.time()
    result = generate(prompt, timeout=240)
    gen_time = round(time.time() - gen_start, 2)
    answer = result.get("response", "")
    total_time = round(time.time() - t0, 2)
    print(f"retrieved: {[c['file'] for c in retrieved]}")
    print(f"gen_time={gen_time}s total_time={total_time}s")
    print(answer[:300])

    results.append({
        "test_id": test_id,
        "question": question,
        "expected_source": row["expected_source"],
        "question_type": row["question_type"],
        "retrieved_sources": ";".join(c["file"] for c in retrieved),
        "top1_source": retrieved[0]["file"],
        "generated_answer": answer,
        "response_time_seconds": gen_time,
    })
    benchmark_rows.append({
        "test_id": test_id,
        "model": "llama3.2:3b",
        "embed_model": "nomic-embed-text",
        "top_k": 4,
        "response_time_seconds": gen_time,
        "total_time_seconds": total_time,
        "answer_length_characters": len(answer),
    })

# Save results
import pandas as pd
outputs_df = pd.DataFrame(results)
outputs_df.to_csv(os.path.join(RESULTS_DIR, "generated_outputs.csv"), index=False)

retrieval_df = pd.DataFrame(retrieval_log_rows)
retrieval_df.to_csv(os.path.join(RESULTS_DIR, "retrieved_chunks.csv"), index=False)

benchmark_df = pd.DataFrame(benchmark_rows)
benchmark_df.to_csv(os.path.join(RESULTS_DIR, "benchmark_results.csv"), index=False)

print("\n\nDone. Saved generated_outputs.csv, retrieved_chunks.csv, benchmark_results.csv")
