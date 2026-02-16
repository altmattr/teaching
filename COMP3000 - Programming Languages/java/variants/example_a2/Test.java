package variants.example_a2;

public class Test{
    public static void main(String[] args){
        Flow a = new Flow(2, 1.0, 10.0);
        Flow b = new Flow(2, 2.0, 10.0);
        Flow c = a.plus(b);
        System.out.println("Flow a: " + a);
        System.out.println("Flow b: " + b);
        System.out.println("Flow c (a + b): " + c);
    }
}