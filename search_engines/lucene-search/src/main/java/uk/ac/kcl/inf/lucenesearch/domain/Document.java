package uk.ac.kcl.inf.lucenesearch.domain;

import java.util.List;

public record Document(
        String documentId,
        String content,
        String title,
        String start,
        String end,
        String speaker,
        Integer slideNumber,
        List<String> keywords,
        DocumentType type,
        String courseName
) {

}