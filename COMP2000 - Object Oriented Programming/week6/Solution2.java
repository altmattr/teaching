public class Solution2 {

    public static void main(String[] args) {
        star();
        System.out.println();
    }

    static void star() {
        System.out.print("* ");
        pipe();
        System.out.print("* ");
    }

    static void pipe() {
        System.out.print("| ");
        try {
            caret();
        } catch (RuntimeException e) {
            // caught here, pipe exit still runs
        }
        System.out.print("| ");
    }

    static void caret() {
        System.out.print("^ ");
        chuck_a_fit();
        System.out.print("^ ");     // skipped
    }

    static void chuck_a_fit() {
        throw new RuntimeException();
    }
}