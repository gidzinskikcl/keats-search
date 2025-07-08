package uk.ac.kcl.inf.lucenesearch;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import uk.ac.kcl.inf.lucenesearch.infrastructure.JsonFileDocumentProvider;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneConfig;
import uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneIndexService;
import uk.ac.kcl.inf.lucenesearch.usecase.IndexService;

import java.nio.file.Paths;

public class BM25IndexerApp {
    public static void main(String[] args) throws Exception {
        String docPath = args[0];
        String indexPath = args[1];

        Directory directory = FSDirectory.open(Paths.get(indexPath));
        Analyzer analyzer = LuceneConfig.getAnalyzer();
        IndexWriter writer = new IndexWriter(directory, new IndexWriterConfig(analyzer));

        IndexService indexService = new LuceneIndexService(writer);
        JsonFileDocumentProvider provider = new JsonFileDocumentProvider(docPath);
        for (Document doc : provider.loadDocuments()) {
            indexService.indexDocument(doc);
        }
        writer.close();
    }
}
