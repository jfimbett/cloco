# Data Assessment Review: Distributional Debt Capacity
**Date:** 2026-06-13
**Score:** 54/100
**Assessment reviewed:** `quality_reports/data_exploration_distributional_debt_capacity.md`
**Research context:** Structural estimation (SMM) — optimal transport / Wasserstein distance applied to corporate debt contracting. θ = (α_ν, σ_ν, κ). Three structural parameters identified jointly from leverage moments (Compustat/CRSP) and credit spread moments (Mergent FISD).

---

## Issues Found

### 1. Measurement Validity — ν_t Proxy Is Theoretically Indefensible as Stated — CRITICAL

**Deduction: -20 points**

The assessment recommends (as its "first attempt") fitting a LogNormal distribution to quarterly bond issuance amounts from Mergent FISD and treating this as ν_t — the aggregate capital supply distribution. This is the most consequential measurement choice in the paper, and the assessment does not adequately defend the theoretical mapping.

The model's ν_t is the distribution of capital that lenders *bring to the market and are willing to deploy to any given firm* — it is a supply distribution over lending capacity, not a distribution over deal sizes already transacted. Bond deal sizes from Mergent FISD reflect the joint equilibrium of supply AND demand. A large bond issuance could reflect either high capital supply (the bank/fund had more to deploy) or high demand (the firm was credit-worthy and chose to issue more). The assessment acknowledges this on page 5 ("Conflates supply and demand: a large issuance could reflect high supply or high demand") but treats this as a minor weakness rather than as a fundamental identification threat.

The problem is sharper than the assessment conveys. In the optimal transport framework, ν_t is a primitive over which the social planner optimizes the coupling. If ν_t is measured as the equilibrium deal-size distribution, then the empirical object is already an *outcome* of the optimal transport problem — making the estimation circular. Specifically: if firms with cash flow distributions closer to ν_t get larger allocations, and ν_t is estimated from allocations (deal sizes), then W1(μ_it, ν_t) is estimated from objects that are simultaneously determining each other. This is a potential circular identification problem that is not named anywhere in the assessment.

The assessment identifies this vaguely in Critical Gap #4: "the model's link between deal size distribution and the supply of capital available to a given firm is not tight" and "Why is the bond deal size distribution the right measure of capital supply to firm i?" — but frames it as a "potential referee objection" rather than as a core threat to identification validity. That framing understates the severity.

Additionally, the assessment is silent on the following theoretical point from the research spec (Section 2): the model's capital supply distribution ν_t applies to *all* firms across the corporate sector, including bank loan borrowers, private placement borrowers, and unrated firms. Mergent FISD captures only the public bond market — which is the upper tail of the credit quality distribution. Using bond issuance sizes to measure ν_t means the measured distribution systematically excludes the lenders and deal structures serving lower-credit-quality firms, producing a ν_t that is biased toward the high-quality end of the capital market. This is a selection-in-measurement problem, not merely a coverage gap.

**What is missing:** The assessment should have graded this as a Critical failure of measurement validity for the primary structural primitive of the paper, not as a feasibility concern. The paper needs a theoretical argument — ideally formalized in the theory section — for why bond deal sizes in a competitive equilibrium serve as a sufficient statistic for the supply-side distribution ν_t. Absent such an argument, the entire ν_t estimation strategy is vulnerable to a desk rejection.

---

### 2. Identification Compatibility — ν_t and λ_it Share Common Shocks — CRITICAL

**Deduction: -20 points**

The SMM estimation is built on a cross-equation restriction: the same θ = (α_ν, σ_ν, κ) must simultaneously fit leverage moments (from Compustat/CRSP) and credit spread moments (from Mergent FISD). The assessment treats these as "independent" data sources. They are not.

If ν_t is estimated from bond issuance deal sizes (Mergent FISD), and leverage is measured from Compustat, then both ν_t and λ_it are driven by common macro shocks — credit cycle dynamics, monetary policy, recession effects — that operate simultaneously on bond issuance volumes and firm leverage ratios. In the language of structural estimation: the weighting matrix W in the SMM criterion function S(θ) = [m_data - m_sim(θ)]' W [m_data - m_sim(θ)] assumes that the cross-equation moment conditions are independent. If the data generating processes for the leverage moments and the spread moments share a common macro factor, the efficient GMM weighting matrix is not block-diagonal across equations, and standard errors estimated under the independence assumption will be understated — potentially severely so.

