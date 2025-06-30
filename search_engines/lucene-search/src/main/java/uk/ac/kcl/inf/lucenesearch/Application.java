package uk.ac.kcl.inf.lucenesearch;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.store.Directory;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;
import uk.ac.kcl.inf.lucenesearch.infrastructure.JsonFileDocumentProvider;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneConfig;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneIndexService;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneSearchService;
import uk.ac.kcl.inf.lucenesearch.usecase.IndexService;
import uk.ac.kcl.inf.lucenesearch.usecase.SearchService;

import java.io.InputStream;
import java.util.List;

public class Application {
    public static void main(String[] args) throws Exception {
        // Setup config
        Directory directory = LuceneConfig.getDirectory();
        Analyzer analyzer = LuceneConfig.getAnalyzer();
        IndexWriter writer = LuceneConfig.getWriter();

        IndexService indexService = new LuceneIndexService(writer);
        SearchService searchService = new LuceneSearchService(directory, analyzer, 10);

        // Load from resources
        InputStream in = Application.class.getClassLoader().getResourceAsStream("documents.json");
        if (in == null) {
            throw new RuntimeException("Could not find documents.json in resources");
        }

        JsonFileDocumentProvider provider = new JsonFileDocumentProvider(in);
        List<Document> documents = provider.loadDocuments();

        // Index the loaded documents
        for (Document doc : documents) {
            indexService.indexDocument(doc);
        }

        writer.close(); // commit & close writer

        // Run a search
        String query = "this";
        List<SearchResult> results = searchService.search(query);

        // Print results
        System.out.println("Search results for: " + query);
        for (SearchResult result : results) {
            System.out.printf("- [%s] %s (score: %.3f)%n", result.query(), result.documentId(), result.score());
        }
    }
}
