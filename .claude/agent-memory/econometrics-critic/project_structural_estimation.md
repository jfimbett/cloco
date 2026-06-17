---
name: Liquid Assets structural estimation patterns
description: Key identification issues and estimation patterns found in the two-type Vickrey auction structural model for wine prices
type: project
---

## Structural Model Status (2026-03-29, v2 review)

After revision: 7 moments (8-bin OLS with HC1) vs 5 free params in fix_lambda spec. Score improved from 35/100 to 65/100.

**Resolved from v1:**
- Under-identification: now 7 moments, 5 params, 2 df overid
- Midpoint bias: replaced with 20-point bin-averaged integration
- Diagonal weighting: now uses full 7x7 HC1 VCV inverse
- Missing J-test: implemented (but see remaining issues)

**Remaining issues (v2):**
- J-test formula double-counts N: uses N_eff * objective, but W = vcov^{-1} already incorporates N. Correct J = objective value alone. Inflates stats by ~10^4.
- Jacobian rank 4/5 in ALL three categories under fix_lambda: one direction locally flat at every optimum
- Burgundy GC: gamma=30, delta=30 at bounds; effectively a 3-param model
- Bordeaux: gamma=0.148 (< 1) makes h(a*) monotone, defeating the hump premise; obj=7628 confirms structural misfit
- Boundary parameter SEs not flagged by se_reliable (only checks condition number)
- Moment regression omits hedonic controls (vintage, chateau, auction house FE)

**Why:** J-test scaling error is because HC1 cov_params() returns Var(hat{beta}) = Omega/N, so inv(Var) already has N baked in. Rank deficiency reflects genuine weak identification of gamma-delta tradeoff.

**How to apply:** (1) J-stat = objective, not N_eff*objective, when W = cov_params()^{-1}. (2) Always report Jacobian rank at optimum for structural models. (3) Flag any parameter within epsilon of its bound as having unreliable SE.
