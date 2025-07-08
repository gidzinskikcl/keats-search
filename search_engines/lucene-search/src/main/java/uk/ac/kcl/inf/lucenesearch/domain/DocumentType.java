package uk.ac.kcl.inf.lucenesearch.domain;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;

@JsonDeserialize(using = DocumentTypeDeserializer.class)
public enum DocumentType {
    SLIDE,
    VIDEO_TRANSCRIPT
}
