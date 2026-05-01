# constructors_01
What is the main purpose of a constructor in Java?

- To declare instance fields after object creation.
+ To initialize a new object when it is created.
- To destroy objects when they go out of scope.
- To replace all setter methods automatically.

# constructors_02
When does a constructor run?

- Every time any instance method is called.
+ When `new` creates an instance of the class.
- Only when fields are accessed for the first time.
- Only for classes that extend another class.

# constructors_03
If a class defines no constructor, what does Java provide?

- No constructor; objects cannot be created.
+ A default no-argument constructor.
- A constructor matching all fields automatically.
- A private constructor that blocks instantiation.

# constructors_04
Which statement about constructor overloading is true?

- A class may have only one constructor.
+ A class can have multiple constructors with different parameter lists.
- Overloaded constructors must have different return types.
- Overloading constructors requires `static` methods.

# constructors_05
What rule applies to `this(...)` in a constructor?

- It can appear anywhere in the constructor body.
+ It must be the first statement in the constructor.
- It can be called more than once in one constructor.
- It calls a constructor in the superclass.

# constructors_06
What is true about `super(...)` in a subclass constructor?

- It is optional and never inserted by the compiler.
+ It calls a superclass constructor and must be first if used explicitly.
- It can appear after field assignments.
- It calls another constructor in the same class.
