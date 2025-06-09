import yaml

import logging
import pathlib
import sys

# Add the parent of src (the project root)
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
# from data.testing.metadata import slides_metadata
from data.slides.metadata import slides_metadata
from data_collection import document_processor, utils
from data_collection.content_gateways import pdf_gateway, ppt_gateway
from data_collection.segments import slides_segmenter
from documents import document, document_adapter
from documents.pdf import pdf_document_builder
from documents.ppt import ppt_document_builder
from gateways import mongodb_gateway


def configure_logging():
    """
    Configure logging for the entire application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )

def load_config(config_file: str) -> dict:
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


COURSES = pathlib.Path("/Users/piotrgidzinski/KeatsSearch_workspace/data/courses/lecture_slides")
# COURSES = pathlib.Path("/Users/piotrgidzinski/KeatsSearch_workspace/data/courses/test")
METADATA = slides_metadata.METADATA

# Define a mapping of file extensions to their gateways and document classes
CONTENT_PROCESSORS = {
    "pdf": (
        pdf_gateway.PDFGateway, 
        pdf_document_builder.PDFDocumentBuilder, 
        slides_segmenter.SlidesSegmenter,
        document_adapter.DocumentAdapter
    ),
    "pptx": (
        ppt_gateway.PPTGateway, 
        ppt_document_builder.PPTDocumentBuilder, 
        slides_segmenter.SlidesSegmenter,
        document_adapter.DocumentAdapter
    ),
}

def main():
    # STATS ARE WRONG
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting data processing pipeline.")
    
    # For now the process work for slides only
    processor = document_processor.DocumentProcessor()

    logger.info("Processing slides, this might take couple of seconds...")
    # SLIDES
    slides_documents, stats = document_processor.process_slides(
        processor=processor,
        courses=COURSES,
        metadata=METADATA,
        content_processors=CONTENT_PROCESSORS
    )

    logger.info("Data processing complete!")
    logger.info(f"Processed {len(slides_documents)} documents.")
    stats.log_summary(logger)

    # EXPORT
    logger.info("Initialising Mongo Database...")

    config = load_config("config.yaml")
    export_gateway = mongodb_gateway.MongoDBGateway(
        database_name=config["mongodbKeats"]["database"],
        collection_name=config["mongodbKeats"]["collection"]["documents"],
        uri=config["mongodbKeats"]["uri"]
    )

    logger.info("Exporting documents to storage...")

    docs_dict = document.to_dict(docs=slides_documents)

    try:
        export_gateway.add(documents=docs_dict)
        logger.info(f"Inserted {len(docs_dict)} documents into MongoDB.")
    except Exception as e:
        logger.error(f"Failed to export documents: {e}")

    logger.info("Data processing complete!")


    # STATS
    logger.info("Exporting stats...")
    stats_gateway = mongodb_gateway.MongoDBGateway(
        database_name=config["mongodbKeats"]["database"],
        collection_name=config["mongodbKeats"]["collection"]["stats"],
        uri=config["mongodbKeats"]["uri"]
    )

    stats_doc = stats.summarize()
    stats_doc["run_id"] = utils.generate_run_id()

    try:
        stats_gateway.add(documents=[stats_doc])
        logger.info(f"Inserted stats document into the MongoDB.")
    except Exception as e:
        logger.error(f"Failed to export stats: {e}")

    logger.info("Done!")


if __name__ == "__main__":
    main()


