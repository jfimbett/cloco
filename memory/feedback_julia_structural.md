---
name: Julia for structural estimation
description: Use Julia (not Python) for structural estimation code — Python too slow for DE + bootstrap
type: feedback
---

Write structural estimation code in Julia, not Python.

**Why:** Python's per-call overhead makes differential evolution (25 × n_free × 1000 evaluations) and parametric bootstrap (B=500 draws, each needing its own optimization) prohibitively slow. Julia eliminates this overhead and enables `Threads.@threads` parallelism over bootstrap draws.

**How to apply:** Any new structural estimation scripts go in `code/structural/*.jl`. The existing Python cleaning/analysis pipeline (scripts 00–09) stays in Python. Only scripts 10+ (moments extraction, estimation, robustness) are Julia. The moments JSON file (`output/structural_moments_fine.json`) is the handoff point — Python produces it, Julia consumes it.
