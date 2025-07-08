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
                        "id123",                    // iD
                        "doc123",                   // documentId
                        "Testing Lucene indexing",  // content
                        "00:00:00",                 // start
                        "00:01:00",                 // end
                        1,                          // pageNumber
                        "lecture_01",               // lectureId
                        "Lucene Test",              // lectureTitle
                        DocumentType.SLIDE,         // type
                        "CS101",                    // courseId
                        "Lucene Course"             // courseName
                );

        indexService.indexDocument(doc);
        writer.commit();

        try (DirectoryReader reader = DirectoryReader.open(directory)) {
            IndexSearcher searcher = new IndexSearcher(reader);
            TermQuery idQuery = new TermQuery(new Term("documentId", "doc123"));
            var hits = searcher.search(idQuery, 1);
            assertEquals(1, hits.totalHits.value);

            var storedDoc = searcher.doc(hits.scoreDocs[0].doc);
            assertEquals("doc123", storedDoc.get("documentId"));
            assertEquals("Testing Lucene indexing", storedDoc.get("content"));
            assertEquals("Lucene Test", storedDoc.get("lectureTitle"));
            assertEquals("00:00:00", storedDoc.get("start"));
            assertEquals("00:01:00", storedDoc.get("end"));
            assertEquals("lecture_01", storedDoc.get("lectureId"));
            assertEquals("CS101", storedDoc.get("courseId"));
            assertEquals("1", storedDoc.get("pageNumber"));
            assertEquals("SLIDE", storedDoc.get("type"));
            assertEquals("Lucene Course", storedDoc.get("courseName"));

            String[] keywords = storedDoc.getValues("keywords");
            assertEquals(0, keywords.length);
        }
    }



    @Test
    void indexDocumentHandlesNullStartAndEnd() throws Exception {
        uk.ac.kcl.inf.lucenesearch.domain.Document doc =
                new uk.ac.kcl.inf.lucenesearch.domain.Document(
                        "id456",                          // iD
                        "doc456",                         // documentId
                        "Lucene supports flexible schemas", // content
                        null,                             // start
                        null,                             // end
                        2,                                // pageNumber
                        "lecture_02",                     // lectureId
                        "Null Timestamps",                // lectureTitle
                        DocumentType.SLIDE,               // type
                        "CS102",                          // courseId
                        "Lucene Course"                   // courseName
                );

        indexService.indexDocument(doc);
        writer.commit();

        try (DirectoryReader reader = DirectoryReader.open(directory)) {
            IndexSearcher searcher = new IndexSearcher(reader);

            TermQuery idQuery = new TermQuery(new Term("documentId", "doc456"));
            var hits = searcher.search(idQuery, 1);
            assertEquals(1, hits.totalHits.value);

            var storedDoc = searcher.doc(hits.scoreDocs[0].doc);
            assertEquals("doc456", storedDoc.get("documentId"));
            assertEquals("Lucene supports flexible schemas", storedDoc.get("content"));
            assertEquals("Null Timestamps", storedDoc.get("lectureTitle"));
            assertEquals("lecture_02", storedDoc.get("lectureId"));
            assertEquals("CS102", storedDoc.get("courseId"));
            assertEquals("2", storedDoc.get("pageNumber"));
            assertEquals("Lucene Course", storedDoc.get("courseName"));
            assertEquals("SLIDE", storedDoc.get("type"));

            assertNull(storedDoc.get("start"));
            assertNull(storedDoc.get("end"));

            String[] keywords = storedDoc.getValues("keywords");
            // The keywords were not set, so expect empty array
            assertEquals(0, keywords.length);
        }
    }


}
