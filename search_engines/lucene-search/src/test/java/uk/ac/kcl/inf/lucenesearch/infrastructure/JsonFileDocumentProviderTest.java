package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.junit.jupiter.api.Test;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.DocumentType;
import uk.ac.kcl.inf.lucenesearch.usecase.DocumentProvider;

import java.io.InputStream;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class JsonFileDocumentProviderTest {

    @Test
    void loadDocuments_parsesJsonResourceCorrectly() throws Exception {
        // Get file path from resources
        var resourceUrl = getClass().getClassLoader().getResource("test-documents.json");
        assertNotNull(resourceUrl, "Test JSON file should exist in src/test/resources");

        String path = resourceUrl.getPath();
        DocumentProvider provider = new JsonFileDocumentProvider(path);
        List<Document> documents = provider.loadDocuments();

        assertEquals(2, documents.size());

        Document doc1 = documents.get(0);
        assertEquals("doc1", doc1.documentId());
        assertEquals("Lucene is awesome", doc1.content());
        assertEquals("Intro to Lucene", doc1.title());
        assertEquals("00:00:00", doc1.start());
        assertEquals("00:01:00", doc1.end());
        assertEquals("Dr. Smith", doc1.speaker());
        assertEquals(1, doc1.slideNumber());
        assertEquals(List.of("lucene", "intro"), doc1.keywords());
        assertEquals(DocumentType.SLIDE, doc1.type());
        assertEquals("Information Retrieval", doc1.courseName());

        Document doc2 = documents.get(1);
        assertEquals("doc2", doc2.documentId());
        assertEquals("It supports indexing and searching", doc2.content());
        assertEquals("Lucene Features", doc2.title());
        assertNull(doc2.start());
        assertNull(doc2.end());
        assertNull(doc2.speaker());
        assertEquals(2, doc2.slideNumber());
        assertEquals(List.of(), doc2.keywords());
        assertEquals(DocumentType.SLIDE, doc2.type());
        assertEquals("Information Retrieval", doc2.courseName());

    }

}
