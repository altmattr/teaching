import java.util.List;

public class Puzzle6 {

    // Starter: 166 characters (spaces and newlines count).
    // Return every word reversed,
    // e.g. ["hi","cat"] -> ["ih","tac"].
    public static List<String> reversed(List<String> words) {
        for (int i = 0; i < words.size(); i++) {
            words.set(i, new StringBuilder(words.get(i)).reverse().toString());
        }
        return words;
    }
}