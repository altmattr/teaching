import java.util.List;
import java.util.Comparator;
import java.util.Iterator;

public class Puzzle5 {

    // Starter: 471 characters (spaces and newlines count).
    // Shout every word, drop the words shorter than 3 letters,
    // then sort the survivors by length, shortest first,
    // e.g. ["banana","hi","apple","a"] -> ["APPLE","BANANA"].
    public static List<String> normalize(List<String> words) {
        for (int i = 0; i < words.size(); i++) {
            words.set(i, words.get(i).toUpperCase());
        }
        Iterator<String> it = words.iterator();
        while (it.hasNext()) {
            if (it.next().length() < 3) it.remove();
        }
        words.sort(new Comparator<String>() {
            public int compare(String a, String b) {
                return Integer.compare(a.length(), b.length());
            }
        });
        return words;
    }
}