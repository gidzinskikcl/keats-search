import subprocess
import shutil
from pathlib import Path

import config
import logger as api_logger
from core import indexer

class LuceneIndexer(indexer.DocumentIndexer):
    """
    Handles document indexing by invoking the Lucene-based Java indexer.
    """ 

    def __init__(self, index_dir: str =  config.settings.INDEX_DIR, json_doc_path: str =  config.settings.DOC_PATH):
        self.index_dir = index_dir
        self.json_doc_path = json_doc_path
        self.logger = api_logger.get_logger(self.__class__.__name__)
        self.JAR_PATH =  config.settings.LUCENE_JAR_PATH

    def index(self):
        if not Path(self.json_doc_path).exists():
            raise FileNotFoundError(f"Document file does not exist: {self.json_doc_path}")
        
        index_path = Path(self.index_dir)
        if index_path.exists():
            shutil.rmtree(index_path) 

        self.logger.info(f"Starting indexing: {self.json_doc_path} → {self.index_dir}")

        proc = subprocess.run(
            [
                "java",
                "-jar", self.JAR_PATH,
                "--mode", "index",
                self.json_doc_path,
                self.index_dir
            ],
            capture_output=True,
            text=True
        )

        if proc.returncode != 0:
            self.logger.error(f"Indexing failed: {proc.stderr.strip()}")
            raise RuntimeError(f"Indexing failed: {proc.stderr.strip()}")

        self.logger.info("Indexing complete.")