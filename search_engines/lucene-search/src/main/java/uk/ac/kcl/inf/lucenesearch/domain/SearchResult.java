package uk.ac.kcl.inf.lucenesearch.domain;

public record SearchResult(
        String query,
        String documentId,
        String content,
        float score,
        String courseName,
        String title
) {
}