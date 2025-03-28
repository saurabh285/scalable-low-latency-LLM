import faiss
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Paths
KB_PATH = "data/knowledge_base.json"
FAISS_PATH = "data/faiss_index.idx"

# Load or initialize knowledge base
if os.path.exists(KB_PATH):
    with open(KB_PATH, "r") as f:
        knowledge_base = json.load(f)
else:
    knowledge_base = []

# Load or create FAISS index
def get_index():
    if os.path.exists(FAISS_PATH):
        return faiss.read_index(FAISS_PATH)
    else:
        return faiss.IndexFlatL2(384)

index = get_index()

# Build index if empty
if index.ntotal == 0 and knowledge_base:
    questions = [item["question"] for item in knowledge_base]
    embeddings = model.encode(questions)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, FAISS_PATH)

def search_faiss(query: str, threshold=0.4):
    """Returns best-matching answer from knowledge base using FAISS"""
    if index.ntotal == 0:
        return None

    query_vector = model.encode([query])
    D, I = index.search(np.array(query_vector).astype("float32"), k=1)

    distance = D[0][0]
    idx = I[0][0]

    if distance < threshold:
        return knowledge_base[idx]["answer"]
    return None

def add_to_knowledge_base(question: str, answer: str):
    """Adds a new QnA to knowledge base, Redis, and FAISS"""
    # 1. Update knowledge base file
    knowledge_base.append({"question": question, "answer": answer})
    with open(KB_PATH, "w") as f:
        json.dump(knowledge_base, f, indent=2)

    # 2. Update FAISS
    embedding = model.encode([question])
    index.add(np.array(embedding).astype("float32"))
    faiss.write_index(index, FAISS_PATH)
