
from benchmarking.metrics import precision, reciprocal_rank, ndcg
from benchmarking.utils import loader, wandb_logger
from evaluator import evaluator

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
    eval = evaluator.Evaluator(metrics)
    logger = wandb_logger.WandbLogger(project="keats-search", run_name="baseline-eval")

    # Run evaluation for each model
    for model in models:
        model_name = model.__class__.__name__
        print(f"\n🔍 Evaluating model: {model.__class__.__name__}")
        results = eval.evaluate(model=model, queries=queries, ground_truth=ground_truth)
        for metric_name, score in results["mean"].items():
            print(f"  {metric_name}: {score:.4f}")

        # Log to wandb
        logger.log_metrics(model_name, results["mean"])

if __name__ == "__main__":
    main()
