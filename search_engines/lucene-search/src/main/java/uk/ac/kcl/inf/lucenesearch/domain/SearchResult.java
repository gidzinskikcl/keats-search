package uk.ac.kcl.inf.lucenesearch.domain;

public record SearchResult(
        float score,
        String iD,
        String documentId,
        String content,
        String courseId,
        String courseName,
        String lectureId,
        String lectureTitle,
        String start,
        String end,
        String pageNumber,
        String type
) {
}