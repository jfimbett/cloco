---
name: optimal-transport-economics-finance
description: Key references for optimal transport in economics and finance — books, foundational math papers, economics applications
metadata:
  type: reference
---

## Mathematical Foundations

| Paper | Key result | Publication |
|-------|-----------|-------------|
| Brenier (1991) | Polar factorization; monotone rearrangement = optimal 1D transport map | CPAM Vol. 44, pp. 375–417 |
| Gangbo-McCann (1996) | Existence/uniqueness of optimal transport maps for general costs; c-convex potentials | Acta Mathematica Vol. 177, pp. 113–161 |
| Villani (2003) | Graduate textbook; Kantorovich duality; Wasserstein spaces | AMS Grad Studies in Math Vol. 58 |
| Villani (2009) | Comprehensive reference; Wasserstein geometry; connections to PDEs | Springer Grundlehren Vol. 338 |
| Santambrogio (2015) | Applied perspective; numerical methods; calculus of variations | Springer PNDE Vol. 87 |

## Economics Applications

| Paper | Application | Publication |
|-------|-------------|-------------|
| Galichon (2016) | First econ textbook on OT; matching markets, gravity, quantile regression | Princeton University Press |
| Galichon (2021) | Survey: OT in matching, discrete choice, quantile regression, trade | Advances in Econ & Econometrics, Cambridge; arXiv:2107.04700 |
| Chernozhukov-Galichon-Hallin-Henry (2017) | Multivariate quantile functions via OT; center-outward distribution | Annals of Statistics 45(1): 223–256 |

## Finance Applications (as of June 2026) — Exhaustive Search

| Paper | Application | Publication |
|-------|-------------|-------------|
| Backhoff-Veraguas et al. (2020) | Adapted Wasserstein distance for financial stability; filtration-aware | Finance & Stochastics 24(3):601–632 |
| Beiglboeck-Henry-Labordere-Penkner (2013) | Model-independent option bounds = mass transport problem | Finance & Stochastics 17(3):477–501 |
| Dolinsky-Soner (2014) | Martingale OT = robust super-hedging duality (continuous time) | Prob Theory Related Fields 160:391–427 |
| Gunsilius (2023) | Wasserstein barycenter = distributional synthetic control | Econometrica 91(3):1105–1117 |
| Galichon (2017 survey) | OT survey for econometricians | Econometrics Journal 20(2):C1–C11 |
| Galichon-Henry (2026 guide) | Econometrician's guide to OT (most recent comprehensive survey) | arXiv:2604.04227 |
| Back-Cocquemas-Ekren-Lioui (2024 WP) | OT/Kantorovich duality in Kyle's informed trading model | SSRN 3628726 |
| Malamud-Cieslak-Schrimpf (2021 WP) | OT = Bayesian persuasion / information design | SFI Research Paper 21-15 |
| Blanchet-Chen-Zhou (2022) | Wasserstein-DRO portfolio selection | Management Science 68(9):6382–6410 |
| Nguyen et al. (2024) | Conditional Wasserstein-DRO portfolio | Operations Research 73(5):2801–2829 |
| Blanchet-Murthy (2019) | Wasserstein balls for distributional risk quantification | Math Op Research 44(2):565–600 |
| Mohajerin Esfahani-Kuhn (2018) | Data-driven Wasserstein-DRO, tractable reformulation | Math Programming 171:115–166 |
| Bartl-Drapeau-Obloj-Wiesel (2021) | Sensitivity / perturbation calculus for Wasserstein-DRO | Proc Royal Society A 477:20210176 |
| Fajgelbaum-Schaal (2020) | OT networks in spatial GE | Econometrica 88(4):1411–1452 |
| Lindenlaub-Postel-Vinay (2023) | Multidimensional sorting = OT assignment | JPE 131(12):3497–3539 |
| Boerma-Tsyvinski-Zimin (2025) | Multi-marginal OT: sorting with teams | JPE 133(2) |
| Guo-Loeper-Wang (2022) | OT calibration of LSV models | Mathematical Finance 32(1):122–157 |
| Eckstein-Guo-Lim-Obloj (2021) | Multi-marginal MOT for robust multi-asset pricing | SIAM J Financial Math 12(1):158–188 |
| Galichon-Henry (2011) | Set identification via OT in games with multiple equilibria | REStud 78(4):1264–1298 |
| Cuturi (2013) | Sinkhorn: entropic regularization of OT; fast computation | NeurIPS 26:2292–2300 |
| Peyre-Cuturi (2019) | Computational OT monograph | Foundations & Trends ML 51(1):1–244 |
| Panaretos-Zemel (2019) | Statistical aspects of Wasserstein distances | Annual Rev Statistics 6:405–431 |
| Hallin et al. (2021) | Center-outward distribution functions via OT | Annals of Statistics 49(2):1139–1165 |
| Chernozhukov-Fernandez-Val-Melly (2013) | Inference on counterfactual distributions (implicit OT via quantile coupling) | Econometrica 81(6):2205–2268 |
| Pflug-Pichler (2012) | Nested distance = generalized Wasserstein for multistage processes | SIAM J Optimization 22(1):1–23 |
| Hobson-Neuberger (2012) | Robust bounds for forward start options (Skorokhod / MOT precursor) | Mathematical Finance 22(1):31–56 |
| Acciaio et al. (2016) | Model-free FTAP using OT duality | Mathematical Finance 26(2):233–251 |
| Lacker (2018) | Liquidity risk governed by Wasserstein-type transport inequalities | Math Op Research 43(3):813–837 |
| Birghila-Pflug (2019) | Optimal XL insurance under Wasserstein ambiguity | Insurance Math Econ 88:30–43 |

## Scooping Risk Assessment (June 2026)
**NONE.** No paper found using OT/Wasserstein for debt contracting, debt capacity, or corporate leverage distributions. The gap is confirmed empty after ~40 searches across SSRN, NBER, arXiv, and Google Scholar.

## Key Methodological Points
- W1 (1-Wasserstein) duality: W1(mu,nu) = sup_{phi 1-Lip} E_mu[phi] - E_nu[phi] = Kantorovich-Rubinstein theorem. 1D case: W1(mu,nu) = integral |F_mu^{-1}(t) - F_nu^{-1}(t)| dt (L1 distance between quantile functions)
- W2 (2-Wasserstein): W2^2(mu,nu) = integral (F_mu^{-1}(t) - F_nu^{-1}(t))^2 dt in 1D. Minimum expected squared displacement.
- The quantile coupling (monotone rearrangement) is the unique optimal coupling for W1 and W2 in 1D. Cite Brenier (1991) and Villani (2009) for this.
- Entropic regularization (Sinkhorn, Cuturi 2013) makes W_p estimation tractable at scale. Use epsilon-regularized OT for Compustat implementation.
- Adapted Wasserstein (Backhoff-Veraguas 2020) is for dynamic, filtration-aware problems. Static debt capacity uses standard W1 — no adaptation needed.
