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
        if (args.length != 3) {
            System.err.println("Usage: java Application <path_to_documents.json> <query> <similarity>");
            System.exit(1);
        }

        String docPath = args[0];
        String query = args[1];
        String similarityName = args[2];

        Directory directory = LuceneConfig.getDirectory();
        List<SearchResult> results = getSearchResults(directory, docPath, query, similarityName);

        // Print results as JSON
        ObjectMapper mapper = new ObjectMapper();
        System.out.println(mapper.writeValueAsString(results));
    }

    private static List<SearchResult> getSearchResults(Directory directory, String docPath, String query, String similarityName) throws Exception {
        Analyzer analyzer = LuceneConfig.getAnalyzer();
        IndexWriter writer = LuceneConfig.getWriter();

        org.apache.lucene.search.similarities.Similarity similarity = getSimilarityByName(similarityName);

        IndexService indexService = new LuceneIndexService(writer);
        SearchService searchService = new LuceneSearchService(directory, analyzer, similarity, 10);

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

    private static org.apache.lucene.search.similarities.Similarity getSimilarityByName(String name) {
        return switch (name.toLowerCase()) {
            case "bm25" -> new org.apache.lucene.search.similarities.BM25Similarity();
            case "classic" -> new org.apache.lucene.search.similarities.ClassicSimilarity();
            case "dirichlet" -> new org.apache.lucene.search.similarities.LMDirichletSimilarity(2000f);
            case "jm" -> new org.apache.lucene.search.similarities.LMJelinekMercerSimilarity(0.7f);
            case "boolean" -> new org.apache.lucene.search.similarities.BooleanSimilarity();
            default -> throw new IllegalArgumentException("Unknown similarity: " + name);
        };
    }
}
