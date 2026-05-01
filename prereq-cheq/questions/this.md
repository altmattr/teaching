# this_01
In Java, what does `this` refer to inside an instance method?

- The class object loaded by the JVM.
+ The current object whose method was called.
- The parent class instance.
- The most recently created object of that type.

# this_02
Why is `this.name = name;` commonly used in a constructor?

- It makes `name` static for all instances.
+ It assigns the field `name` using the constructor parameter `name`.
- It creates a new local variable named `name`.
- It forces pass-by-reference for strings.

# this_03
Which statement about `this` in a static method is correct?

- `this` refers to the current class in static methods.
- `this` refers to the first method parameter.
+ `this` cannot be used in a static context.
- `this` works only if the method is `final`.

# this_04
What is the effect of calling `this(0);` as the first line of a constructor?

- It calls a method named `this` with argument `0`.
+ It invokes another constructor in the same class.
- It creates a temporary object with value `0`.
- It calls the superclass constructor with `0`.

# this_05
What does returning `this` from an instance method usually enable?

- Automatic deep copying of the object.
+ Method chaining on the same object.
- Conversion of instance methods into static methods.
- Making the object immutable.

# this_06
Given:
```java
class Counter {
  int n;
  Counter set(int n) {
    this.n = n;
    return this;
  }
}
```
What does `this.n = n;` do?

- Assigns the field to itself and ignores the parameter.
+ Assigns the parameter `n` to the object field `n`.
- Assigns a static field shared by all `Counter` objects.
- Creates a new field `n` local to `set`.
