package uk.ac.kcl.inf.lucenesearch.infrastructure;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.ByteBuffersDirectory;
import org.junit.jupiter.api.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class MetadataUtilTest {

    Directory directory;
    IndexWriter writer;
    DirectoryReader reader;

    @BeforeEach
    void setup() throws Exception {
        directory = new ByteBuffersDirectory();  // fixed this line
        IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
        writer = new IndexWriter(directory, config);

        addDoc("CS101", "1", "doc1", "SLIDE", "Intro to Testing");
        addDoc("CS101", "1", "doc2", "TRANSCRIPT", "Intro to Testing");
        addDoc("CS102", "2", "doc3", "SLIDE", "Advanced Topics");

        writer.close();
        reader = DirectoryReader.open(directory);
    }


    private void addDoc(String courseId, String lectureId, String docId, String type, String lectureTitle) throws Exception {
        Document doc = new Document();
        doc.add(new StringField("courseId", courseId, Field.Store.YES));
        doc.add(new StringField("lectureId", lectureId, Field.Store.YES));
        doc.add(new StringField("documentId", docId, Field.Store.YES));
        doc.add(new StringField("type", type, Field.Store.YES));
        doc.add(new StringField("lectureTitle", lectureTitle, Field.Store.YES));
        doc.add(new StringField("courseName", "Computer Science", Field.Store.YES));
        writer.addDocument(doc);
    }


    @AfterEach
    void tearDown() throws Exception {
        reader.close();
        directory.close();
    }

    @Test
    void testParseFilters() {
        String[] args = {"--course", "CS101", "--lecture", "1"};
        Map<String, String> filters = MetadataUtil.parseFilters(args);
        assertEquals("CS101", filters.get("course"));
        assertEquals("1", filters.get("lecture"));
    }

    @Test
    void testListCourses() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));

        MetadataUtil.listCourses(reader);
        System.setOut(System.out); // reset

        List result = new ObjectMapper().readValue(out.toString(), List.class);
        assertEquals(List.of(
                Map.of("course_id", "CS101", "course_title", "Computer Science"),
                Map.of("course_id", "CS102", "course_title", "Computer Science")
        ), result);
    }


    @Test
    void testListFilesWithFilter() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));

        Map<String, String> filters = Map.of("course", "CS101");
        MetadataUtil.listFiles(reader, filters);
        System.setOut(System.out);

        List result = new ObjectMapper().readValue(out.toString(), List.class);

        assertEquals(1, result.size());
        Map<String, Object> lecture = (Map<String, Object>) result.get(0);
        assertEquals("1", lecture.get("lecture_id"));

        List<Map<String, String>> files = (List<Map<String, String>>) lecture.get("files");
        assertEquals(2, files.size());

        Set<String> expectedTypes = Set.of("pdf", "mp4");
        Set<String> actualTypes = new HashSet<>();
        for (Map<String, String> file : files) {
            actualTypes.add(file.get("doc_type"));
        }

        assertEquals(expectedTypes, actualTypes);
    }


    @Test
    void testListLecturesFilteredByCourse() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));

        Map<String, String> filters = Map.of("course", "CS101");
        MetadataUtil.listLectures(reader, filters);

        System.setOut(System.out);
        List result = new ObjectMapper().readValue(out.toString(), List.class);
        assertEquals(
                List.of(Map.of("course_id", "CS101", "lecture_id", "1", "lecture_title", "Intro to Testing")),
                result
        );

    }



    @Test
    void testListLecturesAll() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));

        MetadataUtil.listLectures(reader, Collections.emptyMap());

        System.setOut(System.out);
        List result = new ObjectMapper().readValue(out.toString(), List.class);
        assertEquals(List.of(
                Map.of("course_id", "CS101", "lecture_id", "1", "lecture_title", "Intro to Testing"),
                Map.of("course_id", "CS102", "lecture_id", "2", "lecture_title", "Advanced Topics")
        ), result);

    }


}
