package uk.ac.kcl.inf.lucenesearch;

import org.apache.lucene.store.NIOFSDirectory;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.store.FSDirectory;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneSearchFilterService;
import uk.ac.kcl.inf.lucenesearch.usecase.SearchService;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.store.Directory;
import org.apache.lucene.analysis.standard.StandardAnalyzer;

import java.nio.file.Paths;
import java.util.*;

public class BM25App {
    public static void main(String[] args) throws Exception {
        if (args.length < 3) {
            System.err.println("Usage: java BM25App <path_to_index_dir> <query> <filter_json>");
            System.exit(1);
        }

        String indexPath = args[0];
        String query = args[1];
        int topK;

        try {
            topK = Integer.parseInt(args[2]);
            if (topK <= 0) {
                throw new NumberFormatException();
            }
        } catch (NumberFormatException e) {
            System.err.println("Invalid top_k value: " + args[2] + " (must be a positive integer)");
            System.exit(1);
            return;
        }

        // Deserialize filter JSON (passed as 4th argument)
        String filterJson = args[3];
        ObjectMapper mapper = new ObjectMapper();
        Map<String, List<String>> filters = mapper.readValue(
                filterJson,
                mapper.getTypeFactory().constructMapType(Map.class, String.class, List.class)
        );

//        Directory directory = FSDirectory.open(Paths.get(indexPath));
        Directory directory = new NIOFSDirectory(Paths.get(indexPath));
        Analyzer analyzer = new StandardAnalyzer();
        SearchService searchService = new LuceneSearchFilterService(directory, analyzer, new BM25Similarity());
        List<SearchResult> results = searchService.search(query, topK, filters);

        System.out.println(mapper.writeValueAsString(results));
    }
}
