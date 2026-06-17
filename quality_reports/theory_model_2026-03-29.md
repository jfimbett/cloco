# Theoretical Model — Liquid Assets

**Date:** 2026-03-29
**Agent:** econ-finance-theorist
**Phase:** Strategy / Theory Development
**Target:** `paper/sections/03_model.tex`

---

## 1. Model Setup

### Environment

We consider a static auction model for a single bottle of wine of age $a \geq 0$ with maturity date $\tau > 0$. The normalized age is $a^* = a / \tau$. Time is discrete: in each period, a bottle of a given normalized age is offered for sale in a second-price sealed-bid (Vickrey) auction. We model the cross-section of auction prices as a function of $a^*$, taking the supply of one bottle per auction as given.

### Agents

There are two types of risk-neutral buyers:

- **Consumption buyers (type $c$):** Value wine for drinking. Their willingness to pay depends on the wine's drinking quality, which is a function of its position in the life-cycle relative to maturity.

- **Collector buyers (type $k$):** Value wine for holding — as a store of value, prestige good, or future resale. Their willingness to pay depends on age-related scarcity and provenance, and is weakly increasing in age.

### Buyer Population

In the auction for a bottle of normalized age $a^*$, there are $n \geq 2$ potential bidders. Each bidder is independently drawn as type $c$ with probability $\lambda(a^*)$ and type $k$ with probability $1 - \lambda(a^*)$.

### Information Structure

Independent private values (IPV). Each bidder knows her own type and valuation. Types are drawn independently. The auction is second-price sealed-bid, so truthful bidding is a weakly dominant strategy.

---

## 2. Valuation Functions

### Assumption 1 (Consumption Valuation)

The consumption-buyer valuation is:

$$v_c(a^*) = \alpha_c \, h(a^*),$$

where $\alpha_c > 0$ is the maximum consumption value and $h : [0, \infty) \to [0,1]$ is a quality function satisfying:

1. $h(0) = 0$, $h(1) = 1$ (peak quality at maturity).
2. $h$ is strictly increasing on $[0, 1]$ and strictly decreasing on $(1, \infty)$.
3. $\lim_{a^* \to \infty} h(a^*) = 0$ (quality decays to zero past maturity).

A tractable parametric form:

$$h(a^*) = \left(\frac{a^*}{1}\right)^{\gamma} e^{\gamma(1 - a^*)} = (a^*)^\gamma \, e^{\gamma(1 - a^*)}, \quad \gamma > 0.$$

This is a Gamma-type density shape: it rises to a peak at $a^* = 1$ and decays exponentially thereafter. The parameter $\gamma$ controls peakedness — higher $\gamma$ means sharper peak and faster post-maturity decay.

### Assumption 2 (Collector Valuation)

The collector-buyer valuation is:

$$v_k(a^*) = \bar{v}_k + \alpha_k \, g(a^*),$$

where $\bar{v}_k > 0$ is the baseline collector value (the "price floor"), $\alpha_k \geq 0$ is the age-premium parameter, and $g : [0, \infty) \to [0, \infty)$ is weakly increasing with $g(0) = 0$.

A tractable form: $g(a^*) = a^*$, giving:

$$v_k(a^*) = \bar{v}_k + \alpha_k \, a^*.$$

This captures the idea that collector value has a level component (scarcity, prestige of holding fine wine) plus an age premium (older wines are rarer and more prestigious).

### Assumption 3 (Buyer Composition)

The probability that a bidder is a consumption buyer is:

$$\lambda(a^*) = \begin{cases} \bar{\lambda} & \text{if } a^* \leq 1, \\ \bar{\lambda} \, e^{-\delta(a^* - 1)} & \text{if } a^* > 1, \end{cases}$$

where $\bar{\lambda} \in (0, 1)$ is the baseline consumption-buyer share and $\delta > 0$ governs the rate of exit after maturity. Consumption buyers leave the market post-maturity because the wine is past its drinking peak — their reservation values decline, making them less likely to participate.

---

## 3. Equilibrium Price

### Second-Price Auction Equilibrium

Under IPV with truthful bidding, the auction price equals the second-highest bid, i.e., the second-highest valuation among the $n$ bidders.

**Notation.** Let $F_{(n-1:n)}(p; a^*)$ denote the CDF of the second-order statistic of $n$ i.i.d. draws from the mixture distribution:

