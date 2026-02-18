# object_modification_01
Given:
```
class Box { int value; }
Box b = new Box();
b.value = 3;
b.value = b.value + 2;
```
What is `b.value` at the end?

- `3`
+ `5`
- `2`
- The code does not compile.

# object_modification_02
Given:
```
class Point { int x; int y; }
Point p = new Point();
p.x = 1;
p.y = 4;
p.x = p.y;
```
What is true at the end?

- `p.x` is `1` and `p.y` is `4`.
+ `p.x` is `4` and `p.y` is `4`.
- `p.x` is `4` and `p.y` is `1`.
- Both fields become `0`.

# object_modification_03
Given:
```
class Counter { int n; }
Counter c = new Counter();
c.n = 10;
int old = c.n;
c.n = 7;
```
Which statement is true?

- `old` becomes `7` because it tracks `c.n`.
+ `old` is `10` and `c.n` is `7`.
- `old` is `7` and `c.n` is `7`.
- `old` is undefined because `c.n` changed.

# object_modification_04
Given:
```
class User { String name; }
User u = new User();
u.name = "Ana";
u.name = u.name + " Li";
```
What is `u.name` at the end?

- `"Ana"`
+ `"Ana Li"`
- `"Li"`
- `null`

# object_modification_05
Given:
```
class Bag { int items; }
Bag bag = new Bag();
bag.items = 2;
if (bag.items > 1) {
  bag.items = 0;
}
```
What is `bag.items` at the end?

- `2`
+ `0`
- `1`
- It depends on reference copying.

# object_modification_06
Given:
```
class State { int code; }
State s = new State();
s.code = 5;

void reset(State t) { t.code = 0; }

reset(s);
```
What is true after `reset(s)`?

- `s.code` stays `5` because methods cannot modify objects.
+ `s.code` is `0` because the object's field was reassigned.
- `s` now points to a new `State` automatically.
- `s.code` is undefined outside `reset`.
