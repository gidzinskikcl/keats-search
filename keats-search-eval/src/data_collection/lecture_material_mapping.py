import os
import json

# Define the paths and course information
BASE_DIR = "keats-search-eval/data"
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts", "lectures")
SLIDES_DIR = os.path.join(BASE_DIR, "slides/lectures")

# Only include these course IDs
COURSES = {
    "18.404J": "Theory of Computation",
    "6.006": "Introduction to Algorithms",
    "6.0002": "Introduction to Computational Thinking and Data Science",
}

# Mapping from lecture_id to lecture_title per course
lecture_titles_by_course = {}
mapping = []

for course_id, course_title in COURSES.items():
    transcript_course_dir = os.path.join(TRANSCRIPTS_DIR, course_id)
    slides_course_dir = os.path.join(SLIDES_DIR, course_id)

    lecture_titles_by_course[course_id] = {}

    # First process transcripts to gather lecture titles
    if os.path.isdir(transcript_course_dir):
        lecture_folders = sorted(os.listdir(transcript_course_dir))
        for lecture_folder in lecture_folders:
            lecture_title = lecture_folder
            lecture_id = lecture_title.split()[0]

            lecture_titles_by_course[course_id][lecture_id] = lecture_title

            lecture_path = os.path.join(transcript_course_dir, lecture_folder)
            if not os.path.isdir(lecture_path):
                continue

            for file in os.listdir(lecture_path):
                if file.endswith(".srt"):
                    mapping.append(
                        {
                            "doc_id": file,
                            "course_id": course_id,
                            "course_title": course_title,
                            "lecture_id": lecture_id,
                            "lecture_title": lecture_title,
                        }
                    )

    # Now process slides using the lecture title from transcripts
    if os.path.isdir(slides_course_dir):
        lecture_folders = sorted(os.listdir(slides_course_dir))
        for lecture_folder in lecture_folders:
            lecture_id = lecture_folder.split()[1].rstrip(":")

            # Fall back to original folder name if no match
            lecture_title = lecture_titles_by_course[course_id].get(
                lecture_id, lecture_folder
            )

            lecture_path = os.path.join(slides_course_dir, lecture_folder)
            if not os.path.isdir(lecture_path):
                continue

            for file in os.listdir(lecture_path):
                if file.endswith(".pdf"):
                    mapping.append(
                        {
                            "doc_id": file,
                            "course_id": course_id,
                            "course_title": course_title,
                            "lecture_id": lecture_id,
                            "lecture_title": lecture_title,
                        }
                    )

# Write to JSON file
output_path = "keats-search-eval/data/metadata/file_to_metadata_mapping.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print(f"Mapping written to {output_path}")


# import os
# import json

# # Define the paths and course information
# BASE_DIR = "keats-search-eval/data"
# TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts", "lectures")
# SLIDES_DIR = os.path.join(BASE_DIR, "slides")

# # Only include these course IDs
# COURSES = {
#     "18.404J": "Theory of Computation",
#     "6.006": "Introduction to Algorithms",
#     "6.0002": "Introduction to Computational Thinking and Data Science"
# }

# # Collect mapping data
# mapping = []

# def extract_lecture_number(name: str) -> str | None:
#     parts = name.split()
#     if len(parts) < 2:
#         return None
#     raw = parts[1]
#     if ":" in raw:
#         return raw.split(":")[0]
#     return raw

# for course_id, course_title in COURSES.items():
#     transcript_course_dir = os.path.join(TRANSCRIPTS_DIR, course_id)
#     slides_course_dir = os.path.join(SLIDES_DIR, course_id)


#     if os.path.isdir(transcript_course_dir):
#         lecture_folders = sorted(os.listdir(transcript_course_dir))
#         for lecture_folder in lecture_folders:
#             lecture_title = lecture_folder
#             lecture_id = lecture_title.split()[0]

#             lecture_path = os.path.join(transcript_course_dir, lecture_folder)
#             if not os.path.isdir(lecture_path):
#                 continue

#             for file in os.listdir(lecture_path):
#                 if file.endswith(".srt"):
#                     mapping.append({
#                         "doc_id": file,
#                         "course_id": course_id,
#                         "course_title": course_title,
#                         "lecture_id": lecture_id,
#                         "lecture_title": lecture_title
#                     })


#     # Now collect slides and match based on lecture number
#     if os.path.isdir(slides_course_dir):
#         lecture_folders = sorted(os.listdir(slides_course_dir))
#         for lecture_folder in lecture_folders:
#             lecture_title = lecture_folder
#             extracted = lecture_title.split()[1]

#             if ":" in extracted:
#                 lecture_id = extracted[:-1]
#             else:
#                 lecture_id = extracted


#             lecture_path = os.path.join(slides_course_dir, lecture_folder)

#             if not os.path.isdir(lecture_path):
#                 continue

#             for file in os.listdir(lecture_path):
#                 if file.endswith(".pdf"):
#                     mapping.append({
#                         "doc_id": file,
#                         "course_id": course_id,
#                         "course_title": course_title,
#                         "lecture_id": lecture_id,
#                         "lecture_title": lecture_title
#                     })


# # Write to JSON file
# output_path = "keats-search-eval/data/metadata/file_to_metadata_mapping.json"
# os.makedirs(os.path.dirname(output_path), exist_ok=True)
# with open(output_path, "w", encoding="utf-8") as f:
#     json.dump(mapping, f, indent=2, ensure_ascii=False)

# print(f"Mapping written to {output_path}")
