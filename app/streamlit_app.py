"""Streamlit demo app for the Module 8 final capstone.

A simple chat-style interface over the real RAG pipeline in src/rag_pipeline.py --
same chunking, embedding, retrieval, and generation used to produce results/.
No fabricated logic here: every answer shown is a real call to the local Ollama API.
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from rag_pipeline import load_chunks, embed, retrieve, build_prompt, generate

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_DIR = os.path.join(REPO, "data", "sample_documents")

st.set_page_config(page_title="Apex Process Solutions -- PMO Risk Assistant", layout="wide")
st.title("Apex Process Solutions -- PMO Risk Assistant")
st.caption("MAI 600 Module 8 final capstone -- local RAG-grounded PMO risk governance assistant")
st.warning(
    "Classroom prototype -- outputs are grounded in fictional policy documents and must be "
    "reviewed by a human PM before being acted on. Not validated for real production use."
)


@st.cache_resource(show_spinner="Loading and embedding the PMO knowledge base...")
def load_knowledge_base():
    chunks = load_chunks(KB_DIR)
    for c in chunks:
        c["embedding"] = embed(c["text"])
    return chunks


with st.sidebar:
    st.subheader("Knowledge base")
    st.write("10 fictional PMO governance documents (Apex Process Solutions):")
    for fname in sorted(os.listdir(KB_DIR)):
        st.write(f"- {fname}")
    st.subheader("Pipeline")
    st.write("nomic-embed-text (embeddings) + llama3.2:3b (generation), both local via Ollama")
    top_k = st.slider("Retrieval top-k", min_value=1, max_value=6, value=4)

sample_questions = [
    "What is a RAID log and what do its four letters stand for?",
    "A team member says the RAID log and the RACI matrix are basically the same tracking tool. Explain what is different between them.",
    "A vendor missed a delivery date and the resulting rework cost pushed the project over budget. How should this be logged and escalated?",
]

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

cols = st.columns(3)
for i, sq in enumerate(sample_questions):
    if cols[i].button(f"Try example {i + 1}", use_container_width=True):
        st.session_state.question_input = sq
        st.rerun()

question = st.text_area(
    "Ask a PMO risk-governance question",
    height=100,
    placeholder="e.g. When must a risk be escalated to the weekly PMO steering review?",
    key="question_input",
)

if st.button("Ask the assistant", type="primary") and question:
    chunks = load_knowledge_base()
    with st.spinner("Retrieving context and generating a grounded answer (can take 30-70s on CPU)..."):
        q_emb = embed(question)
        retrieved = retrieve(q_emb, chunks, top_k=top_k)
        prompt = build_prompt(question, retrieved)
        result = generate(prompt)
        answer = result.get("response", "")

    st.subheader("Answer")
    st.write(answer)

    st.subheader(f"Retrieved sources (top-{top_k})")
    seen = []
    for c in retrieved:
        if c["file"] not in seen:
            seen.append(c["file"])
    for fname in seen:
        st.write(f"- `{fname}`")

    with st.expander("Show retrieved passages used as context"):
        for c in retrieved:
            st.markdown(f"**{c['file']}**")
            st.text(c["text"])
            st.divider()

st.divider()
st.caption(
    "Source: src/rag_pipeline.py | Evaluation: results/evaluation_scores.csv | "
    "AI usage: ai_usage_disclosure.md"
)
