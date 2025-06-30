package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;
import uk.ac.kcl.inf.lucenesearch.usecase.SearchService;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class LuceneSearchService implements SearchService {
    private final Directory directory;
    private final Analyzer analyzer;
    private final int top_k;

    public LuceneSearchService(Directory directory, Analyzer analyzer, int top_k) {
        this.directory = directory;
        this.analyzer = analyzer;
        this.top_k = top_k;
    }

    @Override
    public List<SearchResult> search(String queryStr) throws ParseException {
        try (DirectoryReader reader = DirectoryReader.open(directory)) {
            IndexSearcher searcher = new IndexSearcher(reader);
            Query query = new QueryParser("content", analyzer).parse(queryStr);
            TopDocs hits = searcher.search(query, this.top_k);

            List<SearchResult> results = new ArrayList<>();
            for (ScoreDoc sd : hits.scoreDocs) {
                org.apache.lucene.document.Document doc = searcher.doc(sd.doc);
                results.add(new SearchResult(queryStr, doc.get("documentId"), doc.get("content"), sd.score));
            }
            return results;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
