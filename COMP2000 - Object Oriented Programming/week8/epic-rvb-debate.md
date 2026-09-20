# RvB backup debate deck

Three debate motions about the use of design patterns in the `rvb` codebase.
All evidence anchors are `file:line` in `rvb/src/`.

Each motion is genuinely arguable from the code, so allocate sides and let
the teams dig. During reporting, pair opposing teams for a 10 minute public
debate and have the crowd pick the winner.

---

## Debate 1: State pattern

**Motion: "Refactoring the game's `enum State` into `GameState` classes was a change worth making."**

### For

- Each state now owns its behaviour: `ChoosingActor` decides a click selects
  a player, `SelectingNewLocation` decides a click places the actor,
  `BotMoving` drives the bots. No more branching on a tag.
- Adding a state means writing a new class, not editing existing ones
  (Open/Closed Principle). The `Stage` only ever says
  `currentState = new X()`, so it is blind to the details of any state.
- The current state name is surfaced in the UI via `toString()`, so the
  pattern pays for itself in observability.

### Against

- There are only three states in a fixed cycle (Choosing -> Selecting ->
  BotMoving -> Choosing), with no behaviour variation within any state.
  Each state class has exactly one meaningful method.
- `paint()` is empty in two of the three states: half of the `GameState`
  interface is stubbed out.
- The switch-on-enum it replaced would have had one place to update per new
  state; the class version scatters the same change across four files for
  no
  new flexibility. Ceremony over substance.

### Evidence

- `GameState.java:1-4` the interface: `mouseClick` + `paint`
- `Stage.java:22` initial state assignment
- `Stage.java:96` delegation to the current state
- `ChoosingActor.java:12` transition on player click
- `SelectingNewLocation.java:24-28` transition based on players with moves left
- `BotMoving.java:20` transition back to `ChoosingActor`
- `ChoosingActor.java:17-20` empty `paint`
- `SelectingNewLocation.java:32-35` empty `paint`
- `Stage.java:57` state name drawn to the side panel

---

## Debate 2: Strategy pattern

**Motion: "The `MoveStrategy` interface earns its place in `Actor.setLocation`."**

### For

- Textbook structure: an interface, two algorithm classes (`MoveRandomly`,
  `MoveLeft`) and a context (`Actor.mover`) that delegates the decision of
  where to move.
- The strategy really does change at runtime: every `setLocation` rebinds
  it.
- The side panel reads the strategy class back out and prints it, which is
  a neat self-documenting touch.

### Against

- The client never picks the strategy. Selection is hard-wired to grid
  geometry, which is exactly `if (row % 2 == 0) new MoveRandomly(); else
  new MoveLeft();` with extra steps.
- Bot movement bypasses the pattern entirely: `BotMoving` picks a cell with
  a raw `new Random()`, duplicating `MoveRandomly`'s logic, and then
  `setLocation` rewrites the mover for the new cell anyway. The strategy is
  effectively dead code for the bots, which is half the actors on the stage.
- The point of Strategy in HFDP is swappable behaviour at the client's call
  site. Here nothing swaps behaviour; the structure exists but the payoff
  does not.

### Evidence

- `MoveStrategy.java:3-5` the interface
- `Actor.java:13` the `mover` field
- `Actor.java:40-48` `setLocation` branches on row parity to pick the strategy
- `MoveRandomly.java:6-9` random implementation
- `MoveLeft.java:6-12` left-most implementation
- `BotMoving.java:15-17` bot movement chosen with a raw `Random`
- `Stage.java:80-83` mover class name printed in the side panel

---

## Debate 3: Observer pattern

**Motion: "The `Beat`/`Pulse` animation is the Observer pattern in its purest form."**

### For

- Every participant is present and named: the subject (`AnimationBeat`), the
  observer interface (`Pulse`), register/unregister (`punchIn`/`punchOut`)
  and a notify-all loop (`ticktock`) that calls `pulsate` on a list of
  unknown observer types.
- The subject knows nothing but the `Pulse` interface, which is genuinely
  looser coupling than anywhere else in the codebase.
- The `Stage` registers a bot's interest when it joins, and the updating
  observer (`Actor.pulsate`) responds without the subject knowing what kind
  of actor it is.

### Against

- Textbook Observer fires on a state change in the subject. Here the beat
  has no state that the dancers depend on: `ticktock` is a metronome polled
  every frame by `Stage.paint`, not a notification caused by the subject
  changing.
- It pushes tagless data (phase, percentage) at a fixed cadence. Nothing
  distinguishes `punchIn` from a plain listener list.
- The worksheet itself invites the doubt (Task 17: "if we'd left out Beat
  and Pulse, would that be Observer?"). The honest answer purest-form
  defenders must face is that it passes structurally and fails semantically.

### Evidence

- `Beat.java:1-5` the subject interface
- `Pulse.java:1-3` the observer interface
- `AnimationBeat.java:10` the `dancers` list
- `AnimationBeat.java:20-27` `punchIn`/`punchOut`
- `AnimationBeat.java:30-37` `ticktock` notify loop
- `Stage.java:28-30` `punchIn` when a bot is added
- `Stage.java:40` `beat.ticktock()` called from the paint loop
- `Actor.java:50-56` `pulsate` colour update