import hashlib
import pathlib

from data_collection import utils
from data_collection.content_gateways import content_gateway
from data_collection.segments import segmenter

from documents import document_builder, document, document_adapter


class DocumentProcessor:
    """
    Class responsible for processing files into Keats-compatible documents
    using a specific gateway, builder, and transformer.
    """
    def process(
        self,
        file_path: pathlib.Path,
        metadata_entry: dict[str, str],
        gateway: content_gateway.EducationalContentGateway,
        document_builder: document_builder.DocumentBuilder,
        segmenter: segmenter.Segmenter,
        document_adapter: document_adapter.DocumentAdapter
    ) -> list[document.Document]:
        """
        Process a single file into Keats-compatible documents.
        """
        base_name = file_path.stem
        extension = file_path.suffix.lstrip(".").lower()
        course_ids = metadata_entry["course_ids"]
        doc_id = self._generate_doc_id(course_ids=course_ids, base_name=base_name, extension=extension)

        gateway.set_file_path(str(file_path))
        data = gateway.get()

        data["pages"] = segmenter.segment(data=data)

        all_data = {**data, **metadata_entry}

        doc = document_builder.build(doc_id=doc_id, data=all_data)

        result = document_adapter.to_keats(document=doc)
        return result



    def _generate_doc_id(self, course_ids: list[str], base_name: str, extension: str) -> str:
        """Generate a consistent unique ID from course ID and filename."""
        id_string = f"{course_ids}_{base_name}.{extension}"
        return hashlib.sha256(id_string.encode()).hexdigest()
    

    
def process_slides(
        processor: DocumentProcessor,
        courses: pathlib.Path,
        metadata: dict[str, str],
        content_processors: dict,

) -> tuple[list[document.Document], utils.SlideProcessingStats]:
    
    utils.validate_courses(folder=courses, metadata=metadata)
    result = []
    stats = utils.SlideProcessingStats()
    for course in courses.iterdir():

        if not course.is_dir():
            print(f"Skipping non-directory file: {course}")
            continue


        course_info = utils.get_course_info(course.name, metadata)
        course_info = utils.assign_version(course_info=course_info)

        for file in course.iterdir():
            file_extension = file.suffix.lstrip(".").lower()
            stats.append_total()

            if not file_extension:
                print(f"Skipping file with no extension: {file}")
                continue

            stats.record_file(file_extension, course_info["course_ids"])

            content_gateway, document_builder, document_segmenter, document_adapter = content_processors[file_extension]
            docs = processor.process(
                file_path=file,
                metadata_entry=course_info,
                gateway=content_gateway(),
                document_builder=document_builder(),
                segmenter=document_segmenter(),
                document_adapter=document_adapter()
            )
            result.extend(docs)
    return result, stats