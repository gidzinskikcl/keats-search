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
                        "doc123",                          // documentId
                        "Testing Lucene indexing",        // content
                        "Lucene Test",                    // title
                        null,                             // timestamp
                        null,                             // speaker
                        null,                             // slideNumber
                        List.of("lucene", "test"),        // keywords (or List.of())
                        DocumentType.SLIDE, // type,
                        "Lucene Course" // courseName
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
            assertEquals("Testing Lucene indexing", storedDoc.get("content"), "Stored content should match");
        }
    }
}
