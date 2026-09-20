import static org.junit.Assert.*;
import org.junit.Test;
import java.util.*;

public class Puzzle5Test {

    @Test
    public void shoutsDropsShortAndSortsByLength() {
        List<String> words = new ArrayList<>(Arrays.asList("banana", "hi", "apple", "a"));
        assertEquals(Arrays.asList("APPLE", "BANANA"), Puzzle5.normalize(words));
    }

    @Test
    public void allShortGivesEmpty() {
        List<String> words = new ArrayList<>(Arrays.asList("x", "hi"));
        assertEquals(Collections.emptyList(), Puzzle5.normalize(words));
    }

    @Test
    public void emptyGivesEmpty() {
        List<String> words = new ArrayList<>();
        assertEquals(Collections.emptyList(), Puzzle5.normalize(words));
    }

    @Test
    public void alreadyNormalizedIsUnchanged() {
        List<String> words = new ArrayList<>(Arrays.asList("BBB", "CCCC", "A", "DDDD"));
        assertEquals(Arrays.asList("BBB", "CCCC", "DDDD"), Puzzle5.normalize(words));
    }
}