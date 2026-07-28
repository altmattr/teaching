# COMP2000 Weekly Announcements

## Week 1

Welcome to COMP2000. Classes begin this week, both lectures and workshops.  You can prepare for your workshop by bringing a logbook to class.  A logbook is either an actual paper notebook which you use for your notes in class or an electronic equivalent such as OneNote, Notion, etc. Decide before class what suits you and bring it along.  I'm a big fan of a moleskin notebook in a5 size but you decide for yourself. You'll be forming your team, agreeing on how you'll work together, and drawing up a team contract. The contract covers things like team name, expectations, communication rules, and what happens if someone isn't pulling their weight. It matters because this team sticks with you for the whole semester, so it's worth getting the ground rules right early.

## Week 2

This week is all about Git. Before class, read through the Atlassian Git tutorial pages (there are six of them, starting with "What is version control" and finishing with "Syncing"). You don't need to memorise every command, but you do need to know what init, clone, add, commit, push, pull, and log do. The lecture last week covered this, so if you attended you'll already have the basics. In the EPIC activity, your team will use Git as a chat server. That means treating commits as messages and push/pull as sending and receiving. It's a bit of a brain teaser, but it forces you to really understand how the three-tree model works. Bring your logbook.

## Week 3

Objects and Classes. Before class, read Learning Java Chapter 5 (Classes, Methods, Object Creation). The lecture last week covered the Java API documentation, constructors, the `this` keyword, getters and setters, `toString`, static, and the memory model. Come ready to draw. Your team's EPIC activity is sketching what your application interface will look like and then drawing the class structure that brings it to life. You'll need to have decided what simulation you're building. If your team hasn't decided yet, now is the time. Use butcher's paper and a UML-ish notation. Your logbook should include your team's design and at least one other team's design from the reporting period.

## Week 4

Inheritance and Overloading. Before class, read Learning Java Chapter 6 (Subclassing and Inheritance, Interfaces, Inner Classes — just the introductory part). The lecture covered extends, implements, the diamond problem, shadowing, and UML class diagrams. In the EPIC activity, your team will look at the code you've built so far and find places where inheritance can reduce duplication. Where do two classes share fields or methods? Where would `@Override` let you specialise? This is a log book class, so take 25 minutes to sketch your inheritance hierarchy as UML and write down which fields and methods moved to the superclass and why. Bring your logbook and be ready to explain one design decision you're unsure about.

## Week 5

Generics. Before class, read Learning Java Chapter 8 (Introduction to Generics, Type Erasure, Wildcards and Bounded Types). The lecture covered wrapper classes, what type erasure means at runtime, bounded type parameters, and wildcards. Come ready to break things. Your team will be given starter code (Container.java and Main.java) and your job is to cause a runtime exception without adding any casts. You'll explore raw types, unchecked suppression, and heap pollution. It's hands-on and a bit sneaky. Think about: what does `new ArrayList<String>().getClass()` actually return at runtime? Try it before class. Bring your logbook.

## Week 6

Exceptions. Before class, read Learning Java Chapter 4.5 (Exceptions). The lecture covered the Throwable hierarchy, checked vs unchecked exceptions, try/catch/finally, and the `throws` keyword. In the EPIC activity, your team gets three methods that call each other (star → pipe → caret) and you need to add throw and catch statements to produce exact "barcode" outputs. Each level changes where the exception is caught, which changes which exit prints get skipped. It's like a puzzle. Come ready to trace the call stack by hand. If you understand what happens to local variables when a frame unwinds, you're in good shape. Bring your logbook.

## Week 7

Patterns 1: Strategy and Observer. Before class, read Head First Design Patterns Chapters 1 and 2. The lecture covered design patterns generally, the Strategy pattern (composition over inheritance for interchangeable behaviours), and the Observer pattern (one-to-many notification without tight coupling). The EPIC activity is a conference-style class where individual students present their mid-semester submission. If you're presenting, you get 15 minutes plus 5 minutes of questions. All students must attend even if they're not presenting. Your mid-semester submission is due this week. That means your log book, code, and reflection need to be ready. Check the assessment brief for exactly what's required. Bring your logbook.

## Week 8

Patterns 2: Decorator, Iterator, State. Before class, read Head First Design Patterns Chapters 3 (Decorator), 9 (Iterator, up to "Just when we thought it was safe"), and 10 (State). The lecture covered how Decorator wraps objects to add responsibilities dynamically, Iterator lets you traverse collections without exposing their structure, and State lets an object change behaviour when its internal state changes. The EPIC activity is a debate. Your team will be assigned a question and a side, and you'll argue it using evidence from other teams' code. Come ready to argue. After the debate, look at your own project and pick one design pattern that fits. Implement it and be ready to explain why you chose it. Bring your logbook.

## Week 9

Behaviour Parameterisation (Lambdas). Before class, read Modern Java in Action Chapters 1, 2, and 3. The lecture covered what lambdas are (anonymous functions you can pass around), the syntax, functional interfaces like Predicate and Function, and method references. In the EPIC activity, your team gets programming puzzles where you transform or filter collections using streams and lambdas. The goal is to produce the correct result in as few characters as possible. It's code golf. It's not about writing production code, it's about discovering how expressive lambdas can be. Come ready to think in short expressions. Bring your logbook.

## Week 10

Streams. Before class, read Modern Java in Action Chapters 4 and 5. The lecture covered stream pipelines (source → intermediate → terminal), lazy evaluation, and the core operations: filter, map, flatMap, sorted, reduce, collect. In the EPIC activity, your team will look at your project code and find a loop that processes a collection of entities. Replace it with a stream pipeline. Commit both versions so you can compare. Think about: average energy across all herbivores, population by species, entities below a threshold. These are the kinds of calculations that streams handle beautifully. Bring your logbook.

## Week 11

Collecting. Before class, read Modern Java in Action Chapter 6. The lecture covered Collectors.toList/toSet/toMap, groupingBy, partitioningBy, downstream collectors, summarizingInt/Double, and writing a custom Collector. In the EPIC activity, your team will find a place in your code where a collector makes sense. Group entities by species and count them. Compute min/max/average energy per group. Build a map from one property to another. The goal is to produce a meaningful metric about your simulation. Bring your logbook.

## Week 12

Parallelism. Before class, read Modern Java in Action Chapter 7. The lecture covered threads, Runnable, race conditions, synchronised blocks, parallelStream, and ForkJoinPool. In the EPIC activity, your team will find an opportunity for parallelism in your simulation and implement it. Maybe you partition your grid into regions and simulate each on a separate thread. Maybe you use parallel streams for population statistics. Document any race conditions you find and how you fixed them. Bring your logbook.

## Week 13

Student Showcase and final submission. Attend the lecture in week 12 for exam prep and showcase guidance. Prepare a short presentation of your simulation: show it running, walk through your class architecture, and highlight the most interesting emergent behaviour. You don't need slides. The EPIC activity is a conference-style showcase where individual students present (15 minutes plus 5 minutes of questions). Your final submission is due this week: log book, code, and reflection. Check the assessment brief. Bring your logbook and come ready to celebrate what you've built.
