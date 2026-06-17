---
date: 2026-06-14
description: SMM methodology overhaul, reorganization, moment-matching table
status: in-progress
---

# Session Log — SMM Overhaul + Paper Reorganization

## Goal

Address three structural problems raised by the user after Round 10 fixes:
1. Structural parameters duplicated across Section 6 (estimation.tex) and Section 7 (results.tex)
2. No table showing how close model moments are to data moments, with a proper statistic
3. Appendix SMM description missing optimal weighting matrix, Jacobian, and proper inference

## Key Context

- Paper: "Distributional Debt Capacity: Optimal Transport and Corporate Leverage"
- Current peer review score: 81/100 (R9 blind-peer-referee, Minor Revisions)
- Estimation: κ = 0.104 (bootstrap SE 0.005), binding at D9; α_ν = -3.493, σ_ν = 2.392
- Model: κ is identified as constrained GMM optimum — unconstrained GLS gives κ_WLS = 0.142 which violates 2 decile inequality constraints, so κ_bound = 0.104 is the constrained solution
- S_hat: 10×10 bootstrap covariance of decile-mean TRACE spread vectors (500 reps)
- Q-statistic at constrained κ: 594.8

## Changes Made This Session

### Code (`code/data/08_smm_estimation.py`)
- During TRACE bootstrap, now also collects 10-vector of decile-mean spreads per rep → builds `boot_spread_vecs`
- Computes S_hat = 10×10 bootstrap covariance of decile-mean spread vectors
- Computes W_opt = S_hat^{-1} (ridge-regularized)
- Computes κ_WLS = unconstrained GLS = 0.1416 (violates 2 deciles)
- Computes Q_stat = g'W_opt g = 594.76 at constrained κ = 0.1039
- Generates new `tab_moment_matching.tex`

### Paper (`paper/sections/results.tex`)
- Removed duplicate §7.3 "Structural Estimates" (was repeating α_ν, σ_ν, κ from estimation.tex §6.2)
- Added reference to and input of `tab_moment_matching.tex` in Model Fit section

### Paper (`paper/sections/estimation.tex`)
- Expanded §6.2 with Capital supply distribution paragraph and Bankruptcy cost paragraph (moved from deleted results.tex §7.3)
- Updated κ description: "constrained GMM procedure" + mention of unconstrained κ_WLS = 0.142

### Appendix (`paper/appendix/data_appendix.tex`)
- Rewrote Stage 2 to show full GMM machinery:
  - Moment conditions g_d(κ) = s_data_d - κ x_d
  - Optimal weighting matrix W = S^{-1} from bootstrap covariance
  - Jacobian G = ∂m/∂κ = x (the "impulse function" the user asked about)
  - GLS Avar formula: Avar(κ) = (x'Wx)^{-1}
  - Constrained solution derivation (why min-operator = constrained GMM)
- Updated Bootstrap section to describe S_hat estimation

## Verification
- Paper compiles cleanly: 51 pages, 642712 bytes, no errors, no undefined references
- tab_moment_matching.tex generated correctly with Q = 594.76, κ_WLS = 0.1416

## Open Questions
- Should we run Round 11 peer review now?
- The Q-statistic (594.8) is large — this is expected and should be discussed in the text since the model predicts inequality bounds (not equality), so large residuals in D1-D8 are consistent with the model
- The normalized residuals (g_d/σ_d) range from 0.0 (D9, binding) to 15.8 (D3) — referee may ask why D3 has the largest normalized residual


---
**Context compaction (auto) at 17:21**
Check git log and .claude/plans/ for current state.


---
**Context compaction (auto) at 18:28**
Check git log and .claude/plans/ for current state.


---
**Context compaction (auto) at 19:47**
Check git log and .claude/plans/ for current state.
