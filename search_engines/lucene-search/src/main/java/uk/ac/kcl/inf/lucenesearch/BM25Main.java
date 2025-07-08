package uk.ac.kcl.inf.lucenesearch;

import java.util.Arrays;

public class BM25Main {
    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.err.println("Usage: --mode index|search|meta ...");
            System.exit(1);
        }

        if (args[0].equals("--mode")) {
            switch (args[1]) {
                case "index" -> BM25IndexerApp.main(Arrays.copyOfRange(args, 2, args.length));
                case "search" -> BM25App.main(Arrays.copyOfRange(args, 2, args.length));
                case "meta" -> BM25MetadataApp.main(Arrays.copyOfRange(args, 2, args.length));
                default -> {
                    System.err.println("Unknown mode: " + args[1]);
                    System.exit(1);
                }
            }
        } else {
            System.err.println("Missing --mode flag");
            System.exit(1);
        }
    }
}
