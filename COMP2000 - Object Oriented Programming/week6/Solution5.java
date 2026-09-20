public class Solution5 {

    static int iteration = 0;

    public static void main(String[] args) {
        star();
        System.out.println();
    }

    static void star() {
        System.out.print("* ");
        for (int i = 0; i < 2; i++) {
            iteration = i + 1;
            try {
                pipe();
            } catch (RuntimeException e) {
                // caught, continue
            }
        }
        System.out.print("* ");
    }

    static void pipe() {
        System.out.print("| ");
        caret();
        System.out.print("| ");
    }

    static void caret() {
        System.out.print("^ ");
        chuck_a_fit();
        System.out.print("^ ");
    }

    static void chuck_a_fit() {
        if (iteration == 2) {
            throw new RuntimeException();
        }
    }
}