import pathlib
import shutil
import sys

# Source and destination paths
base_dir = pathlib.Path("keats-search-eval/data/slides/lectures")
dest_dir = pathlib.Path("keats-search-api/data/thumbnails")
dest_dir.mkdir(parents=True, exist_ok=True)

# Courses of interest
courses_of_interest = {"6.0002", "6.006", "18.404J"}

# To track duplicates
seen_filenames = set()


def main():
    for course_dir in base_dir.iterdir():
        if not course_dir.is_dir() or course_dir.name not in courses_of_interest:
            continue

        for lecture_dir in course_dir.iterdir():
            if not lecture_dir.is_dir():
                continue

            for file in lecture_dir.glob("*_thumbnail.jpg"):
                if file.name in seen_filenames:
                    print(f"❌ Duplicate filename found: {file.name}")
                    sys.exit(1)

                seen_filenames.add(file.name)
                dest_path = dest_dir / file.name
                shutil.copy(file, dest_path)
                print(f"Copied {file} → {dest_path}")


if __name__ == "__main__":
    main()
