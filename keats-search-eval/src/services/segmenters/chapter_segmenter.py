from schemas import schemas
from services.segmenters import transcript_segmenter


class ChapterSegmenter(transcript_segmenter.TranscriptSegmenter):

    @staticmethod
    def segment(
        transcript_schema: schemas.TranscriptSchema,
    ) -> list[schemas.TranscriptSegment]:
        results = []

        for chapter in transcript_schema.chapters or []:
            matching_subtitles = [
                subtitle
                for subtitle in transcript_schema.subtitles
                if subtitle.timestamp.start >= chapter.timestamp.start
                and subtitle.timestamp.end <= chapter.timestamp.end
            ]

            combined_text = " ".join(sub.text for sub in matching_subtitles)

            segment = schemas.TranscriptSegment(
                nr=chapter.nr,
                parent_file=transcript_schema.file_name,
                timestamp=chapter.timestamp,
                text=combined_text,
                course_id=transcript_schema.course_id,
                course_name=transcript_schema.course_name,
                lecture_id=transcript_schema.lecture_id,
                lecture_name=transcript_schema.lecture_name,
                chapter_title=chapter.title or None,
            )
            results.append(segment)

        return results
