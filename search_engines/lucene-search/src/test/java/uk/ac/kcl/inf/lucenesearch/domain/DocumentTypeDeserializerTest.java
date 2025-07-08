package uk.ac.kcl.inf.lucenesearch.domain;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.module.SimpleModule;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DocumentTypeDeserializerTest {

    private final ObjectMapper mapper = new ObjectMapper();

    public DocumentTypeDeserializerTest() {
        SimpleModule module = new SimpleModule();
        module.addDeserializer(DocumentType.class, new DocumentTypeDeserializer());
        mapper.registerModule(module);
    }

    @Test
    void testDeserializePdfToSlide() throws Exception {
        String json = "\"pdf\"";
        DocumentType result = mapper.readValue(json, DocumentType.class);
        assertEquals(DocumentType.SLIDE, result);
    }

    @Test
    void testDeserializeMp4ToVideoTranscript() throws Exception {
        String json = "\"mp4\"";
        DocumentType result = mapper.readValue(json, DocumentType.class);
        assertEquals(DocumentType.VIDEO_TRANSCRIPT, result);
    }

    @Test
    void testDeserializeUnsupportedValueThrows() {
        String json = "\"docx\"";
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            mapper.readValue(json, DocumentType.class);
        });

        assertTrue(exception.getMessage().contains("Unsupported doc_type"));
    }
}
