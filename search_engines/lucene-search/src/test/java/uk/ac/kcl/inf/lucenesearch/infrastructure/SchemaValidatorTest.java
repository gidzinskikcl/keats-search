package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.junit.jupiter.api.Test;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.DocumentType;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class SchemaValidatorTest {

    @Test
    void validate_acceptsValidSlide() {
        Document slide = new Document(
                "slide1",
                "Slide content",
                "Title of Slide",
                null,
                null,
                3,
                List.of("search", "ranking"),
                DocumentType.SLIDE
        );

        assertDoesNotThrow(() -> SchemaValidator.validate(slide));
    }

    @Test
    void validate_acceptsValidVideoTranscript() {
        Document transcript = new Document(
                "vid1_seg1",
                "Transcript content",
                "Segment Title",
                "00:00:10",
                "Dr. Smith",
                null,
                List.of(),
                DocumentType.VIDEO_TRANSCRIPT
        );

        assertDoesNotThrow(() -> SchemaValidator.validate(transcript));
    }

    @Test
    void validate_rejectsMissingDocumentId() {
        Document doc = new Document(
                null,
                "Content",
                "Title",
                "00:00:00",
                null,
                null,
                null,
                DocumentType.VIDEO_TRANSCRIPT
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("documentId"));
    }

    @Test
    void validate_rejectsMissingTitle() {
        Document doc = new Document(
                "doc1",
                "Some content",
                null,
                "00:00:00",
                null,
                null,
                null,
                DocumentType.VIDEO_TRANSCRIPT
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("title"));
    }

    @Test
    void validate_rejectsMissingSlideNumberForSlide() {
        Document doc = new Document(
                "slide5",
                "Slide content",
                "Slide Title",
                null,
                null,
                null,
                null,
                DocumentType.SLIDE
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("slideNumber"));
    }

    @Test
    void validate_rejectsMissingTimestampForTranscript() {
        Document doc = new Document(
                "vid1_seg1",
                "Transcript content",
                "Segment Title",
                null,
                null,
                null,
                null,
                DocumentType.VIDEO_TRANSCRIPT
        );

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> SchemaValidator.validate(doc));
        assertTrue(ex.getMessage().contains("timestamp"));
    }
}
