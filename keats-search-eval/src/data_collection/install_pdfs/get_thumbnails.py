# import fitz
# import pathlib


# # Root path to lectures
# base_dir = pathlib.Path("keats-search-eval/data/slides/lectures")

# # Courses of interest
# courses_of_interest = {"6.0002", "6.006", "18.404J"}


# def main():
#     for course_dir in base_dir.iterdir():
#         if course_dir.name not in courses_of_interest or not course_dir.is_dir():
#             continue

#         # Look inside each lecture subfolder
#         for lecture_dir in course_dir.iterdir():
#             if not lecture_dir.is_dir():
#                 continue

#             # Find any PDF file in that lecture folder
#             for pdf_path in lecture_dir.glob("*.pdf"):
#                 thumbnail_path = pdf_path.with_name(pdf_path.stem + "_thumbnail.jpg")

#                 if thumbnail_path.exists():
#                     print(f"Already exists: {thumbnail_path.name}")
#                     continue

#                 try:
#                     doc = fitz.open(pdf_path)
#                     page = doc.load_page(0)
#                     mat = fitz.Matrix(0.3, 0.3)  # Zoom = 0.3
#                     pix = page.get_pixmap(matrix=mat)
#                     pix.save(thumbnail_path)
#                     print(f"Thumbnail saved: {thumbnail_path}")
#                 except Exception as e:
#                     print(f"Error processing {pdf_path}: {e}")


# if __name__ == "__main__":
#     main()
import fitz  # PyMuPDF
import pathlib
from PIL import Image
import io

# Root path to lectures
base_dir = pathlib.Path("keats-search-eval/data/slides/lectures")
courses_of_interest = {"6.0002", "6.006", "18.404J"}


def crop_to_16_9(pix):
    img = Image.open(io.BytesIO(pix.tobytes("jpeg")))
    width, height = img.size
    target_aspect = 16 / 9

    if width / height > target_aspect:
        # Too wide: crop width
        new_width = int(height * target_aspect)
        left = (width - new_width) // 2
        box = (left, 0, left + new_width, height)
    else:
        # Too tall: crop height
        new_height = int(width / target_aspect)
        top = (height - new_height) // 2
        box = (0, top, width, top + new_height)

    return img.crop(box)


def main():
    for course_dir in base_dir.iterdir():
        if course_dir.name not in courses_of_interest or not course_dir.is_dir():
            continue

        for lecture_dir in course_dir.iterdir():
            if not lecture_dir.is_dir():
                continue

            for pdf_path in lecture_dir.glob("*.pdf"):
                thumbnail_path = pdf_path.with_name(pdf_path.stem + "_thumbnail.jpg")

                print(f"Saving thumbnail: {thumbnail_path.name}")

                try:
                    doc = fitz.open(pdf_path)
                    page = doc.load_page(0)
                    mat = fitz.Matrix(2.0, 2.0)  # High-res rendering
                    pix = page.get_pixmap(matrix=mat)

                    cropped_img = crop_to_16_9(pix)
                    cropped_img.save(thumbnail_path, "JPEG")
                    print(f"Thumbnail saved: {thumbnail_path}")
                except Exception as e:
                    print(f"Error processing {pdf_path}: {e}")


if __name__ == "__main__":
    main()