$$F_V(v; a^*) = \lambda(a^*) \, \mathbf{1}[v \geq v_c(a^*)] + (1 - \lambda(a^*)) \, \mathbf{1}[v \geq v_k(a^*)].$$

Since each bidder has a deterministic valuation conditional on type (no within-type heterogeneity in the baseline model), the realized valuations in the auction are a random sample from the two-point distribution $\{v_c(a^*), v_k(a^*)\}$ with probabilities $\{\lambda(a^*), 1 - \lambda(a^*)\}$.

**Definition (Equilibrium Price).** The expected equilibrium auction price is:

$$P(a^*) = \mathbb{E}\left[V_{(n-1:n)} \mid a^*\right],$$

where $V_{(n-1:n)}$ is the second-highest order statistic of $n$ i.i.d. draws from the two-point distribution.

### Closed-Form Characterization

Let $\lambda = \lambda(a^*)$, $v_c = v_c(a^*)$, $v_k = v_k(a^*)$, and assume without loss of generality that we track which valuation is higher.

**Case 1: $v_c(a^*) > v_k(a^*)$ (pre-maturity and near-maturity).** The second-highest bid is $v_c$ if at least two bidders are type $c$, and $v_k$ if at most one bidder is type $c$. Thus:

$$P(a^*) = v_c(a^*) \cdot \left[1 - \binom{n}{0}\lambda^0(1-\lambda)^n - \binom{n}{1}\lambda^1(1-\lambda)^{n-1}\right] + v_k(a^*) \cdot \left[\binom{n}{0}\lambda^0(1-\lambda)^n + \binom{n}{1}\lambda^1(1-\lambda)^{n-1}\right].$$

Simplifying: let $q_0 = (1-\lambda)^n$ and $q_1 = n\lambda(1-\lambda)^{n-1}$. Then:

$$P(a^*) = v_c(a^*)(1 - q_0 - q_1) + v_k(a^*)(q_0 + q_1).$$

**Case 2: $v_k(a^*) > v_c(a^*)$ (post-maturity, when consumption value has decayed).** By symmetry:

$$P(a^*) = v_k(a^*)(1 - r_0 - r_1) + v_c(a^*)(r_0 + r_1),$$

where $r_0 = \lambda^n$ and $r_1 = n(1-\lambda)\lambda^{n-1}$.

**Case 3: $v_k(a^*) = v_c(a^*)$.** Then $P(a^*) = v_c(a^*) = v_k(a^*)$.

### General Formula

Unifying all cases:

$$P(a^*) = \max\{v_c, v_k\} \cdot \Pr[\text{at least 2 bidders have value } \max\{v_c, v_k\}] + \min\{v_c, v_k\} \cdot \Pr[\text{at most 1 bidder has value } \max\{v_c, v_k\}].$$

This is a weighted average of the two valuations, where the weight on the higher valuation equals the probability that the second-order statistic equals the higher value.

---

## 4. Key Results

### Proposition 1 (Non-Monotone Price-Age Profile)

Suppose $\alpha_c > \bar{v}_k + \alpha_k$ (consumption value at maturity exceeds collector value at maturity), $\gamma > 0$, $\delta > 0$, and $n \geq 2$. Then there exist $a^*_{\text{peak}}$ and $a^*_{\text{trough}}$ with $1 \leq a^*_{\text{peak}} < a^*_{\text{trough}}$ such that:

1. $P(a^*)$ is strictly increasing on $[0, a^*_{\text{peak}}]$.
2. $P(a^*)$ is strictly decreasing on $[a^*_{\text{peak}}, a^*_{\text{trough}}]$.
3. $P(a^*)$ is eventually increasing for $a^*$ sufficiently large.

**Proof sketch.**

*Phase 1 (Pre-maturity, $a^* \in [0,1]$):* Both $v_c(a^*)$ and $v_k(a^*)$ are increasing, and $\lambda$ is constant. Since $v_c(a^*) = \alpha_c h(a^*)$ is increasing toward its peak $\alpha_c$ and $v_k(a^*)$ is increasing, $P(a^*)$ is a weighted average of two increasing functions, hence increasing.

*Phase 2 (Post-maturity transition, $a^* > 1$):* Two forces operate simultaneously:

