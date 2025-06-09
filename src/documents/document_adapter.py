import hashlib

from documents import document
from documents.pdf import pdf_document
from documents.ppt import ppt_document
from documents.keats import keats_document

class DocumentAdapter:
    @staticmethod
    def to_dict(document) -> list[dict[str, str]]:
        """
        Converts any supported document to a common dictionary representation.
        """
        if isinstance(document, pdf_document.PDFDocument):
            return DocumentAdapter._pdf_to_dict(document)
        elif isinstance(document, ppt_document.PPTDocument):
            return DocumentAdapter._ppt_to_dict(document)
        else:
            raise ValueError(f"Unsupported document type: {type(document)}")

    @staticmethod
    def _pdf_to_dict(pdf_doc: pdf_document.PDFDocument) -> list[dict[str, str]]:
        results = []
        for idx, seg in enumerate(pdf_doc.pages, start=1):
            results.append(
                {
                    "parent_file_id": pdf_doc.doc_id,
                    "parent_file_name": pdf_doc.file_name,
                    "segment_nr": str(idx),
                    "file_type": pdf_doc.file_extension,
                    "course_ids": pdf_doc.course_ids,
                    "course_title": pdf_doc.course_title,
                    "admin_code": pdf_doc.admin_code,
                    "content_type": pdf_doc.content_type,
                    "length": pdf_doc.page_count,
                    "speakers": pdf_doc.authors,
                    "date_created": pdf_doc.date_created,
                    "source": pdf_doc.source,
                    "subject": pdf_doc.subject,
                    "keywords": pdf_doc.keywords,
                    "version": pdf_doc.version,
                    "text": seg.content,
                    "doc_title": "",
                    "start_time": "",
                    "end_time": "",
                    "url": "",
                    "date": "",
                    "description": "",
                    "notes": "",
                }
            )
        return results

    @staticmethod
    def _ppt_to_dict(ppt_doc: ppt_document.PPTDocument) -> list[dict[str, str]]:
        results = []
        for idx, seg in enumerate(ppt_doc.pages, start=1):
            results.append(
                {
                    "parent_file_id": ppt_doc.doc_id, 
                    "parent_file_name": ppt_doc.file_name,
                    "segment_nr": str(idx),
                    "file_type": ppt_doc.file_extension,
                    "doc_title": ppt_doc.doc_title,
                    "course_ids": ppt_doc.course_ids,
                    "course_title": ppt_doc.course_title,
                    "admin_code": ppt_doc.admin_code,
                    "content_type": ppt_doc.content_type,
                    "length": ppt_doc.page_count,
                    "speakers": ppt_doc.authors,
                    "created": ppt_doc.created, 
                    "modified": ppt_doc.modified,
                    "last_modified_by": ppt_doc.last_modified_by,
                    "source": ppt_doc.source,
                    "subject": ppt_doc.subject,
                    "keywords": ppt_doc.keywords,
                    "notes": ppt_doc.comments,
                    "revision": ppt_doc.revision,
                    "category": ppt_doc.category,
                    "content_status": ppt_doc.content_status,
                    "identifier": ppt_doc.identifier,
                    "language": ppt_doc.language,
                    "version": ppt_doc.version,
                    "text": seg.content,
                    "start_time": "",
                    "end_time": "",
                    "date": "",
                    "url": "",
                    "description": "",
                }
            )
        return results

    @staticmethod
    def to_keats(document: document.Document) -> keats_document.KeatsDocument:
        """
        Converts any supported document to a KeatsDocument.
        """
        doc_dict = DocumentAdapter.to_dict(document)
        results = []
        for dd in doc_dict:
            dk = DocumentAdapter.dict_to_keats(data=dd)
            results.append(dk)
        return results

    @staticmethod
    def dict_to_keats(data: dict[str, str]) -> keats_document.KeatsDocument:
        # Hash input includes doc_id, slide number, and segment content
        parent_id = data["parent_file_id"]
        nr = data["segment_nr"]
        text = data["text"]
        hash_input = f"{parent_id}-{nr}-{text}".encode("utf-8")
        unique_id = hashlib.sha256(hash_input).hexdigest()

        return keats_document.KeatsDocument(
            doc_id=unique_id,
            parent_file_id=data["parent_file_id"],
            parent_file_name=data["parent_file_name"],
            segment_nr=data["segment_nr"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            file_type=data["file_type"],
            content_type=data["content_type"],
            length=data["length"],
            doc_title=data["doc_title"],
            course_ids=data["course_ids"],
            course_title=data["course_title"],
            admin_code=data["admin_code"],
            speakers=data["speakers"],
            date=data["date"],
            source=data["source"],
            text=data["text"],
            keywords=data["keywords"],
            url=data["url"],
            description=data["description"],
            notes=data["notes"],
            version=data["version"]
        )
