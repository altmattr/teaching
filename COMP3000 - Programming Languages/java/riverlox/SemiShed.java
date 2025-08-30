package riverlox;

public class SemiShed{
    double mean;
    double dev;
    public SemiShed(double mean, double dev){
        this.mean = mean;
        this.dev = dev;
    }

    public Watershed addSize(double size){
        return new Watershed(mean, dev, size);
    }
}
