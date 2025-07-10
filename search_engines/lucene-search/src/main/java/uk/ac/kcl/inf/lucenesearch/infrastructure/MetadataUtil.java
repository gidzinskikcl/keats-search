package uk.ac.kcl.inf.lucenesearch.infrastructure;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;

import java.util.*;

public class MetadataUtil {
    public static Map<String, String> parseFilters(String[] args) {
        Map<String, String> filters = new HashMap<>();
        for (int i = 0; i < args.length - 1; i += 2) {
            if (args[i].startsWith("--")) {
                filters.put(args[i].substring(2), args[i + 1]);
            }
        }
        return filters;
    }

    public static void listCourses(DirectoryReader reader) throws Exception {
        Map<String, String> courses = new HashMap<>();
        for (int i = 0; i < reader.maxDoc(); i++) {
            Document doc = reader.document(i);
            String courseId = doc.get("courseId");
            String courseTitle = doc.get("courseName");

            if (courseId != null) {
                courses.putIfAbsent(courseId, courseTitle != null ? courseTitle : "");
            }
        }

        List<Map<String, String>> result = courses.entrySet().stream()
                .map(e -> Map.of("course_id", e.getKey(), "course_title", e.getValue()))
                .sorted(Comparator.comparing(m -> m.get("course_id")))
                .toList();

        new ObjectMapper().writeValue(System.out, result);
    }


    public static void listFiles(DirectoryReader reader, Map<String, String> filters) throws Exception {
        Map<String, Map<String, Map<String, String>>> grouped = new HashMap<>();

        for (int i = 0; i < reader.maxDoc(); i++) {
            Document doc = reader.document(i);

            String courseId = doc.get("courseId");
            String lectureId = doc.get("lectureId");
            String docId = doc.get("documentId");
            String docType = doc.get("type");
            String url = doc.get("url");
            String thumbnailUrl = doc.get("thumbnailUrl");

            if (courseId == null || lectureId == null || docId == null || docType == null) continue;
            if (filters.containsKey("course") && !filters.get("course").equals(courseId)) continue;
            if (filters.containsKey("lecture") && !filters.get("lecture").equals(lectureId)) continue;

            String mappedType = switch (docType.toUpperCase()) {
                case "SLIDE" -> "pdf";
                case "TRANSCRIPT", "VIDEO_TRANSCRIPT" -> "mp4";
                default -> null;
            };

            if (mappedType != null) {
                String compositeKey = courseId + "::" + lectureId;

                Map<String, String> docInfo = Map.of(
                        "doc_type", mappedType,
                        "url", url != null ? url : "",
                        "thumbnail_url", thumbnailUrl != null ? thumbnailUrl : ""
                );

                grouped
                        .computeIfAbsent(compositeKey, k -> new HashMap<>())
                        .put(docId, docInfo);
            }
        }

        List<Map<String, Object>> result = new ArrayList<>();
        for (var entry : grouped.entrySet()) {
            String[] splitKey = entry.getKey().split("::", 2);
            String courseId = splitKey[0];
            String lectureId = splitKey[1];

            List<Map<String, String>> files = entry.getValue().entrySet().stream()
                    .map(e -> {
                        Map<String, String> info = e.getValue();
                        return Map.of(
                                "doc_id", e.getKey(),
                                "doc_type", info.get("doc_type"),
                                "url", info.get("url"),
                                "thumbnail_url", info.get("thumbnail_url")
                        );
                    })
                    .sorted(Comparator.comparing(f -> f.get("doc_id")))
                    .toList();

            result.add(Map.of(
                    "course_id", courseId,
                    "lecture", lectureId,
                    "files", files
            ));
        }

        new ObjectMapper().writeValue(System.out, result);
    }


    public static void listLectures(DirectoryReader reader, Map<String, String> filters) throws Exception {
        Map<String, String> lectures = new HashMap<>();

        for (int i = 0; i < reader.maxDoc(); i++) {
            Document doc = reader.document(i);

            String courseId = doc.get("courseId");
            String lectureId = doc.get("lectureId");
            String lectureTitle = doc.get("lectureTitle");

            if (lectureId == null || courseId == null) continue;
            if (filters.containsKey("course") && !filters.get("course").equals(courseId)) {
                continue;
            }

            // Use composite key to disambiguate lectures across courses
            String compositeKey = courseId + "::" + lectureId;
            lectures.putIfAbsent(compositeKey, lectureTitle != null ? lectureTitle : "");
        }

        List<Map<String, String>> result = lectures.entrySet()
                .stream()
                .sorted(Map.Entry.comparingByKey())
                .map(e -> {
                    String[] parts = e.getKey().split("::");
                    String courseId = parts[0];
                    String lectureId = parts[1];
                    return Map.of(
                            "course_id", courseId,
                            "lecture_id", lectureId,
                            "lecture_title", e.getValue()
                    );
                })
                .toList();

        new ObjectMapper().writeValue(System.out, result);
    }



}