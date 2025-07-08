from collections import defaultdict
import json
import pathlib
import subprocess
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

import config
from core import schemas

router = APIRouter()

def _lucene_meta_query(mode: str, index_path: str, filters: dict[str, str] = {}) -> list[dict]:
    args = [
        "java", "-jar", config.settings.LUCENE_JAR_PATH,
        "--mode", "meta", mode, index_path
    ]
    for k, v in filters.items():
        args.extend([f"--{k}", v])

    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())

    return json.loads(proc.stdout)


@router.get("/courses", response_model=list[schemas.CourseInfo])
def list_courses():
    try:
        data = _lucene_meta_query("courses", config.settings.INDEX_DIR)
        return sorted(data, key=lambda d: d["course_id"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/lectures", response_model=list[schemas.LectureInfo])
def list_lectures(course: Optional[str] = Query(None)):
    """
    Returns a list of lecture IDs and titles, optionally filtered by course ID.
    """
    try:
        filters = {}
        if course:
            filters["course"] = course

        data = _lucene_meta_query("lectures", config.settings.INDEX_DIR, filters)
        return data  # no need to sort dicts; let frontend sort by title or ID
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/files", response_model=list[schemas.FileInfo])
def list_files(
    course: Optional[str] = Query(None),
    lecture: Optional[int] = Query(None)
):
    try:
        filters = {}
        if course:
            filters["course"] = course
        if lecture:
            filters["lecture"] = str(lecture)

        data = _lucene_meta_query("files", config.settings.INDEX_DIR, filters)
        return [schemas.FileInfo(**item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

