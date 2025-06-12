from data_collection import schemas
from data_collection.segmenters import transcript_segmenter

class ChapterSegmenter(transcript_segmenter.TranscriptSegmenter):

    @staticmethod
    def segment(transcript_schema: schemas.TranscriptSchema, chapters: list[schemas.Chapter]) -> list[schemas.TranscriptSegment]:
        results = []

        for chapter in chapters:
            matching_subtitles = [
                subtitle for subtitle in transcript_schema.subtitles
                if subtitle.timestamp.start >= chapter.timestamp.start and subtitle.timestamp.end <= chapter.timestamp.end
            ]

            combined_text = " ".join(sub.text for sub in matching_subtitles)


            segment = schemas.TranscriptSegment(
                parent_file=transcript_schema.file_name,
                timestamp=chapter.timestamp,
                text=combined_text
            )
            results.append(segment)

        return results