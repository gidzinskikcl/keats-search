package uk.ac.kcl.inf.lucenesearch.domain;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;

import java.io.IOException;

public class DocumentTypeDeserializer extends JsonDeserializer<DocumentType> {
    @Override
    public DocumentType deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
        String value = p.getText().trim().toLowerCase();

        return switch (value) {
            case "pdf" -> DocumentType.SLIDE;
            case "mp4" -> DocumentType.VIDEO_TRANSCRIPT;
            default -> throw new IllegalArgumentException("Unsupported doc_type: " + value);
        };
    }
}
