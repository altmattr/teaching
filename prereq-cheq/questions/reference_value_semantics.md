# reference_value_semantics_01
Which statement best defines reference vs value semantics in Java?

- Object modification changes the internal state of a mutable Java object.
- Object creation in Java is the process of allocating and initializing class instances.
+ Reference semantics track object identity, while value semantics compare logical content.
- Sequencing is executing Java statements in a defined order.

# reference_value_semantics_02
Which Java construct is most directly tied to reference vs value semantics?

- The Command pattern is typically modeled with an interface such as Runnable or a custom execute() method.
- Classes and records are core Java constructs for compound data modeling.
+ In Java, object variables hold references; primitives hold values directly.
- Constructors, factory methods, and builders are common object-creation techniques.

# reference_value_semantics_03
Which example best demonstrates reference vs value semantics in Java code?

+ String equality with equals() demonstrates value-style comparison.
- Initializing a variable before using it is a basic sequencing example.
- public int add(int a, int b) { return a + b; }
- new ArrayList<>() creates a new list object.

# reference_value_semantics_04
Which is a common mistake when working with reference vs value semantics?

- A common mistake is relying on side effects without clear execution order.
- A common mistake is creating ambiguous overloads that confuse call sites.
+ A common mistake is mixing identity checks and value checks.
- A common mistake is unexpected mutation through shared references.

# reference_value_semantics_05
Which test most directly validates reference vs value semantics behavior?

- A strong test suite covers normal, boundary, and error-path inputs.
- A good test checks state transitions after each critical step.
- A good test verifies state before and after each modifying operation.
+ Tests should explicitly assert both equals() behavior and aliasing behavior.

# reference_value_semantics_06
Which performance/maintainability statement about reference vs value semantics is most accurate?

+ Choosing mutable vs immutable types affects semantic clarity.
- Using this clearly can improve readability in fluent APIs.
- Well-designed compound data improves readability more than using parallel primitive arrays.
- Consistent variable syntax conventions improve code readability.

# reference_value_semantics_07
Which refactoring most improves code related to reference vs value semantics?

+ Refactoring immutable value objects improves reliability of value semantics.
- Refactoring with defensive copies can prevent shared-mutable-state bugs.
- Refactoring with intermediate variables or null-safe design improves chain readability.
- Refactoring toward immutability reduces modification-related defects.

# reference_value_semantics_08
Which Java API/keyword detail is most relevant to reference vs value semantics?

- try/finally is often used to enforce cleanup sequence.
- record types provide concise syntax for immutable compound data carriers.
+ equals() and hashCode() define value semantics for custom classes.
- Using JUnit and a debugger effectively is a practical proficiency signal.

# reference_value_semantics_09
Which debugging approach is most useful for reference vs value semantics problems?

- Debuggers are useful for inspecting object graphs and nested field values.
- Debugging with this in watch expressions helps inspect current object state.
+ Semantic bugs appear when collections rely on inconsistent equality rules.
- Profilers and logs help proficient developers diagnose performance and behavior issues.

# reference_value_semantics_10
Which statement about reference vs value semantics is true?

- this always points to the receiver object for the current instance call.
- Good type design makes APIs safer and easier to use correctly.
+ Clear semantics are essential for correct APIs and collection behavior.
- Identity and equality are different concepts in Java object models.
