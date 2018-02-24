# Communications Protocol :one::one::zero::one:

Below is a table for the `G-Codes` to control the bot

| Action | Command |
| --- | --- |
| Reset | `G00` |
| Move bot in line | `G01 X[<value>] Y[(value)] F[(speed)]` |
| Lift Pen | `G02 P0` |
| Drop pen | `G02 P1` |
| Set bot postition | `M90 X[(value)] Y[(value)]` |
| Display info | `M100` |

Send `command` -> Receive `S` -> Receive `debug message`

## Example
```
>M100
S
M100

M100
Rembot Firmare v0.1.0
Commands:
G00 - Reset
G01 X[(steps)] Y[(steps)] F[(speed)] - line
G02 P[(arm)] - arm
M90 X[(steps)] Y[(steps)] - Set position
M100 - this help message

All commands must end with a newline.

>G02 P0
S
G02 P0

G02 P:0
```
