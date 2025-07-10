package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.similarities.Similarity;
import org.apache.lucene.store.Directory;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;
import uk.ac.kcl.inf.lucenesearch.usecase.SearchService;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class LuceneSearchFilterService implements SearchService {
    private final Directory directory;
    private final Analyzer analyzer;
    private final Similarity similarity;

    public LuceneSearchFilterService(Directory directory, Analyzer analyzer, Similarity similarity) {
        this.directory = directory;
        this.analyzer = analyzer;
        this.similarity = similarity;
    }

    @Override
    public List<SearchResult> search(String queryStr, int topK, Map<String, List<String>> filters) throws ParseException
    {
        try (DirectoryReader reader = DirectoryReader.open(directory)) {
            IndexSearcher searcher = new IndexSearcher(reader);
            searcher.setSimilarity(this.similarity);

            // Construct combined query
            BooleanQuery.Builder booleanQuery = new BooleanQuery.Builder();

            // Main content query
            String escapedQuery = QueryParser.escape(queryStr);
            Query contentQuery = new QueryParser("content", analyzer).parse(escapedQuery);
            booleanQuery.add(contentQuery, BooleanClause.Occur.MUST);

            // Add filters as exact matches
            for (Map.Entry<String, List<String>> entry : filters.entrySet()) {
                BooleanQuery.Builder subQuery = new BooleanQuery.Builder();
                for (String value : entry.getValue()) {
                    subQuery.add(new TermQuery(new Term(entry.getKey(), value)), BooleanClause.Occur.SHOULD);
                }
                booleanQuery.add(subQuery.build(), BooleanClause.Occur.FILTER);
            }

            // Execute combined query
            TopDocs hits = searcher.search(booleanQuery.build(), topK);

            List<SearchResult> results = new ArrayList<>();
            for (ScoreDoc sd : hits.scoreDocs) {
                org.apache.lucene.document.Document doc = searcher.doc(sd.doc);

                results.add(new SearchResult(
                        sd.score,
                        doc.get("iD"),
                        doc.get("documentId"),
                        doc.get("content"),
                        doc.get("courseId"),
                        doc.get("courseName"),
                        doc.get("lectureId"),
                        doc.get("lectureTitle"),
                        doc.get("start"),
                        doc.get("end"),
                        doc.get("pageNumber"),
                        doc.get("type"),
                        doc.get("url"),
                        doc.get("thumbnailUrl")
                ));
            }

            return results;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
