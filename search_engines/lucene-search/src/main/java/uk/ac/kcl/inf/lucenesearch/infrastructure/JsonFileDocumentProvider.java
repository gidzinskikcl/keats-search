package uk.ac.kcl.inf.lucenesearch.infrastructure;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.usecase.DocumentProvider;

import java.io.InputStream;
import java.util.List;

public class JsonFileDocumentProvider implements DocumentProvider {
    private final InputStream inputStream;
    private final ObjectMapper objectMapper;

    public JsonFileDocumentProvider(InputStream inputStream) {
        this.inputStream = inputStream;
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public List<Document> loadDocuments() throws Exception {
        return objectMapper.readValue(inputStream, new TypeReference<>() {});
    }
}
