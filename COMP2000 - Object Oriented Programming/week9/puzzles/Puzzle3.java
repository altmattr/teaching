import java.util.List;
import java.util.Iterator;

public class Puzzle3 {

    // Starter: 169 characters (spaces and newlines count).
    // Return only the words with 3 or more letters,
    // e.g. ["a","bb","ccc","dddd"] -> ["ccc","dddd"].
    public static List<String> dropShort(List<String> words) {
        Iterator<String> it = words.iterator();
        while (it.hasNext()) {
            if (it.next().length() < 3) it.remove();
        }
        return words;
    }
}