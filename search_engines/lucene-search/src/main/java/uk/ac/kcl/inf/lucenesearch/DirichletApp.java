package uk.ac.kcl.inf.lucenesearch;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.search.similarities.LMDirichletSimilarity;
import org.apache.lucene.store.Directory;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;
import uk.ac.kcl.inf.lucenesearch.infrastructure.JsonFileDocumentProvider;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneConfig;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneIndexService;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneSearchService;
import uk.ac.kcl.inf.lucenesearch.usecase.IndexService;
import uk.ac.kcl.inf.lucenesearch.usecase.SearchService;

import java.util.List;
import java.util.Map;

public class DirichletApp {
    public static void main(String[] args) throws Exception {
        if (args.length != 4) {
            System.err.println("Usage: java DirichletApp <path_to_documents.json> <query> <top_k> <mu>");
            System.exit(1);
        }

        String docPath = args[0];
        String query = args[1];

        int topK;
        float mu;

        try {
            topK = Integer.parseInt(args[2]);
            if (topK <= 0) {
                throw new NumberFormatException("top_k must be > 0");
            }
        } catch (NumberFormatException e) {
            System.err.println("Invalid top_k value: " + args[2]);
            System.exit(1);
            return;
        }

        try {
            mu = Float.parseFloat(args[3]);
            if (mu <= 0) {
                throw new NumberFormatException("mu must be > 0");
            }
        } catch (NumberFormatException e) {
            System.err.println("Invalid mu value: " + args[3]);
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

        SearchService searchService = new LuceneSearchService(directory, analyzer, new LMDirichletSimilarity(mu));
        List<SearchResult> results = searchService.search(query, topK, Map.of());

        ObjectMapper mapper = new ObjectMapper();
        System.out.println(mapper.writeValueAsString(results));
    }
}
