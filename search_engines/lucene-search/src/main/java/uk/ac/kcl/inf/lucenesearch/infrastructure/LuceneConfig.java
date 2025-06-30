package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.ByteBuffersDirectory;
import org.apache.lucene.store.Directory;

import java.io.IOException;

public class LuceneConfig {
    public static Directory directory = new ByteBuffersDirectory(); // use FSDirectory for persistence
    public static Analyzer analyzer = new StandardAnalyzer();
    private static IndexWriter writer;

    public static Analyzer getAnalyzer() {
        return analyzer;
    }

    public static Directory getDirectory() {
        return directory;
    }

    public static IndexWriter getWriter() throws IOException {
        if (writer == null) {
            IndexWriterConfig config = new IndexWriterConfig(analyzer);
            writer = new IndexWriter(directory, config);
        }
        return writer;
    }
}