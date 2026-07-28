# Example A2: A River System Language

This is one possible design for a domain-specific language that models water flows in river systems. It is not the best design. It is not what you should aim for. It is an example, so you can see what a complete implementation looks like.

EPIC3000 is innovative. You are building a programming language for a domain where no standard approach exists. If this were a more conventional assignment, you could find examples online. You can't, so we provide this instead. Think of it as the light at the end of the tunnel, not a map to follow.

Your language will be different. That's the point.

## What the Language Models

A river system is a network of creeks and dams. Rain falls across the system. Water flows downstream, combining at confluences, passing through dams, and eventually reaching the output.

This language lets you describe that structure. You write a program that defines creeks, connects them, and places dams. The interpreter computes the predicted flow at each point in the system over 10 days following a rain event.

Rainfall itself is external. It comes from a command-line argument, a data file, or a web service. The language doesn't include rainfall syntax. It focuses on the river system structure.

## Simplifying Assumptions

This language makes some not-perfectly-accurate assumptions about water flows. In real life, this would be an early draft language and the assumptions would be finessed with domain experts. For us, we want to make reasonable assumptions that work for the domain and for teaching. You will all likely make very different assumptions, and that's fine.

Here are the key assumptions:

- **10-day window.** Water takes about 10 days to flow through a system after rain. In reality, this varies with system size, soil type, and antecedent conditions.

- **Geometric decay.** Flow recedes at a constant fraction each day. Real recession curves are more complex, often power-law or varying with discharge level.

- **Single rainfall value.** One number for the whole system. Real rainfall varies spatially across a catchment.

- **Element-wise addition.** Combining flows just adds them element-wise. Real confluences have backwater effects, sediment dynamics, and incomplete mixing.

- **Dams as flow transformations.** Dams are functions that transform flows. Real dam operations involve multiple outlets, environmental constraints, and operational rules.

- **Level accumulates linearly.** Each day, level increases by inflow minus outflow. Real dams have evaporation, seepage, and other losses.

- **No spatial model.** The language models a graph of flows, not the spatial distribution of water across a landscape.

- **Instantaneous mixing.** Flows mix instantly at confluences. Real mixing takes time and may not be complete.

- **Downstream delay.** Water takes one day to travel from one point in the system to the next. This is a simplification; in reality, travel time depends on channel geometry, flow velocity, and distance.

## Core Concepts

### Flows

A flow is a prediction of how much water will pass a point over 10 days. You write a flow literal like this:

```
[1 ~ 1]@4
```

The three numbers are:

- **start** (1): the day water starts arriving (1-indexed). Before this day, flow is zero.
- **spread** (1): how spread out the flow is (higher = more spread, slower decay)
- **magnitude** (4): total water volume

The literal produces a 10-element array. Each element is the predicted flow on that day. Water arrives on the start day, then decays exponentially based on the spread.

Here's what `[1 ~ 1]@4` produces: `[0, 2.0, 1.0, 0.5, 0.25, 0.125, ...]`. The first element is zero (water hasn't arrived yet). Then it peaks and decays.

The formula: each day, the flow is a fixed fraction of what remains. That fraction is `1 / (spread + 1)`. So spread=1 means 50% per day, spread=2 means 33% per day, spread=0 means 100% per day (all water arrives at once).

### Combining Flows

Creeks combine when they meet. Use the `+` operator:

```
var joes = [1 ~ 1]@4;
var mahers = [3 ~ 2]@4;
var result = joes + mahers;
```

The `+` operator adds element-wise. Day 1 of `result` is day 1 of `joes` plus day 1 of `mahers`. This models a confluence where two creeks merge.

### Dams

A dam is a human-controlled flow adjustment. It receives water from upstream and decides how much to release. You declare a dam like this:

```
dam blocking_dam {
  default: [1~1]@0;
}
```

This dam blocks all flow. Whatever comes in, nothing goes out. The `default` rule says: regardless of conditions, return `[1~1]@0` (a flow of magnitude zero).

Here's a dam that passes flow through unchanged:

```
dam simple_dam {
  default: inflow;
}
```

The keyword `inflow` refers to the upstream flow. This dam does nothing; it's a pass-through.

### When Rules

Dams can have conditions. Use `when` rules:

