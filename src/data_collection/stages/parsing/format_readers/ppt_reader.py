from pptx import Presentation
from data_collection.stages.parsing.format_readers import reader


class PPTReader(reader.Reader):
    """
    Concrete content extractor for PowerPoint files.
    """

    def get_text(self, file_path: str) -> str:
        """
        Extracts text from a PowerPoint file using python-pptx.
        """
        extracted_text = []

        try:
            presentation = Presentation(file_path)
            for slide_number, slide in enumerate(presentation.slides):
                slide_text = []
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        slide_text.append(shape.text)
                # Combine slide texts
                extracted_text.append("\n".join(slide_text))
        except Exception as e:
            print(f"Error reading PowerPoint file: {e}")
            raise e

        result = "\n".join(extracted_text)
        return result

    def get_images(self, file_path: str) -> list:
        """
        Image extraction is not implemented yet.
        """
        raise NotImplementedError("Image extraction is not implemented yet.")

    def get_vector_graphics(self, file_path: str) -> list:
        """
        Vector graphics extraction is not implemented yet.
        """
        raise NotImplementedError("Vector graphics extraction is not implemented yet.")
