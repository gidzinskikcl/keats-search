import torch
from transformers import AutoTokenizer
from splade.models import transformer_rep
from collections import defaultdict
import numpy as np
from tqdm import tqdm
import time

# ==== DEFINE QUERY AND DOCUMENTS OUTSIDE MAIN ====

QUERY = "what is backpropagation in neural networks?"

DOCUMENTS = [
    {
        "id": "doc1",
        "text": "Backpropagation is a training algorithm for neural networks.",
    },
    {"id": "doc2", "text": "Convolutional networks are used in computer vision."},
    {"id": "doc3", "text": "Backpropagation uses gradients to update weights."},
    {"id": "doc4", "text": "The capital of France is Paris."},
]

MODEL_NAME = "naver/splade-cocondenser-ensembledistil"

# =======================


def encode_texts(tokenizer, model, texts, is_query=False):
    encoded = []
    for text in tqdm(texts):
        tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            rep = model(**{"q_kwargs" if is_query else "d_kwargs": tokens})[
                "q_rep" if is_query else "d_rep"
            ]
        encoded.append(rep.squeeze())
    return encoded


def sparse_dot_product(query_vec, doc_vecs):
    scores = []
    for doc_vec in doc_vecs:
        score = (query_vec * doc_vec).sum().item()
        scores.append(score)
    return scores


def main():
    start = time.time()
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = transformer_rep.Splade(MODEL_NAME, agg="max", fp16=False)
    model.eval()
    print(f"Model loaded in {time.time() - start:.2f}s")

    # === Encode documents ===
    start = time.time()
    doc_texts = [doc["text"] for doc in DOCUMENTS]
    doc_ids = [doc["id"] for doc in DOCUMENTS]
    doc_vecs = encode_texts(tokenizer, model, doc_texts, is_query=False)
    print(f"Documents encoded in {time.time() - start:.2f}s")

    # === Encode query ===
    start = time.time()
    query_vec = encode_texts(tokenizer, model, [QUERY], is_query=True)[0]
    print(f"Query encoded in {time.time() - start:.2f}s")

    # === Compute scores ===
    start = time.time()
    scores = sparse_dot_product(query_vec, doc_vecs)
    results = sorted(zip(doc_ids, scores), key=lambda x: x[1], reverse=True)
    print(f"Scoring and ranking done in {time.time() - start:.2f}s")

    # === Print results ===
    print(f"\nTop results for query: '{QUERY}'\n")
    for doc_id, score in results:
        print(f"{doc_id}: {score:.4f}")


if __name__ == "__main__":
    main()
