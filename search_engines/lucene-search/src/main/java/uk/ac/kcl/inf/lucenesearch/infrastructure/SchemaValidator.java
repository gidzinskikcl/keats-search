package uk.ac.kcl.inf.lucenesearch.infrastructure;

import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.DocumentType;

public class SchemaValidator {

    public static void validate(Document doc) throws IllegalArgumentException {
        if (doc.iD() == null || doc.iD().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: iD");
        }
        if (doc.documentId() == null || doc.documentId().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: documentId");
        }
        if (doc.content() == null || doc.content().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: content");
        }
        if (doc.lectureId() == null || doc.lectureId().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: lectureId");
        }
        if (doc.courseId() == null || doc.courseId().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: courseId");
        }
        if (doc.url() == null || doc.url().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: url");
        }

        switch (doc.type()) {
            case DocumentType.SLIDE -> {
                if (doc.pageNumber() == null) {
                    throw new IllegalArgumentException("Missing mandatory field: pageNumber for SLIDE");
                }
            }
            case DocumentType.VIDEO_TRANSCRIPT -> {
                if (doc.start() == null || doc.end() == null) {
                    throw new IllegalArgumentException("Missing mandatory start or end time for VIDEO_TRANSCRIPT");
                }
            }
            default -> throw new IllegalArgumentException("Unknown document type: " + doc.type());
        }
    }
}