```
dam devlins_smart_dam {
  when level > 100: inflow + inflow;
  when level < 2: [1~1]@0;
  default: [1~10]@2;
}
```

The rules are checked in order. The first matching rule determines the output:

1. If the dam level is above 100, release double the inflow (flush the dam)
2. If the dam level is below 2, block all flow (conserve water)
3. Otherwise, release a moderate environmental flow

The `when` syntax is cleaner than writing if/else chains in a function body. It reads like a specification: "when this condition holds, do this."

### Level

Each dam tracks its water level as it processes the 10-day flow array. The level starts at zero. For each day, the dam:

1. Receives that day's inflow
2. Checks its `when` rules
3. Produces an outflow
4. Updates its level: `level += inflow - outflow`

The `level` keyword in `when` rules refers to this accumulating value. It's computed locally within the dam, not stored as a global variable. Each dam has its own independent level.

### Connecting Dams

Use the `<-` operator to connect a dam to its upstream source:

```
var joes_creek = lower_joes_creek <- (upper_joes_creek + mahers_creek);
```

This means: `lower_joes_creek` is downstream of the combined flow of `upper_joes_creek` and `mahers_creek`. The `<-` operator applies the dam to the upstream flow.

Think of `<-` as "is downstream of". The left side is the dam. The right side is what flows into it.

Under the hood, `<-` is function application. The dam is a callable that takes one parameter (the upstream flow) and returns a new flow. You could write the same thing with a function, but the `dam` syntax is more expressive for this domain.

### Plot

Use `plot` to visualise a flow:

```
plot final;
```

This prints a bar chart of the 10-day prediction. Each line represents one day, with the position of the `*` indicating flow magnitude.

## Design Decisions and Rationale

These are the choices this language makes. They're not the only choices. They're not necessarily the right choices. They're the choices that make sense for this example.

**Why 10 elements?** Water takes about 10 days to flow through a typical river system after rain. A 10-day window captures the important behaviour.

**Why geometric decay?** It's simple and models natural recession. After rain, flow peaks quickly then tapers off exponentially. The spread parameter controls how quickly it tapers.

**Why `<-` for connection?** It reads naturally: "lower_joes_creek is downstream of upper_joes_creek". It's also familiar from functional programming, where `<-` often means "extract from" or "bind from".

**Why `when` rules?** They're declarative. You describe what the dam does under different conditions, not how to compute it. This matches how dam operators think: "when the level is high, release more water".

**Why is level computed locally?** Each dam processes the 10-day array day by day, accumulating its own level. No global variables needed. No awkward naming conventions. The level is a local computation within the dam.

**Why no rainfall syntax?** Rainfall is input data, not model logic. Keeping it external means the same river description can be tested with different rainfall scenarios without changing the program.

## Building and Running

To compile:

```
./compile
```

To run (defaults to `src/dammed_devlins.lox`):

```
./run
```

To run a specific program:

```
./run src/simple_dam.lox
```

## Example Programs

### tiny.lox

The simplest possible program. A single flow with no combination and no dams.

```
var only = [1 ~ 1]@4;
```

This creates a flow that starts on day 1, has spread 1, and magnitude 4. It's stored in the variable `only`.

### small.lox

Two flows combined.

```
var joes = [1 ~ 1]@4;
var mahers = [3 ~ 2]@4;
var result = joes + mahers;
```

The `+` operator adds the flows element-wise. `result` is the combined flow of both creeks.

### simple_dam.lox

Dams that modify flow.

```
var joes = [1 ~ 1]@4;
var mahers = [3 ~ 2]@4;
var result = joes + mahers;

dam simple_dam {
  default: inflow;
}

dam blocking_dam {
  default: [1~1]@0;
}

var complete = simple_dam <- result;
var blocked_complete = blocking_dam <- result;
```

Two dams: `simple_dam` passes flow through unchanged, `blocking_dam` stops all flow. The `<-` operator applies each dam to the combined upstream flow.

### devlins.lox

A river network without dams.

```
var upper_joes_creek  = [1   ~ 1]@4;
var mahers_creek      = [1.5 ~ 0]@1;
var lower_joes_creek  = [1   ~ 0]@2;
var joes_creek        = lower_joes_creek <- (upper_joes_creek + mahers_creek);

var upper_devlins_creek = [3 ~ 2]@8;
var lower_devlins_creek = [3 ~ 2]@4;

var devlins_creek = lower_devlins_creek <- (upper_devlins_creek + joes_creek);

plot devlins_creek;
```

