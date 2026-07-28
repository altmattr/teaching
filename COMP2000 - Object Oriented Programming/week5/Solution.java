public class Solution {
    public static void main(String[] args) {
        // approach 1: raw type
        Container<String> strings = new Container<>();
        strings.add("hello");
        strings.add("world");

        Container raw = strings;         // unchecked warning
        raw.add(42);                     // heap pollution
        raw.add(new Object());           // heap pollution

        System.out.println(strings.get(0)); // "hello"
        System.out.println(strings.get(1)); // "world"
        System.out.println(strings.get(2)); // ClassCastException
    }

    // approach 2: raw parameter
    static void poison(Container c) {
        c.add(99);
    }
}
