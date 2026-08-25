"""RAG pipeline for the Apex Process Solutions PMO Risk Assistant (Module 8 final).

Chunking, embedding, retrieval, and generation, all against a local Ollama
installation. This is the Module 7 pipeline (chunk-by-markdown-section,
nomic-embed-text embeddings, llama3.2:3b generation) widened from top-2 to
top-4 retrieval to fix the compound-question failure documented in Module 7.
"""

import glob
import math
import os
import re

import requests

EMBED_MODEL = "nomic-embed-text"
GEN_MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434"
TOP_K = 4


def chunk_document(text, filename, target_words=200):
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    chunks = []
    for sec in sections:
        sec = sec.strip()
        if sec:
            chunks.append({"file": filename, "text": sec})
    return chunks


def load_chunks(kb_dir):
    all_chunks = []
    for fp in sorted(glob.glob(os.path.join(kb_dir, "*.md"))):
        text = open(fp, encoding="utf-8").read()
        all_chunks.extend(chunk_document(text, os.path.basename(fp)))
    return all_chunks


def embed(text, timeout=30):
    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["embedding"]


def cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)


def retrieve(question_embedding, all_chunks, top_k=TOP_K):
    scored = sorted(all_chunks, key=lambda c: cos(question_embedding, c["embedding"]), reverse=True)
    return scored[:top_k]


def build_prompt(question, retrieved_chunks):
    context = "\n\n---\n\n".join(f"[Source: {c['file']}]\n{c['text']}" for c in retrieved_chunks)
    return (
        'You are a PMO assistant. Answer the question using ONLY the reference passages below. '
        'After your answer, add a line starting with "Grounded in:" naming the source file(s) you used.\n\n'
        f"Reference passages:\n{context}\n\nQuestion:\n{question}\n"
    )


def generate(prompt, timeout=180):
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": GEN_MODEL, "prompt": prompt, "stream": False,
              "options": {"temperature": 0.2, "top_p": 0.8}},
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()
