import wandb


class WandbLogger:
    def __init__(self, project: str, run_name: str = None, config: dict = None):
        self.run = wandb.init(
            project=project, name=run_name, config=config or {}, reinit=True
        )

    def log_mean_metrics(
        self, model_name: str, metrics: dict[str, float], step: int = None
    ):
        wandb.log({f"{model_name}_mean_metrics": metrics}, commit=True)

    def log_per_query_metrics(
        self, model_name: str, per_query_scores: dict[str, dict[str, float]]
    ):
        """
        Logs per-query metrics as a table.
        """
        if not per_query_scores:
            return

        metric_names = list(next(iter(per_query_scores.values())).keys())

        # Create a W&B table for logging raw scores
        columns = ["query_id"] + metric_names
        data = [
            [qid] + [scores[m] for m in metric_names]
            for qid, scores in per_query_scores.items()
        ]
        table = wandb.Table(columns=columns, data=data)
        wandb.log({f"{model_name}/per_query_scores": table})

    def finish(self):
        wandb.finish()
