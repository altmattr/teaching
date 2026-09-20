public class Solution3 {

    public static void main(String[] args) {
        star();
        System.out.println();
    }

    static void star() {
        System.out.print("* ");
        try {
            pipe();
        } catch (RuntimeException e) {
            // caught here, pipe exit skipped
        }
        System.out.print("* ");
    }

    static void pipe() {
        System.out.print("| ");
        caret();
        System.out.print("| ");     // skipped
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