The assessment is silent on this contamination problem. It notes that credit spreads and leverage share "common shocks" in the description of Component E (macro variables), but does not connect this to the SMM identification problem. The research spec (Stage 2) acknowledges the issue obliquely by noting that ν_t is "anchored to FRED credit market aggregates (prevents circularity)" — but the assessment does not verify whether this anchoring strategy actually prevents circularity or merely relocates it.

Specifically: if α_ν(t) = f(log BCNSDODNS_t) (Approach C-3 from the assessment), and BCNSDODNS_t is an aggregate balance sheet identity that accounts for total nonfinancial corporate debt outstanding, then movements in aggregate leverage directly move the regressor used to parameterize ν_t. This is simultaneity, not mere correlation. The assessment does not name this problem.

**The key test the assessment should have demanded:** Can the researcher construct an empirical measure of ν_t that is predetermined relative to the leverage outcomes being explained? The assessment does not ask this question anywhere, despite it being the core identification challenge in a structural paper.

**What is missing:** An explicit discussion of the independence (or lack thereof) between the ν_t measurement and the leverage moments used in SMM; a proposal for how to construct or instrument ν_t from data that is plausibly exogenous to contemporaneous firm leverage decisions; and an assessment of whether the bootstrap procedure described in the research spec (resampling firms with replacement) accounts for the time-series common-shock problem at all. It does not — bootstrapping firms handles cross-sectional sampling uncertainty but not time-series macro confounding.

---

### 3. Sample Selection — Mergent FISD Covers Only the Public Bond Market Upper Tail — MAJOR

**Deduction: -15 points**

The assessment acknowledges that Mergent FISD excludes bank loans, private placements, and equity issuances. It treats this as a "weakness" for Component C and a "known issue" for Component D. The severity of this exclusion is understated, and its consequences for κ identification specifically are not analyzed.

The research spec identifies κ as the bankruptcy cost parameter. The assessment correctly notes that credit spreads at issuance from Mergent FISD are the primary empirical moment for identifying κ. But the population of firms that issue public bonds is systematically different from the population of Compustat firms that appear in the leverage panel:

- Public bond issuers are large, rated, investment-grade or near-investment-grade firms.
- The leverage panel (Compustat) contains firms of all sizes including small, unrated firms that borrow exclusively from banks.
- The model's κ is a universal bankruptcy cost parameter applying to all firms in the model — but it is estimated from the credit spread moments of only the large-firm, bond-issuing subset.

This creates a sample-restriction problem for identification: κ is identified from the high-credit-quality upper tail but applied to the full cross-section. If large bond-issuing firms have structurally different bankruptcy costs (e.g., because they have more tangible assets, cleaner capital structures, lower reorganization costs) than the median Compustat firm, the estimated κ will be systematically biased for the broader population. The assessment does not discuss whether the estimated κ from bond spreads applies to the leverage moments from all Compustat firms, or whether this cross-sample inconsistency introduces bias into the SMM estimates.

The assessment also does not discuss the DealScan sample in sufficient depth. It mentions DealScan as a "secondary" source and provides feasibility notes, but does not analyze whether the loan spread distribution from DealScan could partially correct the Mergent FISD coverage gap by adding spreads from the bank loan market. Given that bank loans dominate total corporate debt for small and mid-sized firms — the very firms that drive cross-sectional leverage heterogeneity — the decision to treat DealScan as secondary deserves justification.

**What is missing:** An explicit analysis of the sample overlap between Compustat firms (leverage panel), Mergent FISD issuers (spread identification), and the theoretical model's target population (all nonfinancial firms). A Venn diagram or overlap table showing what fraction of firm-quarter observations in the leverage panel have a contemporaneous bond issuance in Mergent FISD (likely well under 10%) would make the coverage gap concrete. The assessment should have flagged this as a potential deal-breaker for κ identification, not a manageable weakness.

---

### 4. Measurement Validity — oancfy as Proxy for Model's Cash Flow X_i — MAJOR (Partial)

