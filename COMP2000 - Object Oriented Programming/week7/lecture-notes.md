# COMP2000 Lecture: Decorator, Iterator, and State Patterns (handout week 8)

These are the prep notes for the lecture, distilled from the 2025 recording
of this session. The lecture runs 110 minutes. It is a live-coding session,
so the notes below mark where to write code and where to talk.

The three patterns form one story: Decorator and State are both composition
plus delegation, and Iterator is composition viewed through the type system.
Reuse the same words across the hours so they feel like one idea.

---

## Decorator (0:00-0:50)

### Setup: the class explosion

Open with the book's coffee shop: a `Beverage` superclass with Espresso,
HouseBlend, and friends. Each subclass overrides `cost()`. It looks sensible
until you add milk, mocha, whip, soy and the combinations multiply.

Introduce the Open/Closed Principle up front; it is the through-line of the
whole week:

- Working, bug-free code is the most valuable thing in the industry.
- Never encourage going back in and changing it.
- Be closed for modification, open for extension.

### The fields alternative and its limits

Show the "fields as booleans" design before the decorator (`hasMilk`,
`hasSoy`, ...) and let the class find its limits:

- Changing the cost of one component means editing the shared logic.
- You can't express "no whipped cream on iced tea" as a boolean.
- The killer: you can't double up. Two milks can't be stored in one
  `hasMilk` field, and turning the field into a count pushes you into
  "how much does each one cost" territory.

### The pivot: composition

The money moment. A decorator is just putting one object inside another.
Draw two nested circles, then be honest: objects are never inside each
other, they compose. That means one object holds a field referencing the
other, and delegates to it.

```java
Mocha m = new Mocha(new DarkRoast());
```

Now the rest of the hour is running that idea through the type system:

- You need the tiniest superclass so any decorator can wrap any drink.
- Subclass `Beverage` everywhere, and nesting becomes unbounded.
- The construction sorts itself out: you can't make a Mocha with nothing
  under it, but a DarkRoast stands alone. Some things sit at the bottom.

One subtlety worth keeping: interface versus abstract class. In Java, if
there's no behaviour in the base, lean interface, and reach for abstract
class when there's shared behaviour or you're worried about multiple
inheritance.

Stacked drinks leave the class with a mental image that lasts. Then open
questions for the last few minutes of the section; the diagram-to-code
transition is where half the class glazes over if you rush it.

---

## Iterator (0:50-1:20)

### Setup: two companies merging

One company stores items in an `ArrayList`, the other in a plain array.
The surface difference: `size()` vs `length`, `.get()` vs square brackets.
Deep down both are just "walk the elements once".

### Why hasNext() and next()

This is the genuinely interesting bit and it's worth making them wonder:

- The pattern does not generalise size and get.
- It introduces `hasNext()` and `next()` instead.
- Reason: size/get assume ordering and random access, and a heap is a
  collection where element 6 isn't a thing. The iterator doesn't care
  about order, it just shows you every element once.

### The structure

- The iterator is a separate object owned by the collection. "Give me your
  iterator", not "you are an iterator". This is where their brains melt;
  milk it.
- The iterator keeps an internal position, gets the collection's contents
  in its constructor, returns the current element on `next()` and checks
  the end on `hasNext()`.
- `Iterable` vs `Iterator`: the type-system trick so `.iterator()` compiles.
  Fun fact: arrays are not `Iterable`, purely because of generics.

### The payoff: for-each

- The for-each loop is syntactic sugar for the hasNext/next while loop.
- It is the right loop if you don't care about order and aren't inserting
  or deleting as you go.
- Warn about `Collection.forEach()`. It is a different thing that doesn't
  use the iterator, and it's a hint that lambdas are two weeks away.

Live-code a custom iterator for an array in the recording's style, with the
position counter, so "a separate object that knows how to walk" isn't
abstract.

---

## State (1:20-1:50)

State is the one they will actually use that week, so give it the best
time.

### Setup: a state machine

The hook from the recording: a state machine for the lecturer's morning.
State `asleep`, `hungry`, `thirsty`; transitions on eat, drink, wake. Silly
and it works. State machines turn a messy behaviour into a diagram, and a
diagram almost writes the program for you.

### The gumball machine, done badly

Number-based states, one method per transition, each method doing an
if-on-state. Then add a "winner" state and discover the OCP failure: every
single transition method has to change because it checks a new number it
didn't know about.

### Pivot: objects per state

Flip the design. Objects for every state, each implementing every action,
doing its own job, and transitioning.

The key differences they must feel:

- Unlike Strategy, a State must know its context, because it has to
  transition the context. That is a deliberate, bounded coupling and it's
  the main structural difference from Strategy.
- It's composition and delegation, the same two words from the Decorator
  hour used in a new shape.
- The per-state logic is scattered across classes instead of one method
  with a switch.

### One design choice worth leaving as forum bait

- Alternative A: state objects build the next state (`context.currentState =
  new NextState()`).
- Alternative B (the book): the context owns all its states and the state
  just selects the next one.

The trade-off: creating a fresh state per transition breaks if a state
needs to persist fields, because the new object starts from scratch. The
book's version survives. Good five-minute student discussion.

---

## Tie-backs and the clock

Three hooks to the rest of the week:

- The vending machine you live-code should look like the RAT's trace
  question so quiz answers are seeded in class.
- The rvb codebase (`GameState`, `ChoosingActor`, `SelectingNewLocation`,
  `BotMoving`) is the State pattern students refactor into that week; your
  live code can mirror its structure.
- `BufferedReader(new FileReader(...))` is one line away from the RAT's
  decorator question. Say it explicitly.

## Recording reminders

- Slow down around the diagram-to-code transition in Decorator.
- Live-code the custom iterator and the state machine; don't just talk.
- If the class looks lost on any single step, stop and re-explain that
  step before pushing on. The textbook PDF is available in unit
  information, so full coverage is less important than the first steps
  landing.