# sequencing_01
Which statement best defines sequencing in Java?

- Object identity in Java means whether two references point to the exact same object.
- A command in Java is an object that encapsulates an action behind a method call.
- A function definition in Java declares a method signature and body.
+ Sequencing is executing Java statements in a defined order.

# sequencing_02
Which Java construct is most directly tied to sequencing?

- Assignment operator = copies references for object types.
- A declaration includes a type, a name, and optionally an initializer.
+ Statement order in blocks controls sequencing behavior.
- this.field disambiguates instance fields from parameters with the same name.

# sequencing_03
Which example best demonstrates sequencing in Java code?

- String equality with equals() demonstrates value-style comparison.
- Passing an object reference to a method still allows mutation of the same object.
- A static factory like LocalDate.of(...) is an object creation example.
+ Initializing a variable before using it is a basic sequencing example.

# sequencing_04
Which is a common mistake when working with sequencing?

+ A common mistake is relying on side effects without clear execution order.
- A common mistake is expecting this inside a static method.
- A common mistake is risking NullPointerException in long chains.
- A common mistake is ignoring returned values when the method is pure.

# sequencing_05
Which test most directly validates sequencing behavior?

- A constructor test should verify required fields are set correctly.
- Object-creation tests should confirm valid defaults and invariant setup.
+ A good test checks state transitions after each critical step.
- Tests should explicitly assert both equals() behavior and aliasing behavior.

# sequencing_06
Which performance/maintainability statement about sequencing is most accurate?

- Clear variable semantics reduce confusion around side effects.
- Identity matters for caching, synchronization, and aliasing behavior.
- Command objects can reduce coupling between invoker code and business logic classes.
+ Explicit sequencing improves predictability in imperative code.

# sequencing_07
Which refactoring most improves code related to sequencing?

- Refactoring long declarations into clearer local variables helps maintainability.
- Refactoring to generics improves type safety and reduces casts.
+ Refactoring complex sequences into named methods improves traceability.
- Refactoring to distinct method names can improve API clarity.

# sequencing_08
Which Java API/keyword detail is most relevant to sequencing?

- Returning this enables method chaining patterns.
+ try/finally is often used to enforce cleanup sequence.
- Using JUnit and a debugger effectively is a practical proficiency signal.
- Encapsulation helps control where and how modifications are allowed.

# sequencing_09
Which debugging approach is most useful for sequencing problems?

- Memory/allocation issues are debugged with profilers and GC logs.
- Semantic bugs appear when collections rely on inconsistent equality rules.
+ Debuggers and logs help verify the actual runtime sequence.
- Debuggers are useful for inspecting object graphs and nested field values.

# sequencing_10
Which statement about sequencing is true?

- Correct variable syntax is foundational to writing valid Java programs.
- Clear method names make call sites self-documenting.
- Reference chains should reflect meaningful object relationships, not accidental structure.
+ Readable sequencing reduces accidental order-dependent bugs.