This models a real creek system near Canberra. Upper Joe's Creek and Maher's Creek combine, flow through lower Joe's Creek, then join with Upper Devlin's Creek before flowing through lower Devlin's Creek. The `plot` statement shows the final output.

Note that `lower_joes_creek` and `lower_devlins_creek` are used as dams here, but they're pass-through dams (no rules). They exist to show the structure.

### dammed_devlins.lox

The full example with smart dams.

```
var upper_joes_creek  = [1   ~ 1]@4;
var mahers_creek      = [1.5 ~ 0]@1;
var lower_joes_creek  = [1   ~ 0]@2;
var joes_creek        = lower_joes_creek <- (upper_joes_creek + mahers_creek);

var upper_devlins_creek = [3 ~ 2]@8;
var lower_devlins_creek = [3 ~ 2]@4;

var devlins_creek = lower_devlins_creek <- (upper_devlins_creek + joes_creek);

dam devlins_trivial_dam {
  default: inflow;
}

dam devlins_always_dam {
  default: [1~1]@0;
}

dam devlins_smart_dam {
  when level > 100: inflow + inflow;
  when level < 2: [1~1]@0;
  default: [1~10]@2;
}

var final = devlins_smart_dam <- devlins_creek;

plot final;
```

Three dams demonstrate different behaviours:

- `devlins_trivial_dam`: pass-through, does nothing
- `devlins_always_dam`: blocks all flow
- `devlins_smart_dam`: responds to its level, flushing when full and conserving when low

The `devlins_smart_dam` is the interesting one. As it processes the 10-day flow array, its level accumulates. When the level gets high, it releases more water. When it gets low, it blocks flow. This models real dam operation.

## For Students

This is an example, not a template.

Your language will be different. You'll make different choices about syntax, semantics, and features. That's good. The best submissions will be those that reflect your own thinking about what makes a good domain-specific language for river systems.

Use this to see what a complete implementation looks like. See how the pieces fit together. Understand the design decisions and their rationale. Then make your own decisions.

Don't copy this. Don't follow it slavishly. Don't assume it's the right answer. It's one answer. There are many others.

If you're stuck, look at this and ask yourself: "what would I do differently?" That's where your design starts.

## Possible Extensions

The design above is deliberately minimal. It covers the core concepts but leaves plenty of room for you to go further. Here are some ideas to inspire your own design. Don't feel you need to implement all of these. Pick the ones that interest you or that solve a problem you've encountered in your own language design.

### Dam Behaviours as Functions

The current design treats each dam as a standalone entity. A more powerful approach treats dam declarations as *behaviours* (templates) that produce dam instances. This requires functions-returning-functions, which Lox supports.

Imagine this:

```
dam smart_dam(capacity) {
  return fun(inflow) {
    // rules that reference capacity from the closure
  };
}

var dam1 = smart_dam(100);
var dam2 = smart_dam(200);
```

Now `dam1` and `dam2` are independent dams with different capacities, both created from the same behaviour. This is like a class and its instances, but without explicit OOP syntax. The `capacity` parameter is captured in the closure, so each instance remembers its own capacity.

This separates *what a dam does* (behaviour) from *how big it is* (capacity). You can define one smart dam behaviour and instantiate it many times with different capacities across a river system. Real dam operators think this way: "we have a standard dam design, but each dam has different specifications."

To implement this, you'd need `dam` to be an expression (not just a statement) that returns a function. You'd also need `LoxCallable` to return `Value` instead of `Flow` so that functions can return other functions.

### External Rainfall Input

Currently, rainfall is implicit. A more practical language accepts rainfall from outside the program. This makes the language useful for actual prediction, not just demonstration.

There are several ways to do this. Command-line arguments are simple:

```
./run river.lox --rain 5
```

Data files work for historical analysis:

```
./run river.lox --data rainfall.csv
```

Web services work for real-time prediction:

```
./run river.lox --weather-api https://api.bom.gov.au/rain
```

Interactive prompts work for experimentation:

```
./run river.lox
Enter rainfall (mm): 5
```

