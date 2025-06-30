package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.junit.jupiter.api.Test;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.usecase.DocumentProvider;

import java.io.InputStream;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class JsonFileDocumentProviderTest {

    @Test
    void loadDocuments_parsesJsonResourceCorrectly() throws Exception {
        // Get InputStream from test resources
        InputStream in = getClass().getClassLoader().getResourceAsStream("test-documents.json");
        assertNotNull(in, "Test JSON file should exist in src/test/resources");

        DocumentProvider provider = new JsonFileDocumentProvider(in);
        List<Document> documents = provider.loadDocuments();

        // Validate parsed documents
        assertEquals(2, documents.size());
        assertEquals("doc1", documents.get(0).documentId());
        assertEquals("Lucene is awesome", documents.get(0).content());
        assertEquals("doc2", documents.get(1).documentId());
        assertEquals("It supports indexing and searching", documents.get(1).content());
    }
}