- **Composition effect:** $\lambda(a^*)$ falls, shifting weight from $v_c$ toward $v_k$. Since $v_c$ is still above $v_k$ in a neighborhood of $a^* = 1$ (by assumption $\alpha_c > \bar{v}_k + \alpha_k$), the probability that the second-highest bidder is type $c$ falls, reducing the price.

- **Valuation effect:** $v_c(a^*)$ decays while $v_k(a^*)$ continues to rise slowly.

The composition effect dominates near $a^* = 1$ because $v_c$ drops sharply (exponential decay controlled by $\gamma$) and $\lambda$ drops (controlled by $\delta$). Both reduce the weight on the high consumption valuation. Price falls.

*Phase 3 (Recovery):* As $a^* \to \infty$, $\lambda(a^*) \to 0$ and $v_c(a^*) \to 0$. The auction is populated almost entirely by collectors. The price converges to $v_k(a^*)$, which is increasing in $a^*$. The price eventually recovers and rises.

The trough occurs at the age where the declining composition effect (fewer consumption buyers supporting high prices) is exactly offset by the rising collector premium. $\square$

### Proposition 2 (Trough Disappearance — The Burgundy Grand Cru Case)

Define the "collector-dominance ratio":

$$\rho \equiv \frac{\bar{v}_k}{\alpha_c}.$$

There exists a threshold $\rho^* \in (0, 1)$ such that if $\rho > \rho^*$, then $P(a^*)$ is monotonically increasing for all $a^* \geq 0$.

**Proof sketch.**

When $\rho$ is large, $\bar{v}_k > \alpha_c h(a^*)$ for all $a^* \in [0, 1)$ sufficiently far from maturity — the collector floor exceeds the consumption valuation for young wines. This means:

1. Consumption buyers are effectively "priced out" even when young. They cannot win the auction because $v_k > v_c$ for most of the age range.
2. The equilibrium price is determined almost entirely by collector valuations, which are monotonically increasing.
3. Even near maturity where $v_c$ may briefly exceed $v_k$, the consumption-buyer share $\bar{\lambda}$ is small (in practice, consumption buyers self-select out of high-$\rho$ categories), so the price impact of the consumption peak is negligible.

Formally, when $\bar{v}_k \geq \alpha_c$ (i.e., $\rho \geq 1$), the collector valuation dominates the consumption valuation at all ages, and $P(a^*) = v_k(a^*)(1 - r_0 - r_1) + v_c(a^*)(r_0 + r_1)$ is increasing since the dominant term $v_k(a^*)$ is increasing and $v_c$ enters with vanishing weight. When $\rho < 1$ but $\rho > \rho^*$, the brief interval where $v_c > v_k$ is too narrow and the consumption-buyer share too small to generate a price decline. $\square$

**Empirical mapping.** The ratio $\rho$ maps directly to the observable "share of young lots priced above \$200/bottle":

| Category | $\rho$ (implied) | Young lots > \$200 | Trough |
|----------|------------------|--------------------|--------|
| Burgundy Grand Cru | High ($\rho > \rho^*$) | 51.5% | Absent |
| Bordeaux Crus Classés | Moderate ($\rho < \rho^*$) | 39.0% | Present (−26.2%) |
| Burgundy Premier Cru | Low ($\rho \ll \rho^*$) | 11.2% | Present (−22.4%) |

### Proposition 3 (Comparative Statics)

Define the trough depth as $\Delta(a^*) \equiv P(a^*_{\text{peak}}) - P(a^*_{\text{trough}})$ for a category with $\rho < \rho^*$.

1. $\Delta$ is increasing in $\bar{\lambda}$ (higher consumption-buyer share $\Rightarrow$ deeper trough).
2. $\Delta$ is decreasing in $\bar{v}_k$ (higher collector floor $\Rightarrow$ shallower trough).
3. $\Delta$ is increasing in $\gamma$ (sharper consumption peak $\Rightarrow$ faster post-maturity value decay $\Rightarrow$ deeper trough).
4. $\Delta$ is increasing in $\delta$ (faster consumption-buyer exit $\Rightarrow$ deeper trough).

**Proof sketch.**

(1) Higher $\bar{\lambda}$ means more consumption buyers compete for the bottle near maturity, raising the peak price. Post-maturity, these same buyers exit, so the price falls further before collectors dominate. The peak is higher and the trough lower.

