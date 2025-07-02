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
        if (args.length < 3 || args.length > 4) {
            System.err.println("Usage: java Application <path_to_documents.json> <query> <similarity> [param]");
            System.exit(1);
        }

        String docPath = args[0];
        String query = args[1];
        String similarityName = args[2];
        String param = args.length == 4 ? args[3] : null;

        Directory directory = LuceneConfig.getDirectory();
        List<SearchResult> results = getSearchResults(directory, docPath, query, similarityName, param);


        // Print results as JSON
        ObjectMapper mapper = new ObjectMapper();
        System.out.println(mapper.writeValueAsString(results));
    }

    private static List<SearchResult> getSearchResults(Directory directory, String docPath, String query, String similarityName, String similarityParams) throws Exception {
        Analyzer analyzer = LuceneConfig.getAnalyzer();
        IndexWriter writer = LuceneConfig.getWriter();

        org.apache.lucene.search.similarities.Similarity similarity = getSimilarityByName(similarityName, similarityParams);

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

    private static org.apache.lucene.search.similarities.Similarity getSimilarityByName(String name, String param) {
        name = name.toLowerCase();
        float defaultMu = 2000f;
        float defaultLambda = 0.7f;

        switch (name) {
            case "bm25":
                return new org.apache.lucene.search.similarities.BM25Similarity();

            case "classic":
                return new org.apache.lucene.search.similarities.ClassicSimilarity();

            case "boolean":
                return new org.apache.lucene.search.similarities.BooleanSimilarity();

            case "dirichlet":
                float mu = defaultMu;
                if (param != null) {
                    try {
                        String[] parts = param.split("=");
                        if (parts.length == 2 && parts[0].equals("mu")) {
                            mu = Float.parseFloat(parts[1]);
                        }
                    } catch (NumberFormatException e) {
                        System.err.println("Invalid mu parameter: " + param + ", using default " + defaultMu);
                    }
                }
                return new org.apache.lucene.search.similarities.LMDirichletSimilarity(mu);

            case "jm":
                float lambda = defaultLambda;
                if (param != null) {
                    try {
                        String[] parts = param.split("=");
                        if (parts.length == 2 && parts[0].equals("lambda")) {
                            lambda = Float.parseFloat(parts[1]);
                        }
                    } catch (NumberFormatException e) {
                        System.err.println("Invalid lambda parameter: " + param + ", using default " + defaultLambda);
                    }
                }
                return new org.apache.lucene.search.similarities.LMJelinekMercerSimilarity(lambda);

            default:
                throw new IllegalArgumentException("Unknown similarity: " + name);
        }
    }


}
