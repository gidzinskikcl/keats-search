package uk.ac.kcl.inf.lucenesearch.usecase;

import org.apache.lucene.queryparser.classic.ParseException;
import uk.ac.kcl.inf.lucenesearch.domain.SearchResult;

import java.util.List;

public interface SearchService {
    List<SearchResult> search(String query) throws ParseException;
}
