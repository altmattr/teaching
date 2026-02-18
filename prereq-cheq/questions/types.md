# types_01
Which statement best defines types in Java?

+ Types in Java classify values and determine valid operations at compile time.
- A function definition in Java declares a method signature and body.
- Object identity in Java means whether two references point to the exact same object.
- Sequencing is executing Java statements in a defined order.

# types_02
Which Java construct is most directly tied to types?

- Constructors, factory methods, and builders are common object-creation techniques.
- The == operator checks identity for object references.
- In Java, object variables hold references; primitives hold values directly.
+ Java has primitive types and reference types.

# types_03
Which example best demonstrates types in Java code?

- order.getCustomer().getAddress() is a common chain example.
- List<String> b = a; makes b and a refer to the same list instance.
+ int, boolean, and double are primitive type examples.
- this(...) in a constructor calls another constructor in the same class.

# types_04
Which is a common mistake when working with types?

- A common mistake is hard-coding command selection with long if/else chains instead of polymorphism.
- A common mistake is using == instead of equals() for value comparison.
- A common mistake is using variables before definite assignment.
+ A common mistake is unsafe casts without instanceof checks.

# types_05
Which test most directly validates types behavior?

- A good test checks both field initialization and invariants across related fields.
+ Type-related tests should include boundary values and invalid type paths.
- A good test distinguishes identity checks from equality checks.
- A useful test confirms constructors chained with this(...) initialize correctly.

# types_06
Which performance/maintainability statement about types is most accurate?

+ Strong typing catches many errors before runtime.
- Frequent allocation can increase GC pressure in allocation-heavy code paths.
- Creation strategy can affect readability and memory behavior.
- Proficiency grows by deliberate practice on real code, not only quizzes.

# types_07
Which refactoring most improves code related to types?

+ Refactoring to generics improves type safety and reduces casts.
- Refactoring equals/hashCode implementations clarifies value semantics vs identity.
- Refactoring complex sequences into named methods improves traceability.
- Refactoring related parameters into a value object reduces long parameter lists.

# types_08
Which Java API/keyword detail is most relevant to types?

- Overload resolution picks the best matching method signature at compile time.
- super(...) is used in constructors to initialize the parent class.
+ The compiler performs static type checking on Java code.
- System.identityHashCode(obj) can help inspect identity-related behavior.

# types_09
Which debugging approach is most useful for types problems?

- Method-definition issues are easier to debug with clear parameter names and contracts.
- Profilers and logs help proficient developers diagnose performance and behavior issues.
+ Type mismatch compiler errors are key debugging signals.
- Breakpoints on call sites and callee methods are effective for tracing behavior.

# types_10
Which statement about types is true?

- Good method definitions express one responsibility clearly.
- Good object creation APIs make invalid states hard to construct.
+ Good type design makes APIs safer and easier to use correctly.
- this always points to the receiver object for the current instance call.
