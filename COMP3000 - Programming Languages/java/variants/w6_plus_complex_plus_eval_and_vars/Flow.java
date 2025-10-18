package variants.w6_plus_complex_plus_eval_and_vars;

public class Flow {
    double[] prediction = new double[10];
    public Flow(double mean, double variance, double magnitude) {
        for (int i = 0; i < 10; i++) {
            prediction[i] = (i+1 == (int)mean)?  magnitude : 0.0; // this is a broken implementation just to keep moving - ignores variance.
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