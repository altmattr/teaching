# new_01
Which statement best defines new in Java?

- Java proficiency means reliably designing, implementing, testing, and debugging Java programs.
- Overloading defines multiple methods with the same name but different parameter lists.
- Sequencing is executing Java statements in a defined order.
+ The new keyword allocates an object and invokes its constructor.

# new_02
Which Java construct is most directly tied to new?

+ new is required for most class instantiation in Java.
- Core language features, OOP, collections, exceptions, and tooling are essential proficiency areas.
- Java has primitive types and reference types.
- In Java, primitives copy values while object variables copy references.

# new_03
Which example best demonstrates new in Java code?

- println(int) and println(String) are classic overloading examples.
- Passing an object reference to a method still allows mutation of the same object.
+ new ArrayList<>() creates a new list object.
- list.add(x) is a direct object modification example.

# new_04
Which is a common mistake when working with new?

- A common mistake is memorizing syntax without understanding object semantics.
- A common mistake is ignoring returned values when the method is pure.
+ A common mistake is overusing new inside tight loops when reuse is possible.
- A common mistake is exposing many telescoping constructors instead of clearer factories.

# new_05
Which test most directly validates new behavior?

- A constructor test should verify required fields are set correctly.
- Type-related tests should include boundary values and invalid type paths.
- A useful test confirms constructors chained with this(...) initialize correctly.
+ A test can assert that new instances start with independent state.

# new_06
Which performance/maintainability statement about new is most accurate?

+ Frequent allocation can increase GC pressure in allocation-heavy code paths.
- Consistent variable syntax conventions improve code readability.
- Choosing mutable vs immutable types affects semantic clarity.
- Strong typing catches many errors before runtime.

# new_07
Which refactoring most improves code related to new?

- Refactoring with defensive copies can prevent shared-mutable-state bugs.
+ Refactoring to object pools is rare and only justified for measured hotspots.
- Refactoring to a builder improves creation of objects with many optional fields.
- Refactoring complex sequences into named methods improves traceability.

# new_08
Which Java API/keyword detail is most relevant to new?

- Copy constructors or clone alternatives are used when independent copies are needed.
- Dependency injection frameworks centralize object creation in larger systems.
- record types provide concise syntax for immutable compound data carriers.
+ new can also instantiate arrays, e.g., new int[10].

# new_09
Which debugging approach is most useful for new problems?

- Semantic confusion is debugged by tracking assignments and object aliases.
- Compiler error messages are useful when diagnosing overload resolution failures.
- Debugging with this in watch expressions helps inspect current object state.
+ Memory/allocation issues are debugged with profilers and GC logs.

# new_10
Which statement about new is true?

+ Using new correctly is foundational to Java object lifecycle reasoning.
- Good type design makes APIs safer and easier to use correctly.
- Good method definitions express one responsibility clearly.
- this always points to the receiver object for the current instance call.
