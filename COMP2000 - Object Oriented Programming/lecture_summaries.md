# COMP2000 Lecture Summaries (2026)

All lectures are 110 minutes (1 h 50). Timestamps are cumulative: the time at which the lecturer should aim to move on to the next section. Lectures happen one week before the associated handout (e.g. Lecture 1 covers Git and maps to Handout Week 2).

---

## Lecture 1 -- Git (handout week 2)

  - Walk through the three-tree model (working directory, staging area, repository) with a diagram so students understand where changes live at each stage. Move on by 0:15.
  - Cover the basic workflow: init, clone, add, commit, log, status. Run each command live so students see what git does at each step. Move on by 0:35.
  - Explain synchronisation: fetch, pull, push, and working with remotes. Students need to understand how to share work with their team. Move on by 0:50.
  - Show how to set up a GitHub repo, add collaborators, and the difference between SSH and HTTPS. Move on by 1:00.
  - Run a live demo of the team chat exercise (commits as messages). This is the main activity and it helps students see why commit messages matter. Move on by 1:20.
  - Give students a git log to trace through. They interpret the history and reconstruct what happened. Move on by 1:35.
  - Leave time for Q&A and a quick review before wrapping up. Move on by 1:50.

---

## Lecture 2 -- Java API and Classes and Objects (handout week 3)

  - Start with what an object is: an instance of a class that bundles data and methods together. Contrast with procedural languages where data and functions are separate. Move on by 0:10.
  - Explain that a class is a blueprint or template: a custom data type. Show how objects of the same class share structure but hold different values. Move on by 0:15.
  - Show students how to navigate the Java API documentation. They'll need it all semester. Move on by 0:20.
  - Demo JPanel and JFrame briefly. Students just need enough to get a drawing area on screen; the GUI toolkit is not the focus. Move on by 0:25.
  - Cover constructors: default versus parameterised, and what `new` actually does (allocate memory on the heap). Show what happens when you define your own constructor but still need a default one. Move on by 0:40.
  - The `this` keyword disambiguates instance variables from parameters and enables constructor chaining. Walk through a live example where omitting it causes a bug. Move on by 0:50.
  - Get to getters and setters. Explain the data hiding principle: you want a clear interface, not direct access to internals. Move on by 0:55.
  - Cover `toString()` and the `@Override` annotation. Show the default output (class name + memory address) and how to make it useful. Move on by 1:00.
  - Walk through the memory model: heap allocation, references versus values, and what null actually means. Compare with a language that doesn't catch null access at compile time. Move on by 1:15.
  - Explain static variables and methods. Show that static belongs to the class, not to any one instance, and why you'd use `ClassName.method()` over `instance.method()`. Move on by 1:25.
  - Contrast static typing (Java) with dynamic typing (Python). The key point is that types push errors from run time to compile time. Move on by 1:35.
  - Touch on Hungarian notation and code style conventions. The history is interesting but the takeaway is that meaningful names matter more than prefixes. Move on by 1:40.
  - Live code a Point class from scratch. This ties everything together: constructors, toString, static, and the API documentation. Move on by 1:50.

---

## Lecture 3 -- Inheritance (handout week 4)

  - Start with why inheritance exists: you're modelling real-world things and want to share common behaviour. Move on by 0:10.
  - Demonstrate subclassing: the `extends` keyword and what members get inherited. Students need to see a concrete parent-child example. Move on by 0:25.
  - Explain shadowing: local variables, instance variables, and inherited variables. Scope gets more complex once inheritance is in play. Move on by 0:35.
  - The compiled versus interpreted distinction comes up here if students ask. Keep it brief. Move on by 0:45.
  - Cover the diamond problem: multiple inheritance creates ambiguity about which method to call. Java solves this by allowing only single inheritance. Move on by 0:55.
  - Introduce interfaces as a contract-based alternative. `implements` says a class will provide certain methods without dictating how. Move on by 1:10.
  - Show that a class can implement multiple interfaces. This is how Java gives you the flexibility of multiple inheritance without the ambiguity. Move on by 1:20.
  - Mix inheritance with interfaces: a class can extend one parent and implement several interfaces. Draw the UML notation so students can read class diagrams. Move on by 1:30.
  - Show that interfaces can extend other interfaces. Move on by 1:40.
  - Live code a vehicle hierarchy with `Drivable` and `Parkable` interfaces. Get students to predict which methods are available on each variable type. Move on by 1:50.

---

