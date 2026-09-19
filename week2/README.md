# Week 2 — The Sandbox

Cellular automata with falling sand and water.

- **Spec:** [`week2.pdf`](./week2.pdf) — read it first, it is the authority.
- **Template:** [`temp.py`](./temp.py) — runs as-is, but the physics is missing.
  One `NotImplementedError` in `SandSim.update()`: sand fall/slide and water
  spread. Fire, smoke, and wood are the bonus.
- **Setup:** see the [root README](../README.md).

**Due: EOD, 23rd September 2026.**

## Your brief goes here

**Replace this file with your assignment brief.** It must contain your answers to
**Question 1** and **Question 2**.

Q1 - 

first, every cell is copied over, and then is checked with the required physics to 
see if it is breaking any rules or anything like that, and if it does, only then is
it overwritten. if it werestarted empty first, checked with physics and then decided
what to do, then all the stationalry sand and water particles would be switched with
empty boxes.

Q2 - 

by doing from left to right, the empty positions on the left side get filled every
single time, leaving the remaining sand grains to either remain there or go to the
right. this make the left side uniform, but the right side a bit weird. it also doesnt
really reflect reality, since there is no left right thing in nature. rnadomising 
the column order makes sure that there is no left right bias and that the sand piles
remain symmetric on both sides.