from documents import document_builder
from documents.pdf import pdf_document

class PDFDocumentBuilder(document_builder.DocumentBuilder):
    @staticmethod
    def build(doc_id: str, data: dict[str, str]) -> pdf_document.PDFDocument:
        return pdf_document.PDFDocument(
            doc_id=doc_id,
            page_count=data["page_count"],
            file_name=data["file_name"],
            file_extension=data["file_extension"],
            course_ids=data["course_ids"],
            course_title=data["course_title"],
            admin_code=data["admin_code"],
            content_type=data["content_type"],
            authors=data["lecturers"],
            date_created=data["date_created"],
            subject=data["subject"],
            keywords=data["keywords"],
            source=data["source"],
            version=data["version"],
            pages=data["pages"]
        )
