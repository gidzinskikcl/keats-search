package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.store.ByteBuffersDirectory;
import org.apache.lucene.store.Directory;
import org.apache.lucene.index.Term;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import uk.ac.kcl.inf.lucenesearch.domain.DocumentType;
import uk.ac.kcl.inf.lucenesearch.usecase.IndexService;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class LuceneIndexServiceTest {
    private Directory directory;
    private IndexWriter writer;
    private IndexService indexService;

    @BeforeEach
    void setup() throws Exception {
        directory = new ByteBuffersDirectory();
        writer = new IndexWriter(directory, new IndexWriterConfig(new StandardAnalyzer()));
        indexService = new LuceneIndexService(writer);
    }

    @AfterEach
    void cleanup() throws Exception {
        writer.close();
        directory.close();
    }

    @Test
    void indexDocumentTest() throws Exception {
        uk.ac.kcl.inf.lucenesearch.domain.Document doc =
                new uk.ac.kcl.inf.lucenesearch.domain.Document(
                        "doc123",               // documentId
                        "Testing Lucene indexing",        // content
                        "Lucene Test",                    // title
                        "00:00:00",                       // start
                        "00:01:00",                       // end
                        "",                             // speaker
                        1,                              // slideNumber
                        List.of(),        // keywords
                        DocumentType.SLIDE,               // type
                        "Lucene Course"                // courseName
                );

        indexService.indexDocument(doc);
        writer.commit();

        try (DirectoryReader reader = DirectoryReader.open(directory)) {
            IndexSearcher searcher = new IndexSearcher(reader);
            // Check by ID
            TermQuery idQuery = new TermQuery(new Term("documentId", "doc123"));
            var hits = searcher.search(idQuery, 1);
            assertEquals(1, hits.totalHits.value, "Should find doc by ID");

            var storedDoc = searcher.doc(hits.scoreDocs[0].doc);
            assertEquals("doc123", storedDoc.get("documentId"), "Document ID should match");
            assertEquals("Testing Lucene indexing", storedDoc.get("content"), "Stored content should match");
            assertEquals("Lucene Test", storedDoc.get("title"), "Title should match");
            assertEquals("00:00:00", storedDoc.get("start"), "Start timestamp should match");
            assertEquals("00:01:00", storedDoc.get("end"), "End timestamp should match");
            assertEquals("", storedDoc.get("speaker"), "Speaker should be an empty string");
            assertEquals("1", storedDoc.get("slideNumber"), "Slide number should match");
            assertEquals("SLIDE", storedDoc.get("type"), "Document type should match");
            assertEquals("Lucene Course", storedDoc.get("courseName"), "Course name should match");

            // Keywords: empty list means no "keywords" field added
            String[] keywords = storedDoc.getValues("keywords");
            assertEquals(0, keywords.length, "Keywords should be empty");
        }
    }


    @Test
    void indexDocumentHandlesNullStartAndEnd() throws Exception {
        uk.ac.kcl.inf.lucenesearch.domain.Document doc =
                new uk.ac.kcl.inf.lucenesearch.domain.Document(
                        "doc456",                           // documentId
                        "Lucene supports flexible schemas", // content
                        "Lucene Null Timestamps",           // title
                        null,                               // start
                        null,                               // end
                        "Dr. Null",                         // speaker
                        2,                                  // slideNumber
                        List.of("lucene", "schema"),        // keywords
                        DocumentType.SLIDE,                 // type
                        "Lucene Course"                     // courseName
                );

        indexService.indexDocument(doc);
        writer.commit();

        try (DirectoryReader reader = DirectoryReader.open(directory)) {
            IndexSearcher searcher = new IndexSearcher(reader);

            TermQuery idQuery = new TermQuery(new Term("documentId", "doc456"));
            var hits = searcher.search(idQuery, 1);
            assertEquals(1, hits.totalHits.value, "Should find doc by ID");

            var storedDoc = searcher.doc(hits.scoreDocs[0].doc);

            // Check all stored fields
            assertEquals("doc456", storedDoc.get("documentId"), "Document ID should match");
            assertEquals("Lucene supports flexible schemas", storedDoc.get("content"), "Content should match");
            assertEquals("Lucene Null Timestamps", storedDoc.get("title"), "Title should match");
            assertEquals("Dr. Null", storedDoc.get("speaker"), "Speaker should match");
            assertEquals("2", storedDoc.get("slideNumber"), "Slide number should match");
            assertEquals("Lucene Course", storedDoc.get("courseName"), "Course name should match");
            assertEquals("SLIDE", storedDoc.get("type"), "Document type should match");

            // These should be null because they were not stored
            assertNull(storedDoc.get("start"), "Start timestamp should be null");
            assertNull(storedDoc.get("end"), "End timestamp should be null");

            // Keywords should contain the correct values
            String[] keywords = storedDoc.getValues("keywords");
            assertArrayEquals(new String[] {"lucene", "schema"}, keywords, "Keywords should match");
        }
    }

}
