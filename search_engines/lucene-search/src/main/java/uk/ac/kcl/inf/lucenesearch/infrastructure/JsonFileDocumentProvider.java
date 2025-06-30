package uk.ac.kcl.inf.lucenesearch.infrastructure;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.usecase.DocumentProvider;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.List;

public class JsonFileDocumentProvider implements DocumentProvider {
    private final String filePath;
    private final ObjectMapper objectMapper;

    public JsonFileDocumentProvider(String filePath) {
        this.filePath = filePath;
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public List<Document> loadDocuments() throws Exception {
        try (InputStream in = new FileInputStream(filePath)) {
            return objectMapper.readValue(in, new TypeReference<>() {});
        }
    }
}
