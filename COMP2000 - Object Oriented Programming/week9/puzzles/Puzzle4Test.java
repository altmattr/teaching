import static org.junit.Assert.*;
import org.junit.Test;
import java.util.*;

public class Puzzle4Test {

    @Test
    public void uppercasesEveryWord() {
        List<String> words = new ArrayList<>(Arrays.asList("hi", "yo"));
        assertEquals(Arrays.asList("HI", "YO"), Puzzle4.upperAll(words));
    }

    @Test
    public void alreadyUpperCaseIsKept() {
        List<String> words = new ArrayList<>(Arrays.asList("OK", "GO"));
        assertEquals(Arrays.asList("OK", "GO"), Puzzle4.upperAll(words));
    }

    @Test
    public void emptyGivesEmpty() {
        List<String> words = new ArrayList<>();
        assertEquals(Collections.emptyList(), Puzzle4.upperAll(words));
    }

    @Test
    public void mixedCaseWordsAllShout() {
        List<String> words = new ArrayList<>(Arrays.asList("HeLLo", "wOrld"));
        assertEquals(Arrays.asList("HELLO", "WORLD"), Puzzle4.upperAll(words));
    }
}