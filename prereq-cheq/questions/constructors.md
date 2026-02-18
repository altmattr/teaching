# constructors_01
Which statement best defines constructors in Java?

+ A constructor initializes a new object instance when new is used.
- Object identity in Java means whether two references point to the exact same object.
- Java proficiency means reliably designing, implementing, testing, and debugging Java programs.
- A command in Java is an object that encapsulates an action behind a method call.

# constructors_02
Which Java construct is most directly tied to constructors?

- new is required for most class instantiation in Java.
+ A constructor has the same name as the class and no return type.
- In Java, primitives copy values while object variables copy references.
- Access modifier, return type, name, and parameters form the method definition.

# constructors_03
Which example best demonstrates constructors in Java code?

+ Overloaded constructors allow different initialization parameter sets.
- Implementing undo usually stores command history and a reverse operation per command.
- int, boolean, and double are primitive type examples.
- println(int) and println(String) are classic overloading examples.

# constructors_04
Which is a common mistake when working with constructors?

- A common mistake is using variables before definite assignment.
- A common mistake is exposing mutable internal fields directly.
+ A common mistake is duplicating initialization logic instead of chaining with this(...).
- A common mistake is exposing many telescoping constructors instead of clearer factories.

# constructors_05
Which test most directly validates constructors behavior?

- A strong test suite covers normal, boundary, and error-path inputs.
- A useful test mutates one alias and asserts the other alias sees the change.
- A good test contrasts primitive parameter changes with object state changes.
+ A constructor test should verify required fields are set correctly.

# constructors_06
Which performance/maintainability statement about constructors is most accurate?

+ Constructor work should stay lightweight to avoid slow object creation.
- Identity matters for caching, synchronization, and aliasing behavior.
- Explicit sequencing improves predictability in imperative code.
- Clear variable semantics reduce confusion around side effects.

# constructors_07
Which refactoring most improves code related to constructors?

- Refactoring toward immutability reduces modification-related defects.
- Refactoring immutable value objects improves reliability of value semantics.
- Refactoring with intermediate variables or null-safe design improves chain readability.
+ Refactoring shared setup into one canonical constructor reduces bugs.

# constructors_08
Which Java API/keyword detail is most relevant to constructors?

- final on a reference prevents rebinding, not mutation of the referenced object.
+ super(...) is used in constructors to initialize the parent class.
- Dependency injection frameworks centralize object creation in larger systems.
- Overload resolution picks the best matching method signature at compile time.

# constructors_09
Which debugging approach is most useful for constructors problems?

- Creation bugs often surface as null fields or partially initialized objects.
- Semantic confusion is debugged by tracking assignments and object aliases.
+ Constructor bugs are often found by checking object state immediately after instantiation.
- Compiler diagnostics are the primary tool for variable syntax issues.

# constructors_10
Which statement about constructors is true?

- Understanding reference copying is central to reasoning about Java object mutation.
+ Constructors should establish valid invariants before methods are called.
- Good object creation APIs make invalid states hard to construct.
- Compound data should model domain concepts, not just group random values.
