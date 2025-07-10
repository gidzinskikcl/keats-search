# Evaluation Summary

## Ground Truth Annotated Evaluation

### Rankings for Precision@1 (k=1)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `SpladeSearchEngine` | 0.5595 |
| 2 | `lmjelinekmercersearchengine_lambda_0.3` | 0.5330 |
| 3 | `lmjelinekmercersearchengine_lambda_0.5` | 0.5286 |
| 4 | `BM25SearchEngine` | 0.4846 |
| 5 | `lmjelinekmercersearchengine_lambda_0.7` | 0.4846 |
| 6 | `lmjelinekmercersearchengine_lambda_0.1` | 0.4758 |
| 7 | `dirichletsearchengine_mu_500` | 0.4581 |
| 8 | `lmjelinekmercersearchengine_lambda_0.9` | 0.4141 |
| 9 | `TFIDFSearchEngine` | 0.4053 |
| 10 | `dirichletsearchengine_mu_1000` | 0.4009 |
| 11 | `dirichletsearchengine_mu_1500` | 0.3833 |
| 12 | `dirichletsearchengine_mu_2000` | 0.3744 |
| 13 | `BooleanSearchEngine` | 0.2159 |
| 14 | `RandomSearchEngine` | 0.0044 |

### Rankings for MRR@5 (k=5)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `SpladeSearchEngine` | 0.6576 |
| 2 | `lmjelinekmercersearchengine_lambda_0.5` | 0.6366 |
| 3 | `lmjelinekmercersearchengine_lambda_0.3` | 0.6325 |
| 4 | `lmjelinekmercersearchengine_lambda_0.7` | 0.6128 |
| 5 | `BM25SearchEngine` | 0.6087 |
| 6 | `dirichletsearchengine_mu_500` | 0.5843 |
| 7 | `lmjelinekmercersearchengine_lambda_0.1` | 0.5811 |
| 8 | `lmjelinekmercersearchengine_lambda_0.9` | 0.5426 |
| 9 | `dirichletsearchengine_mu_1000` | 0.5424 |
| 10 | `TFIDFSearchEngine` | 0.5233 |
| 11 | `dirichletsearchengine_mu_1500` | 0.5160 |
| 12 | `dirichletsearchengine_mu_2000` | 0.5035 |
| 13 | `BooleanSearchEngine` | 0.3203 |
| 14 | `RandomSearchEngine` | 0.0059 |

### Rankings for MRR@10 (k=10)

| Rank | Model Name | Score |
|------|-------------|--------|
| 1 | `SpladeSearchEngine` | 0.6657 |
| 2 | `lmjelinekmercersearchengine_lambda_0.5` | 0.6451 |
| 3 | `lmjelinekmercersearchengine_lambda_0.3` | 0.6410 |
| 4 | `lmjelinekmercersearchengine_lambda_0.7` | 0.6201 |
| 5 | `BM25SearchEngine` | 0.6181 |
| 6 | `dirichletsearchengine_mu_500` | 0.5929 |
| 7 | `lmjelinekmercersearchengine_lambda_0.1` | 0.5899 |
| 8 | `lmjelinekmercersearchengine_lambda_0.9` | 0.5562 |
| 9 | `dirichletsearchengine_mu_1000` | 0.5511 |
| 10 | `TFIDFSearchEngine` | 0.5349 |
| 11 | `dirichletsearchengine_mu_1500` | 0.5288 |
| 12 | `dirichletsearchengine_mu_2000` | 0.5144 |
| 13 | `BooleanSearchEngine` | 0.3320 |
| 14 | `RandomSearchEngine` | 0.0071 |

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
