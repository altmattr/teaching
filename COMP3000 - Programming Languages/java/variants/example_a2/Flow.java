package variants.example_a2;

public class Flow implements Value{
    public double[] prediction = new double[10];
    public Flow(double starts, double variance, double magnitude) {
        double remaining = magnitude;
        double ratio = 1/(variance+1);
        for (int i = 0; i < 10; i++){
            if (i < starts-1){
                prediction[i] = 0.0;
            }else {
                prediction[i] = remaining * ratio;
                remaining = remaining - prediction[i];
            }
        }
    }

    public Flow(double[] prediction){
        this.prediction = prediction;
    }

    public Flow plus(Flow b) {
        double[] newPrediction = new double[10];
        for (int i = 0; i < 10; i++) {
            newPrediction[i] = this.prediction[i] + b.prediction[i];
        }
        return new Flow(newPrediction);
    }

    public Flow addUpstream(Flow b){
        return this.plus(b);

    }

    public String toString(){
        String ret = "[";
        for (int i = 0; i < 10; i++){
            ret = ret + String.format("%.2f", prediction[i]);
            if (i<9) ret = ret + ", ";
        }
        ret = ret + "]";
        return ret;
    }



}