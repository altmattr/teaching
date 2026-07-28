public class BarcodePuzzle {

    static int iteration = 0;

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
        caret();
        System.out.print("| ");
    }

    static void caret() {
        System.out.print("^ ");
        System.out.print("^ ");
    }
}
