from unittest.mock import patch, MagicMock
from benchmarking.utils import wandb_logger


@patch("benchmarking.utils.wandb_logger.wandb")
def test_wandb_logger_init(mock_wandb):
    mock_wandb.init.return_value = MagicMock()

    logger = wandb_logger.WandbLogger(
        project="my-test-project", run_name="test-run", config={"k": 5}
    )

    mock_wandb.init.assert_called_once_with(
        project="my-test-project", name="test-run", config={"k": 5}, reinit=True
    )

    assert logger.run == mock_wandb.init.return_value


@patch("benchmarking.utils.wandb_logger.wandb")
def test_log_mean_metrics(mock_wandb):
    logger = wandb_logger.WandbLogger(project="my-project")
    metrics = {"precision": 0.9, "ndcg": 0.8}

    logger.log_mean_metrics("LuceneModel", metrics)

    mock_wandb.log.assert_called_once_with(
        {"LuceneModel_mean_metrics": {"precision": 0.9, "ndcg": 0.8}}, commit=True
    )


@patch("benchmarking.utils.wandb_logger.wandb")
def test_log_per_query_metrics(mock_wandb):
    mock_table = MagicMock()
    mock_wandb.Table.return_value = mock_table

    logger = wandb_logger.WandbLogger(project="my-project")

    per_query_scores = {
        "q1": {"Precision": 0.8, "NDCG": 0.75},
        "q2": {"Precision": 0.9, "NDCG": 0.85},
    }

    logger.log_per_query_metrics("LuceneModel", per_query_scores)

    expected_columns = ["query_id", "Precision", "NDCG"]
    expected_data = [["q1", 0.8, 0.75], ["q2", 0.9, 0.85]]

    # Check one of the wandb.Table calls had the correct args
    mock_wandb.Table.assert_any_call(columns=expected_columns, data=expected_data)

    # Optionally check how many times it was called
    assert mock_wandb.Table.call_count == 1

    # Check first log was with the full table
    mock_wandb.log.assert_any_call({"LuceneModel/per_query_scores": mock_table})


@patch("benchmarking.utils.wandb_logger.wandb")
def test_finish(mock_wandb):
    logger = wandb_logger.WandbLogger(project="another-project")
    logger.finish()

    mock_wandb.finish.assert_called_once()
