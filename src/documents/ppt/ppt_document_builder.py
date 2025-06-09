from documents import document_builder
from documents.ppt import ppt_document


class PPTDocumentBuilder(document_builder.DocumentBuilder):
    @staticmethod
    def build(doc_id: str, data: dict[str, str]) -> ppt_document.PPTDocument:
        return ppt_document.PPTDocument(
            doc_id=doc_id,
            doc_title=data["doc_title"],
            page_count=data["page_count"],
            file_name=data["file_name"],
            file_extension=data["file_extension"],
            course_ids=data["course_ids"],
            course_title=data["course_title"],
            admin_code=data["admin_code"],
            content_type=data["content_type"],
            subject=data["subject"],
            authors=data["lecturers"],
            keywords=data["keywords"],
            comments=data["comments"],
            last_modified_by=data["last_modified_by"],
            revision=data["revision"],
            created=data["created"],
            modified=data["modified"],
            category=data["category"],
            content_status=data["content_status"],
            identifier=data["identifier"],
            language=data["language"],
            version=data["version"],
            source=data["source"],
            pages=data["pages"]
        )
