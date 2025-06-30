from unittest.mock import patch, MagicMock
from benchmarking.utils import wandb_logger 


@patch("benchmarking.utils.wandb_logger.wandb")
def test_wandb_logger_init(mock_wandb):
    mock_wandb.init.return_value = MagicMock()

    logger = wandb_logger.WandbLogger(project="my-test-project", run_name="test-run", config={"k": 5})

    mock_wandb.init.assert_called_once_with(
        project="my-test-project",
        name="test-run",
        config={"k": 5},
        reinit=True
    )

    assert logger.run == mock_wandb.init.return_value


@patch("benchmarking.utils.wandb_logger.wandb")
def test_wandb_logger_log_metrics(mock_wandb):
    logger = wandb_logger.WandbLogger(project="my-project")
    metrics = {"precision": 0.9, "ndcg": 0.8}

    logger.log_metrics("LuceneModel", metrics, step=1)

    mock_wandb.log.assert_called_once_with(
        {"LuceneModel/precision": 0.9, "LuceneModel/ndcg": 0.8},
        step=1
    )


@patch("benchmarking.utils.wandb_logger.wandb")
def test_wandb_logger_finish(mock_wandb):
    logger = wandb_logger.WandbLogger(project="another-project")
    logger.finish()

    mock_wandb.finish.assert_called_once()
