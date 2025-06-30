import wandb


class WandbLogger:
    def __init__(self, project: str, run_name: str = None, config: dict = None):
        self.run = wandb.init(
            project=project,
            name=run_name,
            config=config or {},
            reinit=True
        )

    def log_metrics(self, model_name: str, metrics: dict[str, float], step: int = None):
        wandb.log({f"{model_name}/{k}": v for k, v in metrics.items()}, step=step)

    def finish(self):
        wandb.finish()
