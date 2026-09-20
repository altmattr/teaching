import static org.junit.Assert.*;
import org.junit.Test;
import java.util.*;

public class Puzzle1Test {

    @Test
    public void sortsByLengthShortestFirst() {
        List<String> words = new ArrayList<>(Arrays.asList("bbb", "a", "cc", "dddd"));
        assertEquals(Arrays.asList("a", "cc", "bbb", "dddd"), Puzzle1.sortByLength(words));
    }

    @Test
    public void equalLengthsKeepOrder() {
        List<String> words = new ArrayList<>(Arrays.asList("zebra", "apple", "mango"));
        assertEquals(Arrays.asList("zebra", "apple", "mango"), Puzzle1.sortByLength(words));
    }

    @Test
    public void alreadySortedIsUnchanged() {
        List<String> words = new ArrayList<>(Arrays.asList("a", "bb", "ccc"));
        assertEquals(Arrays.asList("a", "bb", "ccc"), Puzzle1.sortByLength(words));
    }

    @Test
    public void emptyGivesEmpty() {
        List<String> words = new ArrayList<>();
        assertEquals(Collections.emptyList(), Puzzle1.sortByLength(words));
    }
}