## Lecture 4 -- Generics (handout week 5)

  - Arrays are contiguous blocks of memory where every element has the same type. Remind students that arrays are primitive in Java, not objects. Move on by 0:10.
  - Wrapper classes (Integer, Float, Double) let primitives work where objects are required. Autoboxing and unboxing hide the conversion. Move on by 0:20.
  - Show the problem: collections without generics force you to cast everything, and the compiler can't check that casts are safe. Move on by 0:30.
  - Generic classes use angle brackets to specify a type parameter. The compiler catches mismatches at compile time, not run time. Move on by 0:45.
  - Type erasure is how generics stay backwards compatible with Java 1.4. The type parameter disappears at run time, so `ArrayList<String>` and `ArrayList<Integer>` are the same class. Move on by 0:55.
  - Bounded type parameters (`<T extends Comparable>`) restrict what types can be used. They let you call methods on the type parameter. Move on by 1:05.
  - Wildcards (`? extends T` and `? super T`) handle situations where the exact type is unknown. Push versus pull: this is the hardest part, so take it slowly. Move on by 1:15.
  - `Optional<T>` is a container that might hold a value or might be empty. It forces the caller to handle both cases, which is safer than null. Move on by 1:25.
  - Brief history: Wadler and Ibersky's Pizza language pioneered generics before they were added to Java. Move on by 1:30.
  - Live demo: refactor a raw ArrayList to use generics. Show how the compiler flags unsafe code. Move on by 1:45.
  - Q&A. Move on by 1:50.

---

## Lecture 5 -- Exceptions (handout week 6)

  - Start with what life was like before exceptions: nested if statements everywhere in C. The real task (reading a file) gets buried in error-checking noise. Move on by 0:10.
  - Show the Throwable hierarchy: Exception versus Error. Errors (OutOfMemoryError, StackOverflowError) are things you probably can't handle in your programme. Move on by 0:20.
  - Checked exceptions must be handled or declared. Unchecked exceptions (RuntimeException and its subclasses) don't force the compiler to complain. Move on by 0:30.
  - Introduce try, catch, finally. Wrap code that might fail, handle the failure if it happens, and clean up either way. Move on by 0:45.
  - The `throws` keyword lets a method declare that it can produce an exception. The caller then has to handle it or declare it too. Move on by 0:55.
  - Walk through specific exceptions: ArithmeticException from division by zero, FileNotFoundException from opening a missing file. Move on by 1:05.
  - Use multiple catch blocks to handle different exceptions differently. Order matters: the most specific exception comes first. Move on by 1:15.
  - The `finally` block runs whether an exception was thrown or not. It's where you close files, release locks, or clean up resources. Move on by 1:25.
  - If time allows, show try-with-resources. It closes resources automatically and makes the code shorter. Move on by 1:30.
  - Live code a file reader with exception handling. Show the code with and without proper exception handling so students feel the difference. Move on by 1:45.
  - Q&A and review. Move on by 1:50.

---

## Lecture 6 -- Strategy and Observer Patterns (handout week 7)

  - Start with what design patterns are: reusable solutions to common problems. Mention the Gang of Four book and the Head First Design Patterns textbook. Move on by 0:15.
  - Strategy Pattern solves the problem of inheritance explosion. Instead of subclassing for every variation, you compose behaviours into objects. Move on by 0:35.
  - Live code a payment system with CreditCardPayment and PayPalPayment strategies. Show how adding a new payment type doesn't change existing code. Move on by 0:55.
  - Observer Pattern solves the problem of tight coupling. When one object changes, it notifies its dependents without needing to know what they are. Move on by 1:10.
  - Live code a weather station: Subject registers observers and notifies them when the temperature changes. Move on by 1:30.
  - Compare the two patterns. Strategy is about interchangeable behaviour. Observer is about one-to-many notification. Move on by 1:40.
  - Give students scenarios and ask them to pick which pattern fits. This reinforces the difference. Move on by 1:50.

---

## Lecture 7 -- Decorator, State, and Iterator Patterns (handout week 8)

  - Decorator Pattern solves the problem of subclass explosion. Adding every combination of features (milk, sugar, whipped cream) as a subclass is unmanageable. Move on by 0:15.
  - Walk through the coffee shop example. You've got a Beverage abstract class, and decorators wrap a beverage to add cost and description. Move on by 0:30.
  - Live code a coffee shop with milk, sugar, and whipped cream decorators. Show how you can stack them. Move on by 0:50.
  - Iterator Pattern lets you access elements without exposing the internal structure of a collection. Move on by 1:05.
  - Show Java's Iterable and Iterator interfaces. Most collections support for-each because they implement Iterable. Move on by 1:15.
  - State Pattern lets an object change its behaviour when its internal state changes. It looks like the object has changed class. Move on by 1:30.
  - Live code a vending machine with NoCoin, HasCoin, and Dispensing states. Each state decides what happens when you insert a coin or press a button. Move on by 1:45.
  - Q&A. Move on by 1:50.

---

## Lecture 8 -- Lambdas (handout week 9)

  - Start with mathematical functions: `f(x) = x + 7` is a named function, `λx.x + 7` is the same thing without a name. Students don't need lambda calculus, just the intuition. Move on by 0:10.
  - An anonymous function is a function without a name. That's what a lambda is: a block of code you can pass around. Move on by 0:15.
  - Show the lambda syntax in Java: `(parameters) -> expression`. Start simple and then show a block body with curly braces. Move on by 0:25.
  - Functional interfaces are interfaces with a single abstract method. Java provides many of them: IntUnaryOperator, IntConsumer, Predicate, Function. Move on by 0:40.
  - Use `forEach` with a lambda. Compare it to a traditional for loop side by side so students see the difference. Move on by 0:50.
  - Predicate and `removeIf` let you filter collections without writing a loop. Show how a predicate expresses intent clearly. Move on by 1:00.
  - Method references (`System.out::println`) are a shorthand when the lambda body is just one method call. Move on by 1:10.
  - Contrast imperative style (you write every step) with functional style (you declare what you want). Move on by 1:20.
  - Live refactoring: replace an anonymous inner class with a lambda. Show how much noise the inner class adds. Move on by 1:35.
  - Give students a list of strings and ask them to write lambdas that filter and transform it. Move on by 1:50.

