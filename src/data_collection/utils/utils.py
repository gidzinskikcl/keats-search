from data_collection import schemas

def document_to_dict(doc: schemas.DocumentSchema) -> dict:
    return {
        "doc_id": doc.doc_id,
        "content": doc.content,
        "title": doc.title,
        "timestamp": {
            "start": doc.timestamp.start.total_seconds() if doc.timestamp else None,
            "end": doc.timestamp.end.total_seconds() if doc.timestamp else None,
        } if doc.timestamp else None,
        "pageNumber": doc.pageNumber,
        "keywords": doc.keywords,
        "doc_type": doc.doc_type.value,  # enum to string
        "speaker": doc.speaker,
        "course_name": doc.course_name,
    }