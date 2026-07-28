public class Main {
    public static void main(String[] args) {
        Container<String> strings = new Container<>();
        strings.add("hello");
        strings.add("world");

        String first = strings.get(0);
        String second = strings.get(1);

        System.out.println(first + " " + second);
    }
}
