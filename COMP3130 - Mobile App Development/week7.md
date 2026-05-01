# Week 7

## Lecture guidance

  * Frame the problem of state
    - particular attention to web
    - talk about server crashes and separate threads
  * Ephemeral vs App state
    - ephemeral in component
    - app in dedicated state - its global
  * Global state options from a general programming pov (component tree context)
    - machine global
    - ask an omnipresent component - flutter's choice
  * State change options
    - notify interested parties
    - refresh all on state change
    - flutter does a combination of two [1]
  * Persist between sessions?
    - files
    - database
    - yaml
  * Difference between serialised forms and in-memory forms
    - now we need an abstraction layer to smooth this out - repository pattern
  * Now what happens if we don't have the state locally?

 [1] Its an interesting combination. You are encouraged to define your interface only in terms of the current state (not in terms of any actions/etc).  However, the state _will_ be careful about who to notify of any changes.  This is a rare but trendy combination which flutter really nails.