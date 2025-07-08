# 📘 Keats Search API

A FastAPI-based service for querying, indexing, and retrieving educational content (lecture slides and videos) using a Lucene BM25 search engine.

---

## Base Info

- **Base URL**: `http://<server-address>:<port>`
- **API Version**: `v1.0`
- **Search Engine**: `BM25`

---
## 📑 Table of Contents

- [General Endpoints](#general-endpoints)
  - [`GET /`](#get-)
  - [`GET /status`](#get-status)
  - [`GET /version`](#get-version)
- [Search Endpoint](#-search-endpoint)
  - [`POST /search`](#post-search)
- [Indexing Endpoint](#️-indexing-endpoint)
  - [`POST /index`](#post-index)
- [Metadata Endpoints](#metadata-endpoints)
  - [`GET /courses`](#get-courses)
  - [`GET /lectures?course=<course_id>`](#get-lecturescoursecourse_id)
  - [`GET /files?course=<course_id>&lecture=<lecture_id>`](#get-filescoursecourse_idlecturelecture_id)
- [Document Format](#document-format)
- [Example API Usage](#examples-api-usage)
  - [`curl` Commands](#-example-curl-commands)
    - [Search](#-search-for-segments)
    - [Index documents](#-index-documents)
    - [Get courses](#-get-list-of-courses)
    - [Get lectures](#-get-list-of-lectures-in-a-course)
    - [Get files](#️-get-files-for-a-lecture)
  - [Python Examples](#-example-python-api-usage)
    - [Search](#-search-1)
    - [Indexing](#-indexing-documents)
    - [List Courses](#-list-courses)
    - [List Lectures](#-list-lectures)
    - [List Files](#-list-files-for-a-lecture)

---

## General Endpoints

### `GET /`
Returns a welcome message.
```json
{
  "message": "Welcome to Keats Search API"
}
```
### `GET /status`

Check if the service is online.

**Response**

```json
{
  "status": "ok"
}
```

---

### `GET /version`

Returns API and search engine version.

**Response**

```json
{
  "version": "v1.0",
  "engine": "bm25"
}
```

---

## 🔍 Search Endpoint

### `POST /search`

Performs a full-text search on indexed documents with optional filtering.

**Request Body**

```json
{
  "query": {
    "question": "Machine Learning"
  },
  "top_k": 5,
  "filters": {
    "courses_ids": ["18.404J"],
    "lectures_ids": ["24"],
    "doc_ids": ["cbfe4302bc8bfa4dca3c3bfcfd4661a8_MIT18_404f20_lec24"]
  }
}
```

- `top_k` is optional (defaults to 10).
- `filters` is optional, you can filter through courses, lectures, documents or a combination of them.

**Response**

Returns a list of ranked documents:

```json
[
  {
    "document": {
      "id": "...",
      "doc_id": "...",
      "content": "...",
      "timestamp": {
        "start": "00:00:01",
        "end": "00:00:15"
      },
      "page_number": 1,
      "lecture_id": "24",
      "lecture_title": "24 Probabilistic Computation cont",
      "course_id": "18.404J",
      "course_name": "Theory of Computation",
      "doc_type": "pdf"
    },
    "score": 2.134
  }
]
```

---

## 🗂️ Indexing Endpoint

### `POST /index`

Index new documents from a JSON file.

**Request Body**

```json
{
  "document_path": "/path/to/documents.json",
  "index_dir": "/path/to/index"
}
```

Both fields are optional — defaults will be used if omitted.

**Response**

```json
{
  "message": "Indexing complete",
  "index_dir": "/path/to/index"
}
```

---

## Metadata Endpoints

### `GET /courses`

List all indexed courses.

**Response**

```json
[
  {
    "course_id": "18.404J",
    "course_title": "Theory of Computation"
  }
]
```

---

### `GET /lectures?course=<course_id>`

List all lectures, optionally filtered by course ID.

**Query Param (optional):**

- `course`: e.g., `18.404J`

**Response**

```json
[
  {
    "lecture_id": "24",
    "lecture_title": "24 Probabilistic Computation cont"
  }
]
```

---

### `GET /files?course=<course_id>&lecture=<lecture_id>`

List files (PDFs, transcripts) per lecture.

**Query Params (optional):**

- `course`: e.g., `18.404J`
- `lecture`: e.g., `24`

**Response**

```json
[
  {
    "lecture": "24",
    "files": [
      {
        "doc_id": "cbfe4302bc8bfa4dca3c3bfcfd4661a8_MIT18_404f20_lec24",
        "doc_type": "pdf"
      },
      {
        "doc_id": "...",
        "doc_type": "mp4"
      }
    ]
  }
]
```

---

## Document Format

Each document in a ranked list of results should follow this schema:

```json
{
  "id": "<unique_segment_id>",
  "doc_id": "<document_file_id>",
  "content": "actual text content...",
  "page_number": "1",
  "lecture_id": "24",
  "lecture_title": "Lecture Title",
  "course_id": "18.404J",
  "course_name": "Theory of Computation",
  "doc_type": "pdf"  // or "mp4"
}
```

---
## Examples API USAGE

### Example `curl` Commands

### 🔍 Search for segments

```bash
curl -X POST http://<host>:<port>/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": { "question": "What is probabilistic computation?" },
    "top_k": 3,
    "filters": {
      "courses_ids": ["18.404J"],
      "lectures_ids": ["24"]
    }
  }'
```

---

### 📄 Index documents

```bash
curl -X POST http://<host>:<port>/index \
  -H "Content-Type: application/json" \
  -d '{
    "document_path": "/absolute/path/to/documents.json",
    "index_dir": "/absolute/path/to/index"
  }'
```

---

### 📚 Get list of courses

```bash
curl http://<host>:<port>/courses
```

---

### 📚 Get list of lectures in a course

```bash
curl "http://<host>:<port>/lectures?course=18.404J"
```

---

### 📚 Get files for a lecture
```bash
curl "http://<host>:<port>/files?course=18.404J&lecture=24"
```
---

## 🐍 Example Python API Usage
### Prerequisite

Make sure you have `requests` installed:

```bash
pip install requests
```

---

### 🔍 Search

```python
import requests

url = "http://<host>:<port>/search"
payload = {
    "query": { "question": "What is probabilistic computation?" },
    "top_k": 5,
    "filters": {
        "courses_ids": ["18.404J"],
        "lectures_ids": ["24"]
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

---

### 📄 Indexing Documents

```python
import requests

url = "http://<host>:<port>/index"
payload = {
    "document_path": "/absolute/path/to/documents.json",
    "index_dir": "/absolute/path/to/index"
}

response = requests.post(url, json=payload)
print(response.json())
```

---

### 📚 List Courses

```python
import requests

response = requests.get("http://<host>:<port>/courses")
print(response.json())
```

---

### 📚 List Lectures

```python
import requests

params = {"course": "18.404J"}
response = requests.get("http://<host>:<port>/lectures", params=params)
print(response.json())
```

---

### 📂 List Files for a Lecture

```python
import requests

params = {"course": "18.404J", "lecture": 24}
response = requests.get("http://<host>:<port>/files", params=params)
print(response.json())
```