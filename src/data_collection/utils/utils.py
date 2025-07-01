from data_collection import schemas
from datetime import timedelta


def document_to_dict(doc: schemas.DocumentSchema) -> dict:
    return {
        "documentId": doc.doc_id,
        "content": doc.content,
        "title": doc.title,
        "start": format_timedelta(doc.timestamp.start) if doc.timestamp else None,
        "end": format_timedelta(doc.timestamp.end) if doc.timestamp else None,
        "slideNumber": doc.pageNumber,
        "keywords": doc.keywords,
        "type": _get_type(doc.doc_type.value),
        "speaker": doc.speaker,
        "courseName": doc.course_name,
    }


def _get_type(type: str) -> str:
    if type == "pdf":
        return "SLIDE"
    elif type == "srt":
        return "VIDEO_TRANSCRIPT"
    else:
        raise ValueError(f"Unsupported document type: '{type}'")


def format_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
