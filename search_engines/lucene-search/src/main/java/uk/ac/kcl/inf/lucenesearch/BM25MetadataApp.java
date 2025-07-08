package uk.ac.kcl.inf.lucenesearch;

import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.store.FSDirectory;
import uk.ac.kcl.inf.lucenesearch.infrastructure.MetadataUtil;

import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Map;

public class BM25MetadataApp {
    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.err.println("Usage: meta courses|files <indexPath> [--course ID] [--lecture NUM]");
            System.exit(1);
        }

        String command = args[0];
        String indexPath = args[1];
        Map<String, String> filters = MetadataUtil.parseFilters(Arrays.copyOfRange(args, 2, args.length));

        try (DirectoryReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexPath)))) {
            switch (command) {
                case "courses" -> MetadataUtil.listCourses(reader);
                case "lectures" -> MetadataUtil.listLectures(reader, filters);
                case "files" -> MetadataUtil.listFiles(reader, filters);
                default -> {
                    System.err.println("Unknown meta command: " + command);
                    System.exit(1);
                }
            }
        }
    }
}