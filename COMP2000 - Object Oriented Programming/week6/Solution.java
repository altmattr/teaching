public class Solution {

    static int iteration = 0;

    public static void main(String[] args) {
        int level = 3;          // change this to run a different level
        System.out.print("Level " + level + ":  ");
        switch (level) {
            case 1 -> level1();
            case 2 -> level2();
            case 3 -> level3();
            case 4 -> level4();
            case 5 -> level5();
            case 6 -> level6();
        }
        System.out.println();
    }

    // ---- Level 1: baseline ----
    static void level1() { star1(); }
    static void star1() {
        System.out.print("* ");
        pipe1();
        System.out.print("* ");
    }
    static void pipe1() {
        System.out.print("| ");
        caret1();
        System.out.print("| ");
    }
    static void caret1() {
        System.out.print("^ ");
        System.out.print("^ ");
    }

    // ---- Level 2: caret throws, pipe catches ----
    static void level2() { star2(); }
    static void star2() {
        System.out.print("* ");
        pipe2();
        System.out.print("* ");
    }
    static void pipe2() {
        System.out.print("| ");
        try {
            caret2();
        } catch (RuntimeException e) {
            // caught here, pipe exit still runs
        }
        System.out.print("| ");
    }
    static void caret2() {
        System.out.print("^ ");
        throw new RuntimeException();
    }

    // ---- Level 3: caret throws, star catches ----
    static void level3() { star3(); }
    static void star3() {
        System.out.print("* ");
        try {
            pipe3();
        } catch (RuntimeException e) {
            // caught here, pipe exit skipped
        }
        System.out.print("* ");
    }
    static void pipe3() {
        System.out.print("| ");
        caret3();
        System.out.print("| ");
    }
    static void caret3() {
        System.out.print("^ ");
        throw new RuntimeException();
    }

    // ---- Level 4: caret throws, star catches, pipe has finally ----
    static void level4() { star4(); }
    static void star4() {
        System.out.print("* ");
        try {
            pipe4();
        } catch (RuntimeException e) {
            // caught here
        }
        System.out.print("* ");
    }
    static void pipe4() {
        System.out.print("| ");
        try {
            caret4();
        } finally {
            System.out.print("| ");   // always runs
        }
    }
    static void caret4() {
        System.out.print("^ ");
        throw new RuntimeException();
    }

    // ---- Level 5: star loops pipe 2x, caret throws on iter 2, star catches ----
    static void level5() { star5(); }
    static void star5() {
        System.out.print("* ");
        for (int i = 0; i < 2; i++) {
            iteration = i + 1;
            try {
                pipe5();
            } catch (RuntimeException e) {
                // caught, continue
            }
        }
        System.out.print("* ");
    }
    static void pipe5() {
        System.out.print("| ");
        caret5();
        System.out.print("| ");
    }
    static void caret5() {
        System.out.print("^ ");
        if (iteration == 2) {
            throw new RuntimeException();
        }
        System.out.print("^ ");
    }

    // ---- Level 6: star loops pipe 2x, caret throws on iter 2, NOT caught ----
    static void level6() { star6(); }
    static void star6() {
        System.out.print("* ");
        for (int i = 0; i < 2; i++) {
            iteration = i + 1;
            pipe6();
        }
        System.out.print("* ");   // never reached
    }
    static void pipe6() {
        System.out.print("| ");
        caret6();
        System.out.print("| ");
    }
    static void caret6() {
        System.out.print("^ ");
        if (iteration == 2) {
            throw new RuntimeException();
        }
        System.out.print("^ ");
    }
}
