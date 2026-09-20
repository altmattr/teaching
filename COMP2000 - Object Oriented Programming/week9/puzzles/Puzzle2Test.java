import static org.junit.Assert.*;
import org.junit.Test;
import java.util.*;

public class Puzzle2Test {

    @Test
    public void sortsIgnoringCase() {
        List<String> words = new ArrayList<>(Arrays.asList("b", "A", "a", "B"));
        assertEquals(Arrays.asList("A", "a", "b", "B"), Puzzle2.sortIgnoreCase(words));
    }

    @Test
    public void mixedWordsSortedCaseInsensitively() {
        List<String> words = new ArrayList<>(Arrays.asList("Zoom", "apple", "Mango", "kiwi"));
        assertEquals(Arrays.asList("apple", "kiwi", "Mango", "Zoom"),
                Puzzle2.sortIgnoreCase(words));
    }

    @Test
    public void emptyGivesEmpty() {
        List<String> words = new ArrayList<>();
        assertEquals(Collections.emptyList(), Puzzle2.sortIgnoreCase(words));
    }

    @Test
    public void singleWordIsUnchanged() {
        List<String> words = new ArrayList<>(Collections.singletonList("Hello"));
        assertEquals(Collections.singletonList("Hello"), Puzzle2.sortIgnoreCase(words));
    }
}