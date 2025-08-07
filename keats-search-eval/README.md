## 🛠️ Usage Instructions (Makefile)

Ensure you have Docker installed and working. All commands below should be run from the project root.


###  1. Build the Docker Image

```bash
make build
```

---

### 2. Indexing

**Index all models (Lucene, DPR, ANCE, SPLADE):**

```bash
make index-all
```

You can also run each model’s indexer individually:

```bash
make index-lucene
make index-dpr
make index-ance
make index-splade
```

Unfortunately, due to time constraints and dependency issues, it was not possible to create a reproducible script for generating ColBERT indexes in Docker. However, the precomputed indexes are available here:```keats-search-eval/src/benchmarking/models/colbert```. The main issue was related to importing FAISS alongside Torch in Docker. This issue ```https://github.com/stanford-futuredata/ColBERT/issues/139``` helped resolve the problem locally, but the solution was not portable to the containerized setup in time.

---

### 3. Benchmarking

**Run benchmarking using original indexes:**

```bash
make benchmark
```

**Run benchmarking using test indexes:**

```bash
make benchmark-test
```

This sets the environment variable `USE_TEST_INDEX=true` and uses `index_test` directories.

Final models prediction use for the report can be found here: ```keats-search-eval/fdata/models_predictions```

---

### 4. Evaluation

**Evaluate predictions from the original benchmark:**

```bash
make evaluate EVAL_MODELS="BM25 DPR"
```

**Evaluate predictions from the test benchmark:**

```bash
make evaluate-test EVAL_MODELS="BM25 DPR"
```

You can customize the models using the `EVAL_MODELS` variable (quoted list of class names).

Final results can be found here ```keats-search-eval/fdata/results```

---

### 5. Combined Pipelines

**Run benchmark + evaluation in one go (original index):**

```bash
make benchmark-evaluate EVAL_MODELS="BM25 DPR"
```

**Run full test pipeline (index → benchmark-test → evaluate-test):**

```bash
make test EVAL_MODELS="BM25 DPR"
```

This will:
1. Generate test indexes for all models
2. Run benchmark using test indexes
3. Evaluate the results using test predictions

---

### 6. Annotate with LLM

Final annotation can be found here: ```keats-search-eval/fdata/ground_truth/annotations.jsonl```

**Run annotation using a selected OpenAI model:**

```bash
make annotate
```

Make sure your `OPENAI_API_KEY` is set in your environment or in the Makefile.

---

###  Models

Models implementations along with indexes can be found in ```keats-search-eval/src/benchmarking/models```

---

###  Data Collection

Collected data can be found in 
```keats-search-eval/fdata/dataset```

Documents can be found here: ```keats-search-eval/fdata/ground_truth/documents.json```

The script for data collection are located in ```keats-search-eval/src/data_collection``` Unfortunately, due to time constraints, there is no Makefile command available to run them directly. You can try running locally by installing ```requirements.txt``` and setting propert python path


---

###  Query Generation

Final query collection can be found here: ```keats-search-eval/fdata/ground_truth/queries.csv```

Collected data can be found in 
```keats-search-eval/fdata/dataset```

The script for data collection are located in ```keats-search-eval/src/data_collection``` Unfortunately, due to time constraints, there is no Makefile command available to run them directly. You can try running locally by installing ```requirements.txt``` and setting propert python path

---

###  Query Generation and Annotation Evaluation

Script for annotation and evaluation can be found here: ```keats-search-eval/src/llm_annotation/benchmarking```

Script for query generation and evaluation can be found here: ```keats-search-eval/src/query_generation```

 Unfortunately, due to time constraints, there is no Makefile command available to run them directly. You can try running locally by installing ```requirements.txt``` and setting propert python path

---

# Evaluation Summary

### Rankings for Precision@1 (k=1)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `ColBERT` | 0.7930 |
| 2 | `SPLADE` | 0.7445 |
| 3 | `BM25` | 0.6960 |
| 4 | `ANCE` | 0.6123 |
| 5 | `TFIDF` | 0.5683 |
| 6 | `DPR` | 0.2643 |
| 7 | `Random` | 0.0000 |

### Rankings for NDCG@5 (k=5)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `SPLADE` | 0.6814 |
| 2 | `BM25` | 0.6644 |
| 3 | `ColBERT` | 0.6632 |
| 4 | `ANCE` | 0.5925 |
| 5 | `TFIDF` | 0.5889 |
| 6 | `DPR` | 0.3439 |
| 7 | `Random` | 0.0078 |

### Rankings for NDCG@10 (k=10)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `SPLADE` | 0.5823 |
| 2 | `BM25` | 0.5810 |
| 3 | `ColBERT` | 0.5357 |
| 4 | `TFIDF` | 0.5293 |
| 5 | `ANCE` | 0.5192 |
| 6 | `DPR` | 0.3253 |
| 7 | `Random` | 0.0060 |

### Rankings for MRR@5 (k=5)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `ColBERT` | 0.8529 |
| 2 | `SPLADE` | 0.8236 |
| 3 | `BM25` | 0.7912 |
| 4 | `ANCE` | 0.7091 |
| 5 | `TFIDF` | 0.6739 |
| 6 | `DPR` | 0.3678 |
| 7 | `Random` | 0.0046 |

### Rankings for MRR@10 (k=10)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `ColBERT` | 0.8541 |
| 2 | `SPLADE` | 0.8263 |
| 3 | `BM25` | 0.7971 |
| 4 | `ANCE` | 0.7173 |
| 5 | `TFIDF` | 0.6829 |
| 6 | `DPR` | 0.3811 |
| 7 | `Random` | 0.0046 |
