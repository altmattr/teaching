import java.util.List;
import java.util.Comparator;

public class Puzzle1 {

    // Starter: 216 characters (spaces and newlines count).
    // Return the words sorted by length, shortest first,
    // e.g. ["bbb","a","cc","dddd"] -> ["a","cc","bbb","dddd"].
    public static List<String> sortByLength(List<String> words) {
        words.sort(new Comparator<String>() {
            public int compare(String a, String b) {
                return Integer.compare(a.length(), b.length());
            }
        });
        return words;
    }
}