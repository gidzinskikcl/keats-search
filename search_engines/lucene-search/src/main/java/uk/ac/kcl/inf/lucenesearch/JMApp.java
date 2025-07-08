package uk.ac.kcl.inf.lucenesearch;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.lucene.search.similarities.LMJelinekMercerSimilarity;
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
import java.util.Map;

public class JMApp {
    public static void main(String[] args) throws Exception {
        if (args.length != 4) {
            System.err.println("Usage: java JMApp <path_to_documents.json> <query> <top_k> <lambda>");
            System.exit(1);
        }
        String docPath = args[0];
        String query = args[1];

        int topK;
        float lambda;
        try {
            topK = Integer.parseInt(args[2]);
            if (topK <= 0) {
                throw new NumberFormatException();
            }
        } catch (NumberFormatException e) {
            System.err.println("Invalid top_k value: " + args[2] + " (must be a positive integer)");
            System.exit(1);
            return; // Unreachable, but required for compilation
        }


        try {
            lambda = Float.parseFloat(args[3]);
            if (lambda <= 0 || lambda >= 1) {
                throw new NumberFormatException("lambda must be between 0 and 1 (exclusive)");
            }
        } catch (NumberFormatException e) {
            System.err.println("Invalid lambda value: " + args[3]);
            System.exit(1);
            return;
        }

        Directory directory = LuceneConfig.getDirectory();
        Analyzer analyzer = LuceneConfig.getAnalyzer();
        IndexWriter writer = LuceneConfig.getWriter();

        IndexService indexService = new LuceneIndexService(writer);
        JsonFileDocumentProvider provider = new JsonFileDocumentProvider(docPath);
        List<Document> documents = provider.loadDocuments();
        for (Document doc : documents) indexService.indexDocument(doc);
        writer.close();

        SearchService searchService = new LuceneSearchService(directory, analyzer, new LMJelinekMercerSimilarity(lambda));
        List<SearchResult> results = searchService.search(query, topK, Map.of());

        ObjectMapper mapper = new ObjectMapper();
        System.out.println(mapper.writeValueAsString(results));
    }
}
