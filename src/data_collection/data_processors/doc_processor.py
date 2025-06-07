import logging
from data_collection.educational_content_gateways import content_gateway
from data_collection.transformers import transformer
from data_collection.data_processors import data_processor
from entities import content, document
from gateways import doc_gateway
from dataclasses import asdict

class DocumentProcessor(data_processor.DataProcessor):
    def __init__(self, 
                 data: list[dict],
                 import_gateway: content_gateway.EducationalContentGateway, 
                 transformer: transformer.Transformer, 
                 export_gateway: doc_gateway.DocumentGateway,
                 logger: logging.Logger = None
                 ) -> None:
        """
        Args:
            data (list[dict]): List of dictionaries containing file paths and metadata.
            import_gateway (EducationalContentGateway): Gateway to import educational content.
            transformer (Transformer): Transformer to convert segments into documents.
            export_gateway (DocumentGateway): Gateway to export documents.
            logger (logging.Logger, optional): Logger for logging messages. Defaults to None.
        """
        self._data = data
        self._import_gateway = import_gateway
        self._transformer = transformer
        self._export_gateway = export_gateway
        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

    def process(self) -> None:
        """
        Orchestrates the pipeline:
        1. Reads content from the content gateway.
        2. Transforms segments into documents.
        3. Stores the documents via the storage gateway.
        """
        cntnt = self._import()

        docs = self._transform(content=cntnt)

        self._export(documents=docs)

        self._logger.info("Pipeline processing complete.")

    def _import(self) -> list[content.Content]:
        """
        Import content from the import gateway.

        Returns:
            list[content.Content]: List of content segments extracted from the files.
        Raises:
            Exception: If an error occurs during the import process.
        """
        self._logger.info("Importing content from files...")
        result = []
        for idx, file in enumerate(self._data):
            try:
                self._import_gateway.set_file_path(file['file_path'])
                self._import_gateway.set_metadata(file['metadata'])
                file_content = self._import_gateway.get()
                result.extend(file_content)
            except Exception as e:
                self._logger.error(f"Failed to import content from {file['file_path']}: {e}")
                continue
            
            self.log_amount(processed=idx, total=len(self._data))
        self._logger.info(f"Done: Extracted {len(result)} segments from {len(self._data)} files.")
        return result
    
    def _transform(self, content: content.Content) -> document.Document: 
        """
        Transform content segments into documents.

        Args:
            content (list[content.Content]): List of content segments to transform.
        Returns:
            list[content.Document]: List of transformed documents.
        Raises:
            Exception: If an error occurs during the transformation process.
        """
        self._logger.info("Transforming segments into documents...")
        result = []
        for idx, s in enumerate(content):
            try:
                self._transformer.set_content(content=s)
                document = self._transformer.transform()
                result.append(document)

                self.log_amount(processed=idx, total=len(content))

            except Exception as e:
                self._logger.warning(f"Failed to transform segment {s.id}: {e}")
        
        self._logger.info(f"Done: Transformed {len(result)} segments into documents.")
        return result
    

    def _export(self, documents: list[document.Document]) -> None:
        """
        Export documents to the export gateway.

        Args:
            documents (list[content.Document]): List of documents to export.
        Raises:
            Exception: If an error occurs during the export process.
        """
        self._logger.info("Exporting documents to storage...")
        docs_dict = [doc.to_dict() for doc in documents]
        try:
            self._export_gateway.add(documents=docs_dict)
            self._logger.info(f"Inserted {len(docs_dict)} documents into the storage gateway.")
        except Exception as e:
            self._logger.error(f"Failed to export documents: {e}")
        

    def log_amount(self, processed: int, total: int, threshold: int = 10) -> None:
        """
        Log the progress of processing segments.

        Args:
            processed (int): Number of segments processed so far.
            total (int): Total number of segments to process.
            threshold (int, optional): Frequency of logging progress. Defaults to 10.
        Raises:
            ValueError: If threshold is not a positive integer.
        """
        if processed % threshold == 0 or processed == total - 1:
            logging.info(f"Processed {processed + 1}/{total} segments.")