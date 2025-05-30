package uk.ac.kcl.inf.gidzinski.keatssearch;

public class SearchResult {
    private final String documentId;
    private final int rank;
    private final double score;

    public SearchResult(String documentId, int rank, double score) {
        this.documentId = documentId;
        this.rank = rank;
        this.score = score;
    }
    public String getDocumentId() {
        return documentId;
    }
    public int getRank() {
        return rank;
    }
    public double getScore() {
        return score;
    }
}