**Deduction: -10 points**

The assessment recommends `oancfy` (operating cash flow from operations, YTD) scaled by total assets as the empirical counterpart to the model's X_i — the firm's cash flow available to repay debt. The choice is defensible and is consistent with the structural estimation literature. However, the assessment contains an important conceptual omission.

The model's cash flow X_i (from the research spec) is the quantity that determines the firm's *ability to repay promised debt payments*. In standard structural models (Leland 1994, Merton 1974), this object is typically modeled as the firm's asset value or its earnings before interest. Operating cash flow (`oancfy`) excludes capital expenditures (which are cash *outflows* from investment), meaning a firm that invested heavily in a quarter has artificially low `oancfy` even if its underlying earning power is high. For capital-intensive firms with lumpy investment, this creates a systematic downward bias in estimated cash flow distributions μ_it that is not uniform across firms or time.

The standard alternative — free cash flow (oancfy minus capx) or EBITDA (`oibdpq`) — addresses this differently. The assessment lists both `oibdpq` and `ibq + dpq` as alternatives but does not advise on which is most appropriate for the theoretical construct. In particular, EBITDA is a *pre-tax, pre-interest* flow that represents the earnings available to all capital providers — which maps more naturally to the model's "cash flow available for distribution" than does operating cash flow (which already reflects some working capital movements).

This is not a fatal flaw — `oancfy` is used widely in the structural estimation literature — but the assessment should have:

1. Explicitly stated which theoretical quantity X_i is being proxied and why `oancfy` is the closest available counterpart.
2. Noted that `oancfy` is net of working capital changes while the model's X_i is typically not — and that firms with volatile working capital (retail, seasonal businesses) will have noisier μ_it estimates.
3. Recommended `oibdpq` (EBITDA) as a robustness check since it is pre-interest and maps more cleanly to the "earnings available to all capital providers" concept in the theory.

The partial deduction (−10 rather than −25) reflects that `oancfy` is a defensible choice that the literature accepts — but the omission of the proxy problem discussion means the paper will face referee questions about why EBITDA was not used, and the assessment provided no ammunition for that defense.

---

### 5. Identification Compatibility — LogNormal Assumption for Both μ_it and ν_t — MAJOR

**Deduction: -10 points**

The entire SMM design assumes that μ_it ~ LogNormal(α_it, σ_it²) estimated by rolling-window MLE, and that ν_t ~ LogNormal(α_ν(t), σ_ν²). The parameters of ν_t are then estimated via SMM. The assessment does not discuss whether this dual LogNormal assumption is testable or what the consequences are if it fails.

