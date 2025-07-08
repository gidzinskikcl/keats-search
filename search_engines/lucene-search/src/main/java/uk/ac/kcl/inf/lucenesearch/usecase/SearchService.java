package uk.ac.kcl.inf.lucenesearch.usecase;

import org.apache.lucene.queryparser.classic.ParseException;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;

import java.util.List;
import java.util.Map;

public interface SearchService {
    List<SearchResult> search(String queryStr, int topK, Map<String, List<String>> filters) throws ParseException;
}
