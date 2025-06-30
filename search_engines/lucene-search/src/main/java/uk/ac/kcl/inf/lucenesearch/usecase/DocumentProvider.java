package uk.ac.kcl.inf.lucenesearch.usecase;

import uk.ac.kcl.inf.lucenesearch.domain.Document;

import java.util.List;

public interface DocumentProvider {
    List<Document> loadDocuments() throws Exception;
}
