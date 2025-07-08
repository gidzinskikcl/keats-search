import os
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    LUCENE_JAR_PATH: str
    INDEX_DIR: str
    DOC_PATH: str
    TOP_K: int = 10

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")

settings = AppConfig()