The problem is structural: if the true μ_it are not log-normal — if, for example, cash flow distributions are right-skewed with fat tails (which is empirically common in corporate finance, especially for young, high-growth firms) — then the estimated Wasserstein distance W1(μ_hat_it, ν_hat_t) is not the true W1 between the data-generating distributions. The bias in the moment conditions depends on how far the true distribution is from log-normal. Because the LogNormal assumption is maintained throughout (it is not tested or relaxed in the assessment's recommended approach), the SMM estimates of θ are inconsistent under misspecification of the functional form.

The research spec's Open Question #2 mentions "Robustness of rolling window estimation to departures from log-normality. Consider gamma or empirical CDF as alternatives" — but this is listed as a future concern. The assessment should have elevated this to a current empirical requirement: the paper needs a distributional fit test (Kolmogorov-Smirnov or Anderson-Darling on the within-firm rolling window residuals) to at least document whether log-normality is a reasonable first approximation for the cross-section of Compustat firms.

The assessment's Variable Table for Component A includes `ibq` (net income) and `dpq` (depreciation) alongside `oancfy` but does not use them; they appear as listed variables without purpose. This creates clutter without addressing the log-normality testing need.

**What is missing:** A test of log-normality for cash flow distributions on the Compustat panel; a discussion of what robustness checks are needed if log-normality is rejected for a nontrivial fraction of firms; and an acknowledgment that the W1 distance computed under the LogNormal assumption is only valid (as a structural moment) if the distributional assumption is approximately correct.

---

### 6. Sample Selection — Rolling Window Creates Time-Varying Sample Composition — MAJOR

**Deduction: -10 points**

The minimum 8-quarter rolling window requirement means that the SMM sample composition changes across time in a non-random way. The assessment acknowledges that "30–50% attrition relative to the raw panel" is expected when imposing the 8+ quarter minimum, but does not analyze when and which firms are excluded.

Firms are excluded from the sample in the following circumstances:
- During their first 2 years after IPO (insufficient history)
- After re-listing or major restructuring events (gap in quarterly data)
- During periods of accounting restatements (temporary reporting gaps)

Each of these exclusion causes is correlated with the outcome variable (leverage) and with the key regressor (W1 distance). IPO firms tend to have low leverage and high uncertainty — exactly the firms for which distributional mismatch would be large. Post-restructuring firms have just undergone a leverage change — exactly the moment of greatest theoretical interest. The rolling window requirement creates a sample that is systematically biased toward firms with stable, continuous operating histories.

The assessment mentions survivorship bias briefly: "Compustat is survivor-bias-free for listed firms (includes delistings back to the data's inception)." This is correct but addresses a different problem — Compustat including delistings does not address the rolling-window attrition problem. A firm that delisted is included in Compustat through its last quarter, but a firm that had a temporary data gap in the middle of its history is excluded from any rolling window spanning that gap. These are distinct issues.

**What is missing:** An analysis of the characteristics of the excluded population (firms with fewer than 8 consecutive quarters in a given rolling window) relative to the included population, on dimensions of size, leverage, credit rating, and industry. If the excluded firms are systematically different on leverage or W1 characteristics, the external validity of the SMM estimates is compromised even within the public-firm universe.

---

### 7. External Validity — Public Firm Coverage — MINOR (Already Partially Addressed)

**Deduction: -5 points**

The assessment does not discuss external validity of the Compustat-based leverage panel to the full corporate sector. The model (from the research spec) applies to a "continuum of firms" without restriction to listed firms. The empirical implementation covers only publicly listed US corporations — approximately 4,000–5,000 active firms at any given time.

Private US firms constitute roughly 99% of all US businesses by count and approximately 45–50% of total business revenues and employment. The leverage behavior of private firms is systematically different from public firms (lower average leverage, different debt maturity structure, heavier reliance on bank loans). If the model's predictions are calibrated to public firm leverage distributions, the welfare claims — particularly the aggregate deadweight cost W2²(μ, ν) — are estimated on a biased sample relative to the model's target population.

The assessment mentions this implicitly in the discussion of Mergent FISD coverage gaps but does not state it as an external validity limitation that affects the welfare interpretation of the structural estimates. Given that the paper's policy claims (financial intermediaries that reduce W2² are welfare-improving) apply to the full corporate sector, this is a real scope limitation.

The partial deduction (−5 rather than the full −15 for a missing external validity discussion) reflects that the restriction to public firms is standard in the structural capital structure literature and that the assessment at least implicitly acknowledges the coverage limitation even if it does not frame it as an external validity concern.

---

### 8. Known Issues — SFAS 95 Break and oancfy Construction — MINOR

**Deduction: -5 points**

The assessment correctly identifies SFAS 95 (1988) as the start date for `oancfy` reliability. However, it does not adequately describe the consequence of this structural break for the rolling-window MLE.

The problem: firms that existed before 1988 and survived to the post-1988 period will have rolling windows that, in the early part of the sample, span the 1988 accounting change. A firm with data from 1986–1993 will have its early rolling windows partially anchored to pre-SFAS-95 `fopty` values that were zero-imputed or substituted, depending on the researcher's handling. If the researcher uses the post-1988 sample starting point for all firms (which the assessment recommends, by starting the clean sample in 1988), then the first valid 8-quarter rolling window does not begin until 1990, and the first valid 20-quarter rolling window does not begin until 1993. This means the effective estimation sample for SMM cannot start until 1993 at earliest — not 1988 as implied by the recommended "primary sample period: 1988 Q1 — 2024 Q4."

The assessment notes the 1995 FISD start date creates a "sample period conflict" (Critical Gap #2) but conflates this with the 1988 SFAS 95 constraint. The more precise statement is: the fully identified SMM model — requiring both cash flow distributions (μ_hat_it from rolling windows) AND credit spreads at issuance (Mergent FISD) — cannot begin before 1995. The 1993–1994 period can contribute to the leverage panel but not to the spread identification. The assessment's recommended "primary sample period: 1988 Q1 — 2024 Q4" is misleading because the SMM cannot use the 1988–1994 observations for identifying all three parameters simultaneously.

**What is missing:** A clear delineation of which sample periods contribute to which identification moments:
- 1988–1994: leverage moments only (partial identification)
- 1995–2024: full identification (leverage + spreads)
The assessment should have recommended treating 1988–1994 as a pre-sample period for computing rolling μ_hat_it, with the actual SMM estimation sample beginning in 1995.

---

### 9. Known Issues — Offering Yield Variable Name and Missingness — MINOR (Partially Addressed)

**Deduction: -5 points**

The assessment correctly flags that `offering_yield` in Mergent FISD is UNVERIFIED and that missing yields are a known problem (Component D). However, it does not quantify the materiality of this issue for κ identification.

Academic users of Mergent FISD report that approximately 30–40% of bonds in the database do not have a populated offering yield. For high-yield bonds — the segment most relevant for κ identification, since high-spread observations provide the most identifying variation for bankruptcy costs — offering yield coverage is lower than for investment-grade bonds because many high-yield deals are privately placed (Rule 144A) and then registered, with the yield at registration differing from the yield at original issuance.

The assessment mentions a fallback (ICE BofA OAS indices), but these are aggregate series, not firm-level issuance spreads. Replacing firm-level spread moments with aggregate OAS moments fundamentally changes the identification strategy: κ would be identified from the time-series of aggregate spreads rather than from the cross-section of firm-level issuance spreads. This changes the nature of the SMM, not merely the data source.

The assessment should have quantified the expected offering yield coverage rate (or provided a SQL query to measure it) and discussed whether the remaining non-missing observations are a representative cross-section of the full bond universe or are systematically investment-grade-biased.

---

## Score Breakdown

- Starting score: 100
- ν_t proxy is theoretically indefensible (circular identification problem unnamed): -20
- ν_t and λ_it share common shocks — SMM independence assumption violated: -20
- Mergent FISD covers only bond market upper tail — κ identification sample too narrow: -15
- oancfy proxy problem understated — theory-variable mapping imprecise: -10
- LogNormal assumption untested — W1 moments inconsistent under misspecification: -10
- Rolling window creates non-random time-varying sample — selection bias unanalyzed: -10
- External validity — public firm restriction not discussed as scope limitation: -5
- SFAS 95 + rolling window → SMM sample start date misdescribed as 1988: -5
- offering_yield missingness materiality not quantified: -5
- **Final Score: 54/100**

---

## Summary Judgment

This assessment is thorough on the mechanics of data access and construction — the variable mnemonics, WRDS schema paths, CCM merge conventions, and winsorization choices are all correctly documented and appropriately hedged with UNVERIFIED flags. That operational layer is solid. The critical failure is structural: the assessment does not adequately engage with the two problems that will determine whether this paper can be published.

First, the measurement validity of ν_t is treated as a data sourcing challenge when it is actually a theoretical identification problem. The Mergent FISD bond deal-size approach measures an equilibrium outcome, not a supply primitive — and using it risks circular identification of the optimal transport model's core object. This needs to be resolved at the theory level before the data collection begins.

Second, the SMM design as described assumes that the data sources for the three parameter-identifying moment groups (leverage, spreads, and ν_t) are mutually independent. They share macro shocks. The assessment does not name this assumption or discuss how to defend it. A referee will.

The assessment can be revised to a passing standard by: (1) explicitly naming and proposing a solution to the circularity problem in ν_t estimation; (2) discussing how to partition or instrument around the common-shock contamination between ν_t and the leverage moments; and (3) delineating the true SMM estimation sample (1995–2024, not 1988–2024) with clarity about which observations contribute to which moment conditions.

**Strike 1:** This assessment must be revised before data collection proceeds.

---

*Review conducted by: data-quality-surveyor*
*Research project: Distributional Debt Capacity (SMM / Optimal Transport)*
*Review number: 1 of 3 (Strike 1)*
