# Communications Protocol :one::one::zero::one:
Below is a table for the `R-Codes` to control the bot
| Action | Command |
| --- |---|
Reset | `R0`
Left | `R1 Xx Yy FSPEED`
Down |  `R1 Xx Yy FSPEED`
Right | `R1 Xx Yy FSPEED`
Up | `R1 Xx Yy FSPEED`
Lift Pen | `R2 P0`
Drop pen | `R2 P1`
Open Claw | `R3 C0`
Close Claw | `R3 c1`
Set postition | `R9 Xx Yx`


Send `command` -> Receive `S` -> Receive `debug message`
