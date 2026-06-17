# Positioning Guide: Distributional Debt Capacity

**Project**: Distributional Debt Capacity (Wasserstein Distance / Optimal Transport)
**Compiled**: 2026-06-14

---

## Suggested Contribution Statement

(Draft for researcher to adapt)

"We show that the cross-sectional distribution of corporate leverage and credit spreads is determined by the 1-Wasserstein distance between individual firm cash flow distributions and the aggregate capital supply distribution. This distributional characterization formalizes and identifies the 'unobserved supply/demand factor' documented by Collin-Dufresne, Goldstein, and Martin (2001) and provides a structural foundation for the excess bond premium of Gilchrist and Zakrajsek (2012). Using TRACE bond data (2012–2024) and Compustat (1989–2024), we estimate the aggregate capital supply distribution via the Fréchet mean of firm cash flow distributions — validated against FRED Flow-of-Funds data — and show that the resulting Wasserstein distances explain both the level and cross-sectional variation in credit spreads beyond standard leverage, volatility, and risk premium proxies."

---

## Key Differentiators from the 4–5 Most Similar Papers

### 1. vs. Collin-Dufresne, Goldstein, Martin (2001) — JF

**Their claim**: A single common factor drives residual spread changes; this factor is unexplained by credit risk or liquidity variables.

**This paper's claim**: The common factor is the shift in the Fréchet mean of the capital supply distribution νt. The W1 distance provides a structural characterization of what CDG measure residually. This paper does not just document the factor — it names, measures, and derives it from first principles.

**Differentiator**: Mechanism identification (W1 = debt capacity sufficient statistic) vs. residual factor documentation.

### 2. vs. Gilchrist-Zakrajsek (2012) — AER

**Their claim**: The excess bond premium (EBP) reflects financial sector risk-bearing capacity; it is a time-series aggregate measure.

**This paper's claim**: W1(μit, νt) is a bond-level, firm-specific measure that varies cross-sectionally within each period, not just in the time series. The EBP is the time-series average of what this paper explains cross-sectionally.

**Differentiator**: Cross-sectional identification of the W1 channel vs. time-series identification of the EBP. The paper should include a regression showing W1 explains spread variation within EBP deciles.

### 3. vs. Nozawa (2017) — JF

**Their claim**: Expected returns account for ~40% of cross-sectional spread variance; expected credit loss accounts for ~60%.

**This paper's claim**: Within Nozawa's expected-return component, W1 is the dominant driver. The W1 distance reflects the supply-side risk premium embedded in the spread beyond the default component.

**Differentiator**: The paper should demonstrate that W1 explains the "expected return" component of Nozawa's decomposition — i.e., augment his VAR with the W1 measure and show it loads significantly on the risk-premium factor.

### 4. vs. Siriwardane (2019) — JF

**Their claim**: Capital shocks to CDS protection sellers explain 12% of weekly CDS spread changes (CDS market, 2010–2014 sample).

**This paper's claim**: The aggregate capital supply distribution explains the cross-section of TRACE corporate bond spreads (bond market, 2012–2024 sample). The distributional approach gives a structural measure of capital supply rather than institution-specific capital shocks.

**Differentiators**: (a) TRACE bonds vs. CDS; (b) cross-section vs. time-series; (c) aggregate distributional measure vs. institution-level capital shocks; (d) theory derived from first principles vs. reduced-form measurement. The W2 measure additionally provides a social welfare interpretation absent from Siriwardane.

### 5. vs. Bretscher, Schmid, Sen, Sharma (RFS 2026)

**Their claim**: Institutional demand composition (inelastic insurers + elastic mutual funds) is a state variable for corporate bond pricing; estimated using a demand-system equilibrium model.

**This paper's claim**: The Wasserstein distance between the Fréchet mean of νt and each firm's μit is the sufficient statistic for individual debt capacity. The distributional approach provides a parsimonious scalar (W1) that captures the consequence of institutional heterogeneity without requiring full demand-system estimation.

**Differentiators**: (a) W1/W2 is derived from a theory of optimal contracting between borrowers and the aggregate capital supply distribution, while Bretscher et al. are empirical demand-system estimation; (b) this paper makes welfare statements (W2 = aggregate deadweight cost) unavailable in the demand-system framework; (c) the Fréchet mean estimator is novel; (d) Bretscher et al. use pre-2020 data; this paper extends to 2024. Frame as complements: demand-system decomposition provides the micro-foundation for institutional composition, while the Wasserstein approach delivers the aggregate sufficient statistic.

---

## Potential Target Journals

