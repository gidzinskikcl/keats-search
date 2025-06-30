package uk.ac.kcl.inf.lucenesearch.usecase;

import uk.ac.kcl.inf.lucenesearch.domain.Document;

public interface IndexService {
    void indexDocument(Document doc) throws Exception;
}