(2) Higher $\bar{v}_k$ raises the price floor. Even when consumption buyers exit, the collector bid provides a higher outside option, truncating the price decline.

(3) Higher $\gamma$ sharpens the consumption valuation peak: $v_c(a^*)$ rises faster to maturity and decays faster afterward. The post-maturity decline in $v_c$ is steeper, pulling the auction price down more sharply.

(4) Higher $\delta$ accelerates the exit of consumption buyers post-maturity, reducing competition for the bottle in the transition zone and lowering the price before the collector premium dominates. $\square$

---

## 5. Empirical Predictions

### Prediction 1 (Non-Monotone Profile)
For wine categories where consumption buyers constitute a substantial fraction of bidders, the price-age profile should be non-monotone: rising pre-maturity, falling post-maturity, recovering at antique ages. **Confirmed** for Bordeaux Crus Classés and Burgundy Premier Cru.

### Prediction 2 (Trough Disappearance for High-Floor Wines)
Wine categories with a sufficiently high collector-dominance ratio $\rho$ — observable as a high share of young lots priced above \$200 — should exhibit a monotonically increasing price-age profile with no post-maturity trough. **Confirmed** for Burgundy Grand Cru.

### Prediction 3 (Cross-Sectional Variation in Trough Depth)
Across categories with a trough, the depth should be increasing in the consumption-buyer share (decreasing in $\rho$). Bordeaux Crus Classés (39% young lots above \$200) has a deeper trough (−26.2%) than Burgundy Premier Cru (11.2% above \$200, trough −22.4%). The ordering is consistent with the model only if Bordeaux has both a higher $\bar{\lambda}$ *and* other parameters (e.g., $\gamma$, $\delta$) that amplify the trough. The Burgundy Premier Cru trough being shallower despite a lower $\rho$ could reflect a less peaked consumption-valuation function or slower consumption-buyer exit for Burgundy wines.

### Prediction 4 (Monotone Pre-Maturity Rise)
All categories should exhibit rising prices pre-maturity, regardless of buyer composition — because both $v_c$ and $v_k$ are increasing before maturity. **Confirmed** for all three groups.

---

## 6. Relationship to Literature

The model builds on **Lovo and Spaenjers (2018, AER)**, who develop a heterogeneous-buyer model of art markets with consumption and investment (collector) types. Our model differs in three key respects:

1. **Finite consumption life.** Unlike art, wine has a biological maturity date after which consumption value declines. This generates the single-peaked consumption valuation $v_c(a^*)$ that is central to the non-monotone price profile.

2. **Observable maturity heterogeneity.** The maturity date $\tau$ varies across wines and is (imperfectly) observable via expert tasting notes. This provides cross-sectional variation in $a^*$ that identifies the model's predictions.

3. **Static auction mechanism.** We model a sequence of independent auctions rather than a dynamic search-and-matching model. This is appropriate for the institutional setting (French wine auctions are standard ascending auctions with many bidders per lot).

Relative to **Dimson, Mahajan, and Spaenjers (2015, RFS)**, who document long-run wine returns, our model explains *why* returns are non-uniform over the life-cycle — the composition of demand shifts endogenously as the wine ages.

---

## 7. Extensions

1. **Within-type heterogeneity.** Add noise to valuations: $\tilde{v}_c = v_c(a^*) + \epsilon_c$ and $\tilde{v}_k = v_k(a^*) + \epsilon_k$, where $\epsilon_c, \epsilon_k$ are i.i.d. draws from a continuous distribution. This smooths the price function and enables estimation via simulated method of moments.

2. **Endogenous supply.** Sellers choose when to bring bottles to auction. If consumption buyers exit post-maturity, sellers of post-maturity bottles face lower expected prices and may delay sale, creating a supply-side feedback that amplifies the trough.

3. **Dynamic collector resale.** Collectors who buy at the trough resell at antique ages. Forward-looking collectors should bid up to their expected resale value, potentially dampening the trough. The persistence of the trough in the data suggests transaction costs, storage costs, or authentication risk limit this arbitrage.

4. **Structural estimation.** The model's parameters ($\alpha_c$, $\bar{v}_k$, $\alpha_k$, $\gamma$, $\delta$, $\bar{\lambda}$) can be estimated using the observed price-age profiles and the cross-sectional variation across wine categories, using minimum distance or simulated method of moments.
