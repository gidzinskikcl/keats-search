
from benchmarking.metrics import precision, reciprocal_rank, ndcg
from benchmarking.utils import loader
from evaluator.evaluator import Evaluator

def main():
    # Load data
    queries = loader.load_queries(path="data/queries.json")
    ground_truth = loader.load_ground_truth("data/ground_truth.json")

    # Define models
    models = [
        # TFIDFModel(),
        # BM25Model(),
        # EmbeddingModel()
    ]

    # Define metrics
    metrics = [
        precision.Precision(k=5),
        reciprocal_rank.ReciprocalRank(),
        ndcg.NDCG(k=5),
    ]

    # Initialize evaluator
    evaluator = Evaluator(metrics)

    # Run evaluation for each model
    for model in models:
        print(f"\n🔍 Evaluating model: {model.__class__.__name__}")
        results = evaluator.evaluate(model=model, queries=queries, ground_truth=ground_truth)
        for metric_name, score in results["mean"].items():
            print(f"  {metric_name}: {score:.4f}")

if __name__ == "__main__":
    main()
