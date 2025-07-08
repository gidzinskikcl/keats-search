package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.*;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.store.ByteBuffersDirectory;
import org.apache.lucene.store.Directory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class LuceneSearchFilterServiceTest {
    private LuceneSearchFilterService searchService;

    @BeforeEach
    void setUp() throws Exception {
        Directory directory = new ByteBuffersDirectory();
        IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
        IndexWriter writer = new IndexWriter(directory, config);

        Document doc1 = new Document();
        doc1.add(new TextField("content", "Quick sort is a sorting algorithm", Field.Store.YES));
        doc1.add(new StringField("courseName_exact", "CS101", Field.Store.YES));
        doc1.add(new StringField("title_exact", "Lecture 1", Field.Store.YES));
        doc1.add(new StringField("documentId", "doc1", Field.Store.YES));
        doc1.add(new StringField("type", "VIDEO_TRANSCRIPT", Field.Store.YES));
        writer.addDocument(doc1);

        Document doc2 = new Document();
        doc2.add(new TextField("content", "Merge sort is useful", Field.Store.YES));
        doc2.add(new StringField("courseName_exact", "CS101", Field.Store.YES));
        doc2.add(new StringField("title_exact", "Lecture 2", Field.Store.YES));
        doc2.add(new StringField("documentId", "doc2", Field.Store.YES));
        doc2.add(new StringField("type", "VIDEO_TRANSCRIPT", Field.Store.YES));
        writer.addDocument(doc2);

        writer.close();

        searchService = new LuceneSearchFilterService(directory, new StandardAnalyzer(), new BM25Similarity());
    }

    @Test
    void testKeywordOnlySearch() throws Exception {
        List<SearchResult> results = searchService.search("quick sort", 10, Map.of());
        assertEquals(2, results.size());
        assertEquals("doc1", results.get(0).documentId());
        assertEquals("doc2", results.get(1).documentId());
    }


    @Test
    void testKeywordWithFilter() throws Exception {
        List<SearchResult> results = searchService.search(
                "sort",
                10,
                Map.of("title_exact", List.of("Lecture 1"))
        );
        assertEquals(1, results.size());
        assertEquals("doc1", results.get(0).documentId());
    }

    @Test
    void testFilterNoMatch() throws Exception {
        List<SearchResult> results = searchService.search(
                "sort",
                10,
                Map.of("title_exact", List.of("Lecture 3"))
        );
        assertEquals(0, results.size());
    }

}
