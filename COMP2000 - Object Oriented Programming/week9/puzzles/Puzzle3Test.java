import static org.junit.Assert.*;
import org.junit.Test;
import java.util.*;

public class Puzzle3Test {

    @Test
    public void keepsWordsOfThreeOrMore() {
        List<String> words = new ArrayList<>(Arrays.asList("a", "bb", "ccc", "dddd"));
        assertEquals(Arrays.asList("ccc", "dddd"), Puzzle3.dropShort(words));
    }

    @Test
    public void dropsAllShortWords() {
        List<String> words = new ArrayList<>(Arrays.asList("x", "hi", "yo"));
        assertEquals(Collections.emptyList(), Puzzle3.dropShort(words));
    }

    @Test
    public void emptyGivesEmpty() {
        List<String> words = new ArrayList<>();
        assertEquals(Collections.emptyList(), Puzzle3.dropShort(words));
    }

    @Test
    public void noneShortIsUnchanged() {
        List<String> words = new ArrayList<>(Arrays.asList("alpha", "beta"));
        assertEquals(Arrays.asList("alpha", "beta"), Puzzle3.dropShort(words));
    }
}