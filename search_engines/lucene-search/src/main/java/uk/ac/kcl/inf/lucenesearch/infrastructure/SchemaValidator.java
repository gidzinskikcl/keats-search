package uk.ac.kcl.inf.lucenesearch.infrastructure;

import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.DocumentType;

public class SchemaValidator {

    public static void validate(Document doc) throws IllegalArgumentException {
        if (doc.documentId() == null || doc.documentId().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: documentId");
        }
        if (doc.content() == null || doc.content().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: content");
        }
        if (doc.title() == null || doc.title().isBlank()) {
            throw new IllegalArgumentException("Missing mandatory field: title");
        }

        switch (doc.type()) {
            case DocumentType.SLIDE -> {
                if (doc.slideNumber() == null) {
                    throw new IllegalArgumentException("Missing mandatory field: slideNumber for SLIDE");
                }
            }
            case DocumentType.VIDEO_TRANSCRIPT -> {
                if (doc.timestamp() == null || doc.timestamp().isBlank()) {
                    throw new IllegalArgumentException("Missing mandatory field: timestamp for VIDEO_TRANSCRIPT");
                }
            }
            default -> throw new IllegalArgumentException("Unknown document type: " + doc.type());
        }
    }
}
