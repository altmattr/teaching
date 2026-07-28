package variants.example_a2;

public class Number implements Value {
    double value;
    public Number(double value){
        this.value = value;
    }
    public String toString(){
        return Double.toString(value);
    }
}
