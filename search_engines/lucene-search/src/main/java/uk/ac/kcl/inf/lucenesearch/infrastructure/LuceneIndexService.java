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

        luceneDoc.add(new StringField("iD", doc.iD(), Field.Store.YES));
        luceneDoc.add(new StringField("documentId", doc.documentId(), Field.Store.YES));
        luceneDoc.add(new TextField("content", doc.content(), Field.Store.YES));

        // Dual indexing for title
        luceneDoc.add(new TextField("lectureTitle", doc.lectureTitle(), Field.Store.YES)); // for search
        luceneDoc.add(new StringField("lectureId", doc.lectureId(), Field.Store.YES)); // for filtering

        // Dual indexing for courseName
        luceneDoc.add(new TextField("courseName", doc.courseName(), Field.Store.YES));
        luceneDoc.add(new StringField("courseId", doc.courseId(), Field.Store.YES));

        luceneDoc.add(new StringField("type", doc.type().name(), Field.Store.YES));

        if (doc.start() != null) {
            luceneDoc.add(new StringField("start", doc.start(), Field.Store.YES));
        }

        if (doc.end() != null) {
            luceneDoc.add(new StringField("end", doc.end(), Field.Store.YES));
        }

        if (doc.pageNumber() != null) {
            luceneDoc.add(new StringField("pageNumber", String.valueOf(doc.pageNumber()), Field.Store.YES));
        }

        writer.addDocument(luceneDoc);
    }


}
