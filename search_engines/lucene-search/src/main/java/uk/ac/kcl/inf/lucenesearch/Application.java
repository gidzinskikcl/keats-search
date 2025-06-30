package uk.ac.kcl.inf.lucenesearch;

import com.fasterxml.jackson.databind.ObjectMapper;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;
import uk.ac.kcl.inf.lucenesearch.infrastructure.JsonFileDocumentProvider;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneConfig;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneIndexService;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneSearchService;
import uk.ac.kcl.inf.lucenesearch.usecase.IndexService;
import uk.ac.kcl.inf.lucenesearch.usecase.SearchService;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.store.Directory;

import java.util.List;

public class Application {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: java Application <path_to_documents.json> <query>");
            System.exit(1);
        }

        String docPath = args[0];
        String query = args[1];

        Directory directory = LuceneConfig.getDirectory();
        List<SearchResult> results = getSearchResults(directory, docPath, query);

        // Print results as JSON
        ObjectMapper mapper = new ObjectMapper();
        System.out.println(mapper.writeValueAsString(results));
    }

    private static List<SearchResult> getSearchResults(Directory directory, String docPath, String query) throws Exception {
        Analyzer analyzer = LuceneConfig.getAnalyzer();
        IndexWriter writer = LuceneConfig.getWriter();

        IndexService indexService = new LuceneIndexService(writer);
        SearchService searchService = new LuceneSearchService(directory, analyzer, 10);

        // Load documents from file path
        JsonFileDocumentProvider provider = new JsonFileDocumentProvider(docPath);
        List<Document> documents = provider.loadDocuments();

        for (Document doc : documents) {
            indexService.indexDocument(doc);
        }

        writer.close();

        List<SearchResult> results = searchService.search(query);
        return results;
    }
}