---

## Lecture 9 -- Streams (handout week 10)

  - Collections have a fixed size at any point in time. Streams might not have a size at all. Think of the difference between a DVD (fixed content) and a live stream (never ending). Move on by 0:10.
  - A stream pipeline has three stages: a source, intermediate operations, and a terminal operation. Nothing happens until you call the terminal operation. Move on by 0:25.
  - `filter` selects elements by a predicate. Show how it replaces an if statement inside a loop. Move on by 0:35.
  - `map` transforms elements from one type to another. Show how it replaces a loop that builds a new list. Move on by 0:45.
  - `sorted` and `forEach` are straightforward. Demonstrate them briefly. Move on by 0:55.
  - `collect` with `Collectors.toList()` turns the stream back into a collection. This is the most common terminal operation. Move on by 1:05.
  - Compare declarative style (what you want) with imperative style (how to do it). Streams hide the plumbing so you focus on the logic. Move on by 1:15.
  - `parallelStream()` can speed things up, but it's not always faster. Show an example where parallel makes a measurable difference. Move on by 1:25.
  - Stream operations look like SQL. If students know `SELECT ... WHERE ... ORDER BY`, they already have the intuition. Move on by 1:30.
  - Live refactoring: replace a for loop with a stream pipeline. Start with the loop, then convert it step by step. Move on by 1:45.
  - In-class exercise: give students a loop and ask them to rewrite it as a stream. Move on by 1:50.

---

## Lecture 10 -- Collecting with Streams (handout week 11)

  - Review terminal operations on streams quickly. `collect` is the most flexible one. Move on by 0:10.
  - `Collectors.toList()`, `toSet()`, and `toMap()` are the basic collectors. Show when you'd pick each one. Move on by 0:25.
  - `groupingBy` categorises elements into a map of lists. It's like a GROUP BY in SQL. Move on by 0:40.
  - `partitioningBy` splits into two groups: true and false. Use it for binary decisions. Move on by 0:50.
  - Downstream collectors (`counting`, `summingInt`, `averagingDouble`) let you summarise each group. Move on by 1:00.
  - `summarizingInt` and `summarizingDouble` return a statistics object with count, sum, min, average, and max. Move on by 1:10.
  - Custom collectors with `Collector.of()` let you build your own accumulation logic. Show a simple example and explain when you'd need it. Move on by 1:25.
  - Live code: group bank transactions by category and sum the totals for each category. Move on by 1:40.
  - In-class exercise: give students data and ask them to summarise it with collectors. Move on by 1:50.

---

## Lecture 11 -- Parallelism (handout week 12)

  - Start with the difference between concurrency (dealing with many things) and parallelism (doing many things at once). Move on by 0:10.
  - Show the Thread class and Runnable interface. Creating a thread is simple, but managing threads correctly is not. Move on by 0:25.
  - Race conditions happen when two threads access shared state without coordination. Show a classic counter example where the result is wrong. Move on by 0:40.
  - `synchronised` blocks and explicit locks prevent race conditions. But they also serialise your code, which defeats the purpose of having threads. Move on by 0:55.
  - `parallelStream()` is the easiest way to add parallelism. The runtime handles the thread management, but you still need to make sure your operations are safe. Move on by 1:10.
  - ForkJoinPool breaks a task into smaller pieces recursively. This is what `parallelStream()` uses under the hood. Move on by 1:20.
  - Parallelism has overhead. If the task is too small or the data is too small, it's slower than sequential. Show the numbers. Move on by 1:30.
  - Live demo: run a simulation step in parallel and sequential mode. Compare the speed and discuss when you would choose each. Move on by 1:45.
  - Q&A. Move on by 1:50.

---

## Lecture 12 -- Showcase and Wrap-up (handout week 13)

  - Recap the key concepts from the semester: classes and objects, inheritance, generics, exceptions, design patterns, lambdas, streams, parallelism. Move on by 0:20.
  - Explain the showcase format: how long each presentation is, what to show (running code, architecture, emergent behaviour). Move on by 0:35.
  - Walk through how to present code effectively. Talk about the structure, not every line. Show the interesting part. Move on by 0:50.
  - Remind students what goes into the final submission: code, log book, reflection. Emphasise the deadline. Move on by 1:05.
  - Give exam preparation guidance. Point to past materials, the question bank, and what topics to prioritise. Move on by 1:20.
  - Open the floor for questions about the project, the final submission, or the exam. Move on by 1:40.
  - Course evaluations and a few closing remarks. Move on by 1:50.
