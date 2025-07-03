package uk.ac.kcl.inf.lucenesearch;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.lucene.search.similarities.ClassicSimilarity;
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

public class TFIDFApp {
    public static void main(String[] args) throws Exception {
        if (args.length < 3) {
            System.err.println("Usage: java TFIDFApp <path_to_documents.json> <query> <top_k>");
            System.exit(1);
        }

        String docPath = args[0];
        String query = args[1];
        // Required: top_k
        int topK;
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

        Directory directory = LuceneConfig.getDirectory();
        Analyzer analyzer = LuceneConfig.getAnalyzer();
        IndexWriter writer = LuceneConfig.getWriter();

        IndexService indexService = new LuceneIndexService(writer);
        JsonFileDocumentProvider provider = new JsonFileDocumentProvider(docPath);
        List<Document> documents = provider.loadDocuments();
        for (Document doc : documents) indexService.indexDocument(doc);
        writer.close();

        SearchService searchService = new LuceneSearchService(directory, analyzer, new ClassicSimilarity(), topK);
        List<SearchResult> results = searchService.search(query);

        ObjectMapper mapper = new ObjectMapper();
        System.out.println(mapper.writeValueAsString(results));
    }
}