Each approach has tradeoffs. Command-line arguments are easy to implement but only support one rainfall value. Data files support time series but need a parsing step. Web services give real-time data but add complexity and external dependencies. Interactive prompts are simple but don't support automation.

Real hydrology models are driven by external data. A language that only supports hardcoded rainfall is a toy. Adding external input makes it useful.

### Multiple Rainfall Events

The current model handles one rain event (10-day prediction). A more realistic model handles multiple rain events over a longer period. Each rain event produces its own 10-day flow array. The interpreter superimposes these arrays (adds them element-wise, offset by the day difference) to produce a combined prediction.

This requires a syntax for specifying rainfall over time:

```
rain day1: 5mm;
rain day2: 0mm;
rain day3: 12mm;
```

Or perhaps a more compact form:

```
rain [5, 0, 12, 0, 0, 3, 0, 0, 0, 0];
```

The interpreter would need to track which day each rain event falls on and offset the corresponding flow arrays accordingly. A rain event on day 3 would produce flows starting on day 3, overlapping with flows from earlier events.

Real rainfall isn't a single event. Rivers respond to sequences of rain over weeks or months. A model that only handles one event misses the important interactions between successive rainfalls.

### Dam-to-Dam Connections

Currently, dams are applied to flows with `<-`. A more expressive language might let dams connect directly to each other, forming a graph. This would use a different operator:

```
dam upstream_dam { ... }
dam downstream_dam { ... }

upstream_dam -> downstream_dam;
```

The `->` operator means "flows into". The interpreter would need to topologically sort the dam graph to determine evaluation order. If there are cycles (dam A flows into dam B which flows into dam A), the interpreter would need to detect and report them.

This is more complex than the current approach, but it models real river systems more accurately. Dams don't just connect to flow variables; they connect to other dams. A dam upstream releases water that flows into the dam downstream.

The topological sort is an interesting implementation challenge. It requires building a dependency graph from the `->` connections, detecting cycles, and determining the correct evaluation order. This is the same problem that build systems (Make, Gradle) and package managers (npm, pip) solve.

### Visualisation Beyond Plot

The current `plot` statement prints a text-based bar chart. More useful output might include SVG files (viewable in a browser), HTML reports with interactive charts, CSV data for import into spreadsheet tools, or JSON for integration with other software.

SVG output is a good starting point. The interpreter generates an SVG file with the flow predictions as line charts or bar charts. The user opens it in a browser:

```
plot final as svg "output.svg";
```

HTML reports combine multiple plots with explanatory text. The interpreter generates a complete HTML file:

```
report {
  plot devlins_creek as chart "Devlin's Creek";
  plot googong as chart "Googong Dam";
}
```

CSV output is useful for analysis in Excel or R:

```
export final as csv "predictions.csv";
```

Text output is fine for debugging, but real users need visual, shareable results. A hydrologist presenting to stakeholders needs a chart, not a terminal printout.

### Real-Time Simulation

The current model computes a static 10-day prediction. A real-time simulation would animate the flow as it happens, showing water levels changing day by day.

This could use ANSI terminal escapes (clear screen, redraw each day), a simple web server (stream updates to a browser), or a graphical window (using Java Swing or JavaFX).

The terminal approach is simplest:

```
simulate 10 days {
  plot final;
  wait 500ms;
  clear;
}
```

Each iteration clears the screen, re-evaluates the flows for the current day, and plots them. The user watches the water move through the system.

The web approach is more visual. The interpreter starts a local HTTP server and streams updates to a browser. The browser renders an animated chart showing flows changing over time.

Animation helps users understand how water moves through a system over time, not just the final prediction. It's also more engaging than static output.

### Modular Dam Library

A more advanced language might support importing dam behaviours from a library. This lets users build a river system from standard, tested components:

```
import standard_dams;

var my_dam = standard_dams.smart_dam(100);
var my_other_dam = standard_dams.blocking_dam;
```

The `standard_dams` module would contain a library of pre-built dam behaviours: pass-through dams, blocking dams, smart dams with different control strategies, and so on.

Students could build their own libraries and share them. A team working on the Canberra river system might create a `canberra_dams` module with dams specific to that system. Another team working on a different system might create their own module.

Real engineering uses standard components. A dam library lets users compose systems from tested, documented building blocks instead of writing everything from scratch.
