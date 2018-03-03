# Communications Protocol :one::one::zero::one:

## GCODE Subset

Below is a table for the `G-Codes` to control the bot

| Action | Command |
| --- | --- |
| Move Rapid To position | `G0 X[(value)] Y[(value)] Z[(value)]` |
| Move bot in line | `G1 X[(value)] Y[(value)] Z[(value)] F[(speed)]` |
| Set bot postition | `M90 X[(value)] Y[(value)]` |
| Display info | `M100` |

Send `command` -> Receive `S` -> Receive `debug message`

## Example
```
>M100
S

M100
Rembot Firmare v0.1.0
Commands:
G00 X[(steps)] Y[(steps)] Z[(pen)] F[(speed)] - Rapid Motion
G01 X[(steps)] Y[(steps)] Z[(pen)] F[(speed)] - Common Motion
M90 X[(steps)] Y[(steps)] - Set position
M100 - this help message

All commands must end with a newline.

>
```
