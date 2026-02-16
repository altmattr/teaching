package variants.example_a2;

class Return extends RuntimeException {
  final Value value;

  Return(Value value) {
    super(null, null, false, false);
    this.value = value;
  }
}