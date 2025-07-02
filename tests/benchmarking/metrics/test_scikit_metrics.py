import unittest

# Minimal mock Document class
class Document:
    def __init__(self, doc_id):
        self.doc_id = doc_id

# Your metric classes
class PrecisionAtK:
    def __init__(self, k: int):
        self.k = k
        self.name = f"Precision@{k}"

    def compute(self, query_id: str, retrieved_docs: list, relevant_pairs: set[tuple[str, str]]) -> float:
        if self.k == 0:
            return None
        top_k_docs = retrieved_docs[:self.k]
        if not top_k_docs:
            return 0.0
        y_true = [1 if (query_id, doc.doc_id) in relevant_pairs else 0 for doc in top_k_docs]
        y_pred = [1] * len(y_true)
        if sum(y_true) == 0:
            return 0.0
        return sum(y_true) / len(y_true)  # manual precision computation


class MRRAtK:
    def __init__(self, k: int):
        self.k = k
        self.name = f"MRR@{k}"

    def compute(self, query_id: str, retrieved_docs: list, relevant_pairs: set[tuple[str, str]]) -> float:
        top_k_docs = retrieved_docs[:self.k]
        for rank, doc in enumerate(top_k_docs, start=1):
            if (query_id, doc.doc_id) in relevant_pairs:
                return 1.0 / rank
        return 0.0

# Unit tests (manual expected values)
class TestIRMetrics(unittest.TestCase):

    def setUp(self):
        self.query_id = "Q1"
        self.relevant_pairs = {
            ("Q1", "D1"),
            ("Q1", "D3")
        }
        self.retrieved_docs = [
            Document("D1"),  # relevant
            Document("D2"),  # not relevant
            Document("D3"),  # relevant
            Document("D4"),
            Document("D5")
        ]

    # ------------------ PrecisionAtK ------------------

    def test_precision_at_k_1(self):
        metric = PrecisionAtK(k=1)
        result = metric.compute(self.query_id, self.retrieved_docs, self.relevant_pairs)
        expected = 1.0  # D1 is relevant
        self.assertAlmostEqual(result, expected)

    def test_precision_at_k_3(self):
        metric = PrecisionAtK(k=3)
        result = metric.compute(self.query_id, self.retrieved_docs, self.relevant_pairs)
        # Relevant: D1, D3 → 2 relevant / 3 total
        expected = 2 / 3
        self.assertAlmostEqual(result, expected)

    def test_precision_at_k_5(self):
        metric = PrecisionAtK(k=5)
        result = metric.compute(self.query_id, self.retrieved_docs, self.relevant_pairs)
        # Relevant: D1, D3 → 2/5
        expected = 0.4
        self.assertAlmostEqual(result, expected)

    def test_precision_with_no_relevant_docs(self):
        metric = PrecisionAtK(k=5)
        result = metric.compute("Q2", self.retrieved_docs, self.relevant_pairs)
        expected = 0.0
        self.assertEqual(result, expected)

    def test_precision_at_k_zero(self):
        metric = PrecisionAtK(k=0)
        result = metric.compute(self.query_id, self.retrieved_docs, self.relevant_pairs)
        self.assertIsNone(result)

    # ------------------ MRRAtK ------------------

    def test_mrr_at_k_1(self):
        metric = MRRAtK(k=1)
        result = metric.compute(self.query_id, self.retrieved_docs, self.relevant_pairs)
        expected = 1.0  # D1 is at rank 1
        self.assertAlmostEqual(result, expected)

    def test_mrr_at_k_3(self):
        metric = MRRAtK(k=3)
        result = metric.compute(self.query_id, self.retrieved_docs, self.relevant_pairs)
        expected = 1.0  # D1 is at rank 1
        self.assertAlmostEqual(result, expected)

    def test_mrr_at_k_5_relevant_late(self):
        reordered = [
            Document("D2"),  # not
            Document("D4"),  # not
            Document("D3"),  # relevant ← at rank 3
            Document("D5"),
            Document("D1")   # relevant ← at rank 5 (ignored because D3 is earlier)
        ]
        metric = MRRAtK(k=5)
        result = metric.compute(self.query_id, reordered, self.relevant_pairs)
        expected = 1.0 / 3  # First relevant is D3
        self.assertAlmostEqual(result, expected)

    def test_mrr_with_no_relevant_docs(self):
        metric = MRRAtK(k=5)
        result = metric.compute("Q2", self.retrieved_docs, self.relevant_pairs)
        expected = 0.0
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
