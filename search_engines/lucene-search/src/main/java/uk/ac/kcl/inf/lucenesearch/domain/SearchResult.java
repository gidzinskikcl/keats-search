package uk.ac.kcl.inf.lucenesearch.domain;

import java.util.List;

public record SearchResult(
        float score,
        String documentId,
        String content,
        String courseName,
        String title,
        String start,
        String end,
        String speaker,
        String slideNumber,
        List<String> keywords,
        String type
) {
}