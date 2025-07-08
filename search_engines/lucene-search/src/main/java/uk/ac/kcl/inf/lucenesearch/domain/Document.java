package uk.ac.kcl.inf.lucenesearch.domain;

import com.fasterxml.jackson.annotation.JsonProperty;

public record Document(
        @JsonProperty("id") String iD,
        @JsonProperty("doc_id") String documentId,
        @JsonProperty("content") String content,
        @JsonProperty("start") String start,
        @JsonProperty("end") String end,
        @JsonProperty("page_number") Integer pageNumber,
        @JsonProperty("lecture_id") String lectureId,
        @JsonProperty("lecture_title") String lectureTitle,
        @JsonProperty("doc_type") DocumentType type,
        @JsonProperty("course_id") String courseId,
        @JsonProperty("course_name") String courseName
) {}
