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
        luceneDoc.add(new TextField("title", doc.title(), Field.Store.YES));
        luceneDoc.add(new TextField("courseName", doc.courseName(), Field.Store.YES));
        luceneDoc.add(new StringField("type", doc.type().name(), Field.Store.YES));

        if (doc.start() != null) {
            luceneDoc.add(new StringField("start", doc.start(), Field.Store.YES));
        }

        if (doc.end() != null) {
            luceneDoc.add(new StringField("end", doc.end(), Field.Store.YES));
        }

        if (doc.speaker() != null) {
            luceneDoc.add(new StringField("speaker", doc.speaker(), Field.Store.YES));
        }

        if (doc.slideNumber() != null) {
            luceneDoc.add(new StringField("slideNumber", String.valueOf(doc.slideNumber()), Field.Store.YES));
        }
        if (doc.keywords() != null) {
            for (String keyword : doc.keywords()) {
                if (keyword != null && !keyword.isEmpty()) {
                    luceneDoc.add(new StringField("keywords", keyword, Field.Store.YES));
                }
            }
        }

        writer.addDocument(luceneDoc);
    }


}
