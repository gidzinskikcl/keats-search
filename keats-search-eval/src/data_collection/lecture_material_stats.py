import pandas as pd
import fitz  # PyMuPDF
import json
import os


COURSES = {
    "18.404J": {
        "title": "Theory of Computation",
        "transcripts": "keats-search-eval/data/transcripts/lectures/18.404J",
        "slides": "keats-search-eval/data/slides/lectures/18.404J",
        "n_lectures": 25,
        "topics": [
            "finite automata",
            "regular expressions",
            "push-down automata",
            "context-free grammars",
            "pumping lemmas",
            "Turing machines",
            "Church-Turing thesis",
            "decidability",
            "the halting problem",
            "reducibility",
            "the recursion theorem",
            "computational complexity",
            "P versus NP problem",
            "hierarchy theorems",
            "hard problems",
            "probabilistic computation",
            "interactive proof systems",
        ],
    },
    "6.0002": {
        "title": "Introduction to Computational Thinking and Data Science",
        "transcripts": "keats-search-eval/data/transcripts/lectures/6.0002",
        "slides": "keats-search-eval/data/slides/lectures/6.0002",
        "n_lectures": 15,
        "topics": [],
    },
    "6.006": {
        "title": "Introduction to Algorithms",
        "transcripts": "keats-search-eval/data/transcripts/lectures/6.006",
        "slides": "keats-search-eval/data/slides/lectures/6.006",
        "n_lectures": 21,
        "topics": [
            "dynamic arrays",
            "heaps",
            "binary trees",
            "hash tables",
            "sorting",
            "graph searching",
            "dynamic programming",
        ],
    },
}


def collect_total_duration(transcript_path):
    total_seconds = 0
    if not os.path.exists(transcript_path):
        return 0
    for lecture in os.listdir(transcript_path):
        lecture_path = os.path.join(transcript_path, lecture)
        if not os.path.isdir(lecture_path):
            continue
        # Try to find the JSON metadata
        for file in os.listdir(lecture_path):
            if file.endswith(".json"):
                json_path = os.path.join(lecture_path, file)
                try:
                    with open(json_path, "r") as f:
                        data = json.load(f)
                        duration = data.get("duration", 0)
                        total_seconds += duration
                except (json.JSONDecodeError, FileNotFoundError):
                    continue
    return total_seconds


def count_total_slide_pages(slides_path):
    total_pages = 0
    if not os.path.exists(slides_path):
        return 0
    for lecture in os.listdir(slides_path):
        lecture_path = os.path.join(slides_path, lecture)
        if not os.path.isdir(lecture_path):
            continue
        for file in os.listdir(lecture_path):
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(lecture_path, file)
                try:
                    doc = fitz.open(pdf_path)
                    total_pages += doc.page_count
                except Exception as e:
                    print(f"Error reading {pdf_path}: {e}")
                break  # assume only one PDF per lecture
    return total_pages


def count_subdirs(path):
    if not os.path.exists(path):
        return 0
    return sum(os.path.isdir(os.path.join(path, d)) for d in os.listdir(path))


def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"


def main():
    rows = []
    for code, data in COURSES.items():
        transcript_dir = data["transcripts"]
        slides_dir = data["slides"]

        num_lectures = count_subdirs(transcript_dir)
        num_slides = count_subdirs(slides_dir)
        total_duration_sec = collect_total_duration(transcript_dir)
        total_slide_pages = count_total_slide_pages(slides_dir)

        rows.append(
            {
                "Course Code": code,
                "Course Title": data["title"],
                "# Lectures": num_lectures,
                "# Slide Folders": num_slides,
                "# Slide Pages": total_slide_pages,
                "Total Duration": format_duration(total_duration_sec),
            }
        )

    df = pd.DataFrame(rows)
    df_transposed = df.set_index("Course Code").T
    df_transposed.to_latex("course_stats_transposed.tex", escape=False)

    # Save as LaTeX table
    df.to_latex("course_stats.tex", index=False, escape=False)
    print("Saved to course_stats.tex")


if __name__ == "__main__":
    main()
