package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.junit.jupiter.api.Test;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.DocumentType;
import uk.ac.kcl.inf.lucenesearch.usecase.DocumentProvider;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class JsonFileDocumentProviderTest {

    @Test
    void loadDocuments_parsesJsonResourceCorrectly() throws Exception {
        var resourceUrl = getClass().getClassLoader().getResource("test-documents.json");
        assertNotNull(resourceUrl, "Test JSON file should exist in src/test/resources");

        String path = resourceUrl.getPath();
        DocumentProvider provider = new JsonFileDocumentProvider(path);
        List<Document> documents = provider.loadDocuments();

        assertEquals(2, documents.size());

        Document expectedDoc1 = new Document(
                "0",
                "doc1",
                "Lucene is awesome",
                "00:00:00",
                "00:01:00",
                1,
                "lecture1",
                "Intro to Lucene",
                DocumentType.SLIDE,
                "CS101",
                "Information Retrieval"
        );

        Document expectedDoc2 = new Document(
                "1",
                "doc2",
                "It supports indexing and searching",
                null,
                null,
                2,
                "lecture1",
                "Lucene Features",
                DocumentType.SLIDE,
                "CS101",
                "Information Retrieval"
        );

        assertEquals(expectedDoc1, documents.get(0));
        assertEquals(expectedDoc2, documents.get(1));
    }


}
