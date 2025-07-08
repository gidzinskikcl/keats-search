# Evaluation Summary

## Ground Truth Annotated Evaluation

### Rankings for Precision@1 (k=1)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `lmjelinekmercersearchengine_lambda_0.3` | 0.5330 |
| 2 | `lmjelinekmercersearchengine_lambda_0.5` | 0.5286 |
| 3 | `BM25SearchEngine` | 0.4846 |
| 4 | `lmjelinekmercersearchengine_lambda_0.7` | 0.4846 |
| 5 | `lmjelinekmercersearchengine_lambda_0.1` | 0.4758 |
| 6 | `dirichletsearchengine_mu_500` | 0.4581 |
| 7 | `lmjelinekmercersearchengine_lambda_0.9` | 0.4141 |
| 8 | `TFIDFSearchEngine` | 0.4053 |
| 9 | `dirichletsearchengine_mu_1000` | 0.4009 |
| 10 | `dirichletsearchengine_mu_1500` | 0.3833 |
| 11 | `dirichletsearchengine_mu_2000` | 0.3744 |
| 12 | `BooleanSearchEngine` | 0.2159 |
| 13 | `RandomSearchEngine` | 0.0044 |

### Rankings for MRR@5 (k=5)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `lmjelinekmercersearchengine_lambda_0.5` | 0.6366 |
| 2 | `lmjelinekmercersearchengine_lambda_0.3` | 0.6325 |
| 3 | `lmjelinekmercersearchengine_lambda_0.7` | 0.6128 |
| 4 | `BM25SearchEngine` | 0.6087 |
| 5 | `dirichletsearchengine_mu_500` | 0.5843 |
| 6 | `lmjelinekmercersearchengine_lambda_0.1` | 0.5811 |
| 7 | `lmjelinekmercersearchengine_lambda_0.9` | 0.5426 |
| 8 | `dirichletsearchengine_mu_1000` | 0.5424 |
| 9 | `TFIDFSearchEngine` | 0.5233 |
| 10 | `dirichletsearchengine_mu_1500` | 0.5160 |
| 11 | `dirichletsearchengine_mu_2000` | 0.5035 |
| 12 | `BooleanSearchEngine` | 0.3203 |
| 13 | `RandomSearchEngine` | 0.0059 |

### Rankings for MRR@10 (k=10)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `lmjelinekmercersearchengine_lambda_0.5` | 0.6451 |
| 2 | `lmjelinekmercersearchengine_lambda_0.3` | 0.6410 |
| 3 | `lmjelinekmercersearchengine_lambda_0.7` | 0.6201 |
| 4 | `BM25SearchEngine` | 0.6181 |
| 5 | `dirichletsearchengine_mu_500` | 0.5929 |
| 6 | `lmjelinekmercersearchengine_lambda_0.1` | 0.5899 |
| 7 | `lmjelinekmercersearchengine_lambda_0.9` | 0.5562 |
| 8 | `dirichletsearchengine_mu_1000` | 0.5511 |
| 9 | `TFIDFSearchEngine` | 0.5349 |
| 10 | `dirichletsearchengine_mu_1500` | 0.5288 |
| 11 | `dirichletsearchengine_mu_2000` | 0.5144 |
| 12 | `BooleanSearchEngine` | 0.3320 |
| 13 | `RandomSearchEngine` | 0.0071 |

---
## LLM-Annotated Evaluation

### Rankings for Precision@5 (k=5)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `bm25` | 0.3815 |

### Rankings for MRR@5 (k=5)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `bm25` | 0.7912 |

### Rankings for NDCG@5 (k=5)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `bm25` | 0.6644 |

### Rankings for Precision@10 (k=10)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `bm25` | 0.2621 |

### Rankings for MRR@10 (k=10)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `bm25` | 0.7971 |

### Rankings for NDCG@10 (k=10)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `bm25` | 0.5810 |
