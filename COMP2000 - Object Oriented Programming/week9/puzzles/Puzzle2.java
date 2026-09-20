import java.util.List;
import java.util.Comparator;

public class Puzzle2 {

    // Starter: 201 characters (spaces and newlines count).
    // Return the words sorted ignoring case,
    // e.g. ["b","A","a","B"] -> ["A","a","b","B"].
    public static List<String> sortIgnoreCase(List<String> words) {
        words.sort(new Comparator<String>() {
            public int compare(String a, String b) {
                return a.compareToIgnoreCase(b);
            }
        });
        return words;
    }
}