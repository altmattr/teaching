# object_modification_01
Which statement best defines object modification in Java?

- Sequencing is executing Java statements in a defined order.
- Copying a reference in Java creates another pointer to the same object, not a deep copy.
- A reference chain is a sequence of object references used to reach nested data.
+ Object modification changes the internal state of a mutable Java object.

# object_modification_02
Which Java construct is most directly tied to object modification?

- Statement order in blocks controls sequencing behavior.
- Constructors, factory methods, and builders are common object-creation techniques.
- Access modifier, return type, name, and parameters form the method definition.
+ Setter methods and mutating collection operations are common modification mechanisms.

# object_modification_03
Which example best demonstrates object modification in Java code?

+ list.add(x) is a direct object modification example.
- new ArrayList<>() creates a new list object.
- println(int) and println(String) are classic overloading examples.
- A static factory like LocalDate.of(...) is an object creation example.

# object_modification_04
Which is a common mistake when working with object modification?

+ A common mistake is unexpected mutation through shared references.
- A common mistake is expecting this inside a static method.
- A common mistake is overusing new inside tight loops when reuse is possible.
- A common mistake is mixing identity checks and value checks.

# object_modification_05
Which test most directly validates object modification behavior?

- Tests should cover each overloaded signature explicitly.
- Type-related tests should include boundary values and invalid type paths.
+ A good test verifies state before and after each modifying operation.
- A strong test suite covers normal, boundary, and error-path inputs.

# object_modification_06
Which performance/maintainability statement about object modification is most accurate?

- Creation strategy can affect readability and memory behavior.
+ Uncontrolled modification increases coupling and bug risk.
- Clear variable semantics reduce confusion around side effects.
- Too many overloads can hurt readability more than they help convenience.

# object_modification_07
Which refactoring most improves code related to object modification?

- Refactoring to object pools is rare and only justified for measured hotspots.
- Refactoring shared setup into one canonical constructor reduces bugs.
- Refactoring complex sequences into named methods improves traceability.
+ Refactoring toward immutability reduces modification-related defects.

# object_modification_08
Which Java API/keyword detail is most relevant to object modification?

- Returning this enables method chaining patterns.
- var can be used for local variable type inference in modern Java.
+ Encapsulation helps control where and how modifications are allowed.
- The compiler performs static type checking on Java code.

# object_modification_09
Which debugging approach is most useful for object modification problems?

- Memory/allocation issues are debugged with profilers and GC logs.
- Semantic bugs appear when collections rely on inconsistent equality rules.
+ Mutation bugs are debugged by tracing who writes to the object state.
- Compiler diagnostics are the primary tool for variable syntax issues.

# object_modification_10
Which statement about object modification is true?

- Good type design makes APIs safer and easier to use correctly.
- Understanding variable semantics is essential for reasoning about Java behavior.
- Reference chains should reflect meaningful object relationships, not accidental structure.
+ Clear mutation boundaries make code easier to reason about.
