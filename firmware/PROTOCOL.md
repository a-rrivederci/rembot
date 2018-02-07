# Communications Protocol :one::one::zero::one:
Below is a table for the `R-Codes` to control the bot
| Action | Command |
| --- |---|
Reset | `R00`
Left | `R01 X[(x value)] Y[(y value)] F[(speed)]`
Down |  `R01 X[(x value)] Y[(y value)] F[(speed)]`
Right | `R01 X[(x value)] Y[(y value)] F[(speed)]`
Up | `R01 X[(x value)] Y[(y value)] F[(speed)]`
Lift Pen | `R02 P0`
Drop pen | `R02 P1`
Open Claw | `R03 C0`
Close Claw | `R03 C1`
Set postition | `M90 X[(x value)] Y[(y value)]`
Display info | `M100`


Send `command` -> Receive `S` -> Receive `debug message`
