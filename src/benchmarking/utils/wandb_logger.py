import wandb


class WandbLogger:
    def __init__(self, project: str, run_name: str = None, config: dict = None):
        self.run = wandb.init(
            project=project,
            name=run_name,
            config=config or {},
            reinit=True
        )

    def log_mean_metrics(self, model_name: str, metrics: dict[str, float], step: int = None):
        wandb.log(
            {f"{model_name}_mean_metrics": metrics},
            commit=True
        )


    def log_per_query_metrics(self, model_name: str, per_query_scores: dict[str, dict[str, float]]):
        """
        Logs per-query metrics as a table and logs individual charts for each metric.
        """
        if not per_query_scores:
            return

        # Extract metric names
        metric_names = list(next(iter(per_query_scores.values())).keys())
        query_ids = list(per_query_scores.keys())

        # Create a W&B table for logging raw scores
        columns = ["query_id"] + metric_names
        data = [[qid] + [scores[m] for m in metric_names] for qid, scores in per_query_scores.items()]
        table = wandb.Table(columns=columns, data=data)
        wandb.log({f"{model_name}/per_query_scores": table})

        # Log a separate bar chart for each metric
        for metric_name in metric_names:
            chart_table = wandb.Table(
                data=[[qid, scores[metric_name]] for qid, scores in per_query_scores.items()],
                columns=["query_id", metric_name]
            )

            chart = wandb.plot.bar(
                chart_table,
                "query_id",
                metric_name,
                title=f"{model_name} - {metric_name} per Query"
            )

            wandb.log({f"{model_name}/{metric_name}_bar_chart": chart})





    def finish(self):
        wandb.finish()
