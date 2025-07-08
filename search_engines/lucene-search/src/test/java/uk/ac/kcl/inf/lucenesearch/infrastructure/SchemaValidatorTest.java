package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.junit.jupiter.api.Test;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.DocumentType;

import static org.junit.jupiter.api.Assertions.*;

public class SchemaValidatorTest {

    @Test
    void validate_acceptsValidSlide() {
        Document slide = new Document(
                "id1",
                "slide1",
                "Slide content",
                null,
                null,
                3,
                "lecture1",
                "Title of Slide",
                DocumentType.SLIDE,
                "CS101",
                "Computational Models"
        );

        assertDoesNotThrow(() -> SchemaValidator.validate(slide));
    }

    @Test
    void validate_acceptsValidVideoTranscript() {
        Document transcript = new Document(
                "id2",
                "vid1_seg1",
                "Transcript content",
                "00:00:10",
                "00:00:25",
                null,
                "lecture1",
                "Segment Title",
                DocumentType.VIDEO_TRANSCRIPT,
                "CS102",
                "Information Retrieval"
        );

        assertDoesNotThrow(() -> SchemaValidator.validate(transcript));
    }

    @Test
    void validate_rejectsMissingId() {
        Document doc = new Document(
                null,
                "doc3",
                "Some content",
                "00:00:00",
                "00:00:12",
                null,
                "lectureX",
                "Some Title",
                DocumentType.VIDEO_TRANSCRIPT,
                "CS107",
                "Algorithms 101"
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("iD"));
    }


    @Test
    void validate_rejectsMissingDocumentId() {
        Document doc = new Document(
                "id3",
                null,
                "Content",
                "00:00:00",
                "00:00:12",
                null,
                "lecture2",
                "Title",
                DocumentType.VIDEO_TRANSCRIPT,
                "CS103",
                "Intro to Algorithms"
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("documentId"));
    }

    @Test
    void validate_rejectsMissingLectureId() {
        Document doc = new Document(
                "id4",
                "doc2",
                "Content",
                "00:00:00",
                "00:00:11",
                null,
                null,
                "Some title",
                DocumentType.VIDEO_TRANSCRIPT,
                "CS104",
                "Some Course"
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("lectureId"));
    }

    @Test
    void validate_rejectsMissingCourseId() {
        Document doc = new Document(
                "id5",
                "doc3",
                "Content",
                "00:00:00",
                "00:00:10",
                null,
                "lecture3",
                "Some title",
                DocumentType.VIDEO_TRANSCRIPT,
                null,
                "Course Name"
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertEquals("Missing mandatory field: courseId", ex.getMessage());
    }

    @Test
    void validate_rejectsMissingPageNumberForSlide() {
        Document doc = new Document(
                "id6",
                "slide5",
                "Slide content",
                null,
                null,
                null,
                "lecture4",
                "Slide Title",
                DocumentType.SLIDE,
                "CS105",
                "Slide Course"
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("pageNumber"));
    }

    @Test
    void validate_rejectsMissingTimestampForTranscript() {
        Document doc = new Document(
                "id7",
                "vid1_seg1",
                "Transcript content",
                null,
                null,
                null,
                "lecture5",
                "Segment Title",
                DocumentType.VIDEO_TRANSCRIPT,
                "CS106",
                "Transcript Course"
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("start"));
        assertTrue(ex.getMessage().contains("end"));
    }
}
