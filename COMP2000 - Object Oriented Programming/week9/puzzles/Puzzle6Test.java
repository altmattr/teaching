import static org.junit.Assert.*;
import org.junit.Test;
import java.util.*;

public class Puzzle6Test {

    @Test
    public void reversesEveryWord() {
        List<String> words = new ArrayList<>(Arrays.asList("hi", "cat"));
        assertEquals(Arrays.asList("ih", "tac"), Puzzle6.reversed(words));
    }

    @Test
    public void palindromesAreUnchanged() {
        List<String> words = new ArrayList<>(Arrays.asList("kayak", "noon"));
        assertEquals(Arrays.asList("kayak", "noon"), Puzzle6.reversed(words));
    }

    @Test
    public void emptyGivesEmpty() {
        List<String> words = new ArrayList<>();
        assertEquals(Collections.emptyList(), Puzzle6.reversed(words));
    }

    @Test
    public void mixedLengthWordsReverse() {
        List<String> words = new ArrayList<>(Arrays.asList("a", "tool", "stressed"));
        assertEquals(Arrays.asList("a", "loot", "desserts"), Puzzle6.reversed(words));
    }
}