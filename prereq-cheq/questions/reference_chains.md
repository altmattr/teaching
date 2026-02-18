# reference_chains_01
Given this Java code:
```
Box a = new Box();
a.value = 5;

Box b = a;
Box c = b;

int x = c.value;
c.value = 9;

int y = a.value;
```
Which statement is true?

- `x` changes to `9` because it stores a reference to `c.value`.
+ `x` stays `5`, and `y` is `9`.
- `a`, `b`, and `c` are different objects, so `y` is `5`.
- `y` is `5` because `int y` copies from `a` before mutation.

# reference_chains_02
Given this Java code:
```
Node n1 = new Node();
n1.count = 2;

Node n2 = n1;
Node n3 = n2;

int p = n2.count;
n1.count = 7;
int q = n3.count;
```
Which statement is true?

- `p` becomes `7` because it aliases `n2.count`.
+ `p` is `2`, and `q` is `7`.
- `q` is `2` because `n3` is a copy of `n2`.
- `n1.count = 7` changes only `n1`.

# reference_chains_03
Given this Java code:
```
Box a = new Box();
a.value = 10;

Box b = a;
int x = b.value;

b = new Box();
b.value = 50;

int y = a.value;
```
Which statement is true?

- `x` is `50` and `y` is `50`.
+ `x` is `10` and `y` is `10`.
- `x` is `10` and `y` is `50`.
- `x` is `50` and `y` is `10`.

# reference_chains_04
Given this Java code:
```
Cell a = new Cell();
a.num = 1;

Cell b = a;
Cell c = b;

int m = a.num;
c.num = m + 4;
int n = b.num;
```
Which statement is true?

- `m` becomes `5` because `c.num` changed.
+ `m` is `1`, and `n` is `5`.
- `n` is `1` because `b` stores a value copy.
- `a`, `b`, and `c` now refer to different objects.

# reference_chains_05
Given this Java code:
```
Item i1 = new Item();
i1.v = 3;

Item i2 = i1;
Item i3 = i2;

int t = i3.v;
i2.v = t * 2;
int u = i1.v;
```
Which statement is true?

- `t` is `6` and `u` is `6`.
+ `t` is `3` and `u` is `6`.
- `t` is `3` and `u` is `3`.
- `t` is `6` and `u` is `3`.

# reference_chains_06
Given this Java code:
```
Box a = new Box();
a.value = 4;

Box b = a;
int snap = b.value;

b.value = 9;
int now = a.value;
int still = snap;
```
Which statement is true?

- `still` is `9` because `snap` points at `b.value`.
+ `now` is `9`, and `still` is `4`.
- `now` is `4`, and `still` is `9`.
- `now` is `4`, and `still` is `4`.
