---
name: Theory Model Conventions
description: Two-type Vickrey auction model for wine price-age profiles — parameters, notation, proposition numbering
type: project
---

Model in paper/sections/03_model.tex uses six parameters: (alpha_c, v_bar_k, alpha_k, gamma, delta, lambda_bar). Type c = consumption, type k = collector. Normalized age a* = a/tau. Quality function h(a*) = (a*)^gamma * exp(gamma(1 - a*)). Collector valuation v_k = v_bar_k + alpha_k * a*. Buyer composition lambda(a*) decays exponentially post-maturity at rate delta.

Propositions: 1 (non-monotone profile), 2 (trough disappearance via rho = v_bar_k/alpha_c > rho*), 3 (comparative statics on trough depth). Full proofs deferred to appendix/appendix_main.tex under label app:proofs.

**Why:** Rationalizes empirical findings — Bordeaux/Burgundy Premier Cru show trough, Burgundy Grand Cru does not due to high collector-dominance ratio.
**How to apply:** Any extensions or structural estimation should use these parameter names and functional forms consistently.
