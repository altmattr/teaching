public class Solution4 {

    public static void main(String[] args) {
        star();
        System.out.println();
    }

    static void star() {
        System.out.print("* ");
        try {
            pipe();
        } catch (RuntimeException e) {
            // caught here
        }
        System.out.print("* ");
    }

    static void pipe() {
        System.out.print("| ");
        try {
            caret();
        } finally {
            System.out.print("| ");   // always runs
        }
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