| Rank | Journal | Rationale |
|------|---------|-----------|
| 1 | **Journal of Finance** | Huang-Nozawa-Shi (2025) and Greenwald-Krainer-Paul (2025) published recently in adjacent space; JF is receptive to TRACE-based supply-side papers with structural interpretation. Siriwardane (2019) and Kuehn-Schmid (2014) show JF publishes structural-meets-empirical approaches. |
| 2 | **Review of Financial Studies** | Bretscher et al. (2026) confirms RFS is actively publishing supply-side institutional corporate bond papers. Feldhutter-Schaefer (2018) and Chen-Cui-He-Milbradt (2018) published structural credit papers recently. |
| 3 | **Journal of Financial Economics** | He-Kelly-Manela (2017), Dick-Nielsen et al. (2012) indicate JFE receptive to intermediary/TRACE methodological contributions. |
| 4 | **American Economic Review** | Gilchrist-Zakrajsek (2012) and He-Krishnamurthy (2013) show AER publishes macro-finance papers connecting credit supply to business cycles. Appropriate if the welfare/W2 dimension is emphasized. |
| 5 | **Journal of Political Economy** | Koijen-Yogo (2019) published demand-system asset pricing in JPE; appropriate if the structural estimation and general equilibrium dimensions are dominant. |

---

## Literature Gaps This Paper Fills

| Gap | This Paper's Approach |
|-----|----------------------|
| The CDG (2001) residual supply/demand factor is documented but unnamed | W1(μit, νt) names and measures it structurally |
| EBP (Gilchrist-Zakrajsek 2012) is a time-series aggregate, not cross-sectional | W1 varies cross-sectionally within period, explaining the cross-section of spreads |
| Intermediary capital supply measured as a scalar (leverage ratio) | Capital supply characterized as a full distribution νt with Fréchet mean |
| No formal theory connecting borrower cash flow distribution to debt capacity | Optimal transport theory delivers an analytical formula: W1(μ, ν) = individual debt capacity |
| Aggregate deadweight cost of credit frictions has no welfare measure | W2²(μ, ν) provides the social planner objective; welfare rankings are tractable |
| Cross-section of spreads explained by leverage and volatility but with large residuals | W1 explains the residual distributional mismatch component |
| Demand-system papers (Bretscher et al.) require full institutional holdings data | Fréchet mean estimator recovers νt from publicly available Compustat/FRED data |

---

## Risks

### Risk 1: Bretscher et al. (RFS 2026) — Published Directly Related Paper
**Nature**: Bretscher-Schmid-Sen-Sharma (2026) is now published and addresses the supply-side corporate bond pricing question with a full equilibrium demand-system. It is not a scoop but a direct comparator that will be cited by referees.
**Mitigation**: Frame as complementary rather than competing. Bretscher et al. provide the micro-evidence that institutional composition matters; this paper provides the structural aggregate characterization (W1 is the sufficient statistic for what their demand system produces in equilibrium). Demonstrate that W1 explains spread variation that Bretscher et al.'s demand composition variables do not (i.e., run a horse race controlling for their institutional demand variables).

### Risk 2: Nozawa (2017) on the Cross-Section of Spreads
**Nature**: Nozawa (2017) is the existing authoritative paper on the cross-section of credit spread variation. Any paper claiming to explain the cross-section will be immediately compared to Nozawa.
**Mitigation**: Show that W1 explains the "expected return" component in Nozawa's decomposition, rather than the "expected credit loss" component. These are complementary — the paper identifies the structural supply-side driver of Nozawa's risk-premium factor.

### Risk 3: Siriwardane (2019) on Capital Shocks and Spreads
**Nature**: Uses proprietary CDS data to show capital shocks explain 12% of spread changes. Referees will ask: why not use CDS spreads instead of TRACE bonds? Why institutional capital distribution rather than firm-level capital shocks?
**Mitigation**: Emphasize that (a) TRACE corporate bonds are 10× larger in market value than CDS; (b) the W1 measure aggregates across all lenders rather than requiring proprietary margin data; (c) the Wasserstein framework delivers a theory of optimal debt capacity that Siriwardane's reduced-form does not.

### Risk 4: "Why not a dynamic model?"
**Nature**: Standard referee concern. Static OT gives exact results; dynamic extension is future work.
**Mitigation**: Already documented in domain profile. Show that the static model's cross-sectional predictions hold empirically across quarters; emphasize that dynamic models cannot deliver the W1 = debt capacity analytical result.

### Risk 5: Identification of νt
**Nature**: Referee will ask: "You fit νt to capital supply moments; doesn't this create circularity?"
**Mitigation**: νt is anchored to FRED Flow-of-Funds capital supply data (total credit instruments, Fed balance sheet) — observable aggregate quantities independent of firm leverage or spreads. The Fréchet mean estimator uses firm cash flow distributions μit, not leverage. The SMM second-stage estimates κ from credit spreads, which provides independent cross-equation identification.
