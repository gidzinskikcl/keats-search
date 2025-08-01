package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.search.similarities.Similarity;
import org.apache.lucene.search.similarities.BM25Similarity; // or any other
import org.apache.lucene.store.ByteBuffersDirectory;
import org.apache.lucene.store.Directory;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class LuceneSearchServiceTest {

    private Directory directory;
    private IndexWriter writer;
    private LuceneSearchService searchService;

    @BeforeEach
    void setup() throws Exception {
        directory = new ByteBuffersDirectory();

        // Optional: set the same analyzer used in your app
        StandardAnalyzer analyzer = new StandardAnalyzer();

        // Optional: use same similarity you want to test (BM25, Classic, etc.)
        Similarity similarity = new BM25Similarity();

        writer = new IndexWriter(directory, new IndexWriterConfig(analyzer));

        Document doc = new Document();
        doc.add(new StringField("documentId", "doc001", Field.Store.YES));
        doc.add(new TextField("content", "Lucene is a powerful search library", Field.Store.YES));
        doc.add(new TextField("courseName", "Information Retrieval", Field.Store.YES));
        doc.add(new TextField("lectureTitle", "Introduction to Lucene", Field.Store.YES));
        doc.add(new StringField("start", "00:00:00", Field.Store.YES));
        doc.add(new StringField("end", "00:01:00", Field.Store.YES));
        doc.add(new StringField("pageNumber", "1", Field.Store.YES));
        doc.add(new StringField("type", "SLIDES", Field.Store.YES));

        writer.addDocument(doc);
        writer.commit();

        // Updated constructor to include similarity
        searchService = new LuceneSearchService(directory, analyzer, similarity);
    }

    @AfterEach
    void cleanup() throws Exception {
        writer.close();
        directory.close();
    }

    @Test
    void testSearchReturnsExpectedDocument() throws Exception {
        List<SearchResult> results = searchService.search("lucene", 10, Map.of());

        assertEquals(1, results.size(), "Should return exactly one result");

        SearchResult observed = results.getFirst();
        assertEquals("doc001", observed.documentId(), "Returned document ID should match");
        assertEquals("Lucene is a powerful search library", observed.content(), "Search content should be tracked in result");
        assertTrue(observed.score() > 0.0f, "Search result should have a positive score");
        assertEquals("Information Retrieval", observed.courseName(), "Search results should have a course name");
        assertEquals("Introduction to Lucene", observed.lectureTitle(), "Search results should have a lecture title");
        assertEquals("00:00:00", observed.start(), "Start time should match");
        assertEquals("00:01:00", observed.end(), "End time should match");
        assertEquals("1", observed.pageNumber(), "Slide number should match");
        assertEquals("SLIDES", observed.type(), "Document type should match");

    }
}
