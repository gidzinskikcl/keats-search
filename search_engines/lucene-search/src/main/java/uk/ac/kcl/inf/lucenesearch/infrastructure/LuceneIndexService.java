package uk.ac.kcl.inf.lucenesearch.infrastructure;

import org.apache.lucene.document.StringField;
import uk.ac.kcl.inf.lucenesearch.domain.Document;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import uk.ac.kcl.inf.lucenesearch.usecase.IndexService;

public class LuceneIndexService implements IndexService {
    private final IndexWriter writer;

    public LuceneIndexService(IndexWriter indexWriter) {
        this.writer = indexWriter;
    }

    @Override
    public void indexDocument(Document doc) throws Exception {
        org.apache.lucene.document.Document luceneDoc = new org.apache.lucene.document.Document();
        luceneDoc.add(new StringField("documentId", doc.documentId(), Field.Store.YES));
        luceneDoc.add(new TextField("content", doc.content(), Field.Store.YES));
        writer.addDocument(luceneDoc);
    }
}
