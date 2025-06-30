package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.store.ByteBuffersDirectory;
import org.apache.lucene.store.Directory;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Test;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;
import static uk.ac.kcl.inf.lucenesearch.infrastructure.LuceneConfig.analyzer;

public class LuceneConfigTest {

    @Test
    void testAnalyzer() {
        assertNotNull(LuceneConfig.getAnalyzer(), "Analyzer should not be null");
        assertInstanceOf(StandardAnalyzer.class, analyzer, "Analyzer should be StandardAnalyzer");
    }

    @Test
    void testDirectory() {
        Directory dir = LuceneConfig.getDirectory();
        assertNotNull(dir, "Directory should not be null");
        assertInstanceOf(ByteBuffersDirectory.class, dir, "Directory should be ByteBuffersDirectory");
    }

    @Test
    void testWriter() throws IOException {
        var writer1 = LuceneConfig.getWriter();
        var writer2 = LuceneConfig.getWriter();
        assertNotNull(writer1, "Writer should not be null");
        assertSame(writer1, writer2, "Writer should be a singleton");
        assertInstanceOf(IndexWriter.class, writer1, "Writer should be an IndexWriter");
    }

    @AfterAll
    static void cleanup() throws IOException {
        var writer = LuceneConfig.getWriter();
        writer.close();
        LuceneConfig.getDirectory().close();
    }
}
