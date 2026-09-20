public class Solution1 {

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
        chuck_a_fit();
        System.out.print("^ ");
    }

    static void chuck_a_fit() {
        // does nothing in level 1
    }
}