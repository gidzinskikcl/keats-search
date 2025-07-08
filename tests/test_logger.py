import logging
import logger as logger_


def test_get_logger(caplog):
    logger_name = "test_logger"
    logger = logger_.get_logger(logger_name)

    # Ensure it's the right logger
    assert logger.name == logger_name
    assert logger.level == logging.INFO

    # Logger should have a StreamHandler
    stream_handlers = [
        h for h in logger.handlers if isinstance(h, logging.StreamHandler)
    ]
    assert len(stream_handlers) == 1

    # Log a message
    with caplog.at_level(logging.INFO, logger=logger_name):
        logger.info("Hello from logger test!")

    # Assert the log message was captured
    assert any("Hello from logger test!" in record.message for record in caplog.records)
    assert any(record.levelname == "INFO" for record in caplog.records)
    assert any(record.name == logger_name for record in caplog.records)


def test_github():
    assert 1 == 0