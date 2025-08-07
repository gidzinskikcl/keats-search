import requests

API_URL = "http://46.101.49.168"


def search(
    query: str, top_k: int = 5, course: str = None, lecture: str = None, doc: str = None
):
    payload = {
        "query": {"question": query},
        "top_k": top_k,
        "filters": {},
    }
    if course:
        payload["filters"]["courses_ids"] = [course]
    if lecture:
        payload["filters"]["lectures_ids"] = [lecture]
    if doc:
        payload["filters"]["doc_ids"] = [doc]

    response = requests.post(f"{API_URL}/search", json=payload)
    return response.json()


def get_courses():
    response = requests.get(f"{API_URL}/courses")
    return response.json()


def get_lectures(course_id=None):
    params = {"course": course_id} if course_id else {}
    response = requests.get(f"{API_URL}/lectures", params=params)
    return response.json()


def get_files(course_id=None, lecture_id=None):
    params = {}
    if course_id:
        params["course"] = course_id
    if lecture_id:
        params["lecture"] = lecture_id
    response = requests.get(f"{API_URL}/files", params=params)
    return response.json()


def print_search_results(results):
    for idx, r in enumerate(results):
        doc = r["document"]
        print(f"\nResult {idx + 1}:")
        print(f"  Score: {r['score']:.3f}")
        print(f"  Course: {doc.get('course_id')}")
        print(f"  Lecture: {doc.get('lecture_id')}")
        print(f"  Type: {doc.get('doc_type')}")
        print(f"  URL: {doc.get('url')}")
        print(f"  Page #: {doc.get('page_number')}")
        ts = doc.get("timestamp", {})
        print(f"  Timestamp: {ts.get('start')}–{ts.get('end')}")
        print(f"  Content: {doc.get('content', '').strip()[:150]}...")


if __name__ == "__main__":
    print("=== Available Courses ===")
    courses = get_courses()
    for c in courses:
        print(f"{c['course_id']}: {c['course_title']}")

    print("\n=== Lectures per Course ===")
    for c in courses:
        print(f"\nCourse {c['course_id']}: {c['course_title']}")
        lectures = get_lectures(course_id=c["course_id"])
        for lec in lectures:
            print(f"  Lecture {lec['lecture_id']}: {lec['lecture_title']}")

    print("\n=== Files per Course (First Lecture Only) ===\n")

    for c in courses:
        course_id = c["course_id"]
        print(f"Course {course_id}, Lecture 1")

        files_response = get_files(course_id=course_id, lecture_id=1)

        if not files_response:
            print("  No files found.\n")
            continue

        # Each response is a dict with 'lecture_id' and a nested 'files' list
        files = files_response[0].get("files", [])
        if not files:
            print("  No files available for this lecture.\n")
            continue

        for f in files:
            doc_id = f.get("doc_id", "N/A")
            doc_type = f.get("doc_type", "N/A")
            url = f.get("url", "N/A")
            print(f"  File ID: {doc_id} | Type: {doc_type} | URL: {url}")
        print()

    print("\n=== Example Search ===")
    query = "dynamic programming"
    print(f"Query: {query}")
    results = search(query)
    print_search_results(results)
