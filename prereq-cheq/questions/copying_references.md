# copying_references_01
Which statement best defines copying references in Java?

- Object identity in Java means whether two references point to the exact same object.
+ Copying a reference in Java creates another pointer to the same object, not a deep copy.
- The new keyword allocates an object and invokes its constructor.
- Types in Java classify values and determine valid operations at compile time.

# copying_references_02
What is the most likely result of `Object b = a;` in Java when `a` references an object?

- A new object is created with copied elements.
+ Both `a` and `b` refer to the same list object.
- `b` becomes read-only while `a` stays mutable.
- `a` is set to `null` after assignment.

# copying_references_03
If two variables reference the same object, what happens when one variable mutates that object?

- Only that variable sees the change.
+ The change is visible through both variables.
- Java automatically clones the object first.
- The mutation throws a compile-time error.

# copying_references_04
Which line creates an independent copy rather than just copying a reference?

- `Person p2 = p1;`
- `Object m2 = m1;`
+ `Person p2 = new Person(p1);`
- `Node n2 = n1;`

# copying_references_05
Which misconception most often causes bugs with copied references?

- Thinking object equality (`equals`) always compares identities.
+ Thinking assignment of an object variable duplicates the object.
- Thinking constructors cannot initialize fields.
- Thinking method parameters must be primitives.

# copying_references_06
Given this Java code:
```
Box a = new Box();
a.value = 1;
Box b = a;
b.value = 99;
```
What is true afterward?

- `a` and `b` refer to different objects, so `a.value` is still `1`.
+ `a` and `b` refer to the same object, so `a.value` is `99`.
- Assigning `b = a` creates a new `Box` with copied fields.
- The code does not compile because objects cannot be assigned.
