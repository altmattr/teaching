package riverlox;

public class Watershed {
    double[] shape;
    int maxX = 10;

    public Watershed(double[] shape){
        this.shape = shape;
    }
    public Watershed(double mean, double dev, double size){
        double mu = mean;
        double sigma = dev;

        shape = new double[maxX];
        double sum = 0.0;

        // Compute unnormalized values
        for (int x = 1; x <= maxX; x++) {
            double logX = Math.log(x);
            double exponent = -Math.pow(logX - mu, 2) / (2 * sigma * sigma);
            double value = (1 / (x * sigma * Math.sqrt(2 * Math.PI))) * Math.exp(exponent);
            shape[x - 1] = value;
            sum += value;
        }

        // Normalize and scale by size
        for (int i = 0; i < shape.length; i++) {
            shape[i] /= sum;
            shape[i] *= size;
        }
    }

    public Watershed plus(Watershed other){
        double[] newShape = new double[maxX];
        for (int i = 0; i < maxX; i++) {
            newShape[i] = this.shape[i] + other.shape[i];
        }
        return new Watershed(newShape);
    }

    public String string_for(int rainfall){
        String s = "[";
        for (int i = 0; i < maxX; i++) {
            s += (int)(rainfall*shape[i]);
            if (i < maxX -1){
                s += ",";
            }
        }
        s += "]";
        return s;

    }
}
