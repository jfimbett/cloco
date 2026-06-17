---
name: project-debt-capacity
description: Literature search results and anchors for the Distributional Debt Capacity paper (Wasserstein / Optimal Transport, EDHEC)
metadata:
  type: project
---

## Project Summary
Paper: Distributional Debt Capacity — uses W1/W2 Wasserstein distances between firm cash flow distributions (μit) and aggregate capital supply distribution (νt) to explain cross-sectional leverage and credit spreads. Data: TRACE (2012–2024), Compustat (1989–2024), FRED Flow of Funds.

## Proximity-5 Papers (Must Address Head-On)
- CollinDufresne2001determinants — JF — single residual factor in spread changes = supply/demand shock. W1 names this factor.
- GilchristZakrajsek2012credit — AER — excess bond premium (EBP). W1 provides cross-sectional analog.
- Nozawa2017cross — JF — cross-section of spreads: expected returns ≈ expected losses in variance shares.
- Siriwardane2019limited — JF — CDS capital shocks explain 12% of spread changes. TRACE/distribution approach is complement.
- BretscherSchmidSenSharma2026institutional — RFS 2026 Lead Article — demand-system equilibrium corporate bond pricing. Must frame as complementary (W1 = sufficient statistic for their demand-system output).

## Key Anchors Found
- AER: Gilchrist-Zakrajsek (2012), He-Krishnamurthy (2013), Brunnermeier-Sannikov (2014)
- JF: CDG (2001), Siriwardane (2019), Goldberg-Nozawa (2021), Huang-Nozawa-Shi (2025), Kuehn-Schmid (2014), Gomes-Schmid (2021), Greenwald-Krainer-Paul (2025)
- RFS: Chen-Collin-Dufresne-Goldstein (2009), Bhamra-Kuehn-Strebulaev (2010), Feldhutter-Schaefer (2018), ChernenkoSunderam (2012), Bretscher et al. (2026), Chen-Cui-He-Milbradt (2018), Erel et al. (2012), Faulkender-Petersen (2006), Rauh-Sufi (2010)
- JFE: Dick-Nielsen-Feldhutter-Lando (2012), Friewald-Jankowitsch-Subrahmanyam (2012), He-Kelly-Manela (2017)
- Econometrica: He-Milbradt (2014)
- AER Insights: Koijen-Yogo (2023)
- JFQA: Flannery-Nikolova-Oztekin (2012)
- JME: Ivashina-Laeven-Moral-Benito (2022)
- JF: Becker-Ivashina (2015), Benmelech-Kumar-Rajan (2024), Greenwood-Hanson-Shleifer-Sorensen (2022)

## Already Cited by Researcher (Skip)
Rajan-Zingales (1995), Frank-Goyal (2009), Baker-Wurgler (2002), Lemmon-Roberts-Zender (2008), DeAngelo-Roll (2015), Graham-Harvey (2001), Kashyap-Stein (2000), Khwaja-Mian (2008), Greenwood-Hanson (2013 RFS), Ivashina-Scharfstein (2010), Koijen-Yogo (2019 JPE), Massa-Yasuda-Zhang (2013 JFE), Zhu (2021 JFE), Lemmon-Roberts (2010 JFQA)

## Key Data Sources in This Literature
- TRACE (2002–present): Bond transaction data; accessed via WRDS/FINRA
- NAIC insurance holdings (quarterly): Used by Becker-Ivashina (2015), Bretscher et al.
- eMAXX institutional bond holdings: Used by Bretscher et al.
- Federal Reserve Flow of Funds (Z.1): Standard for aggregate intermediary balance sheets — validates νt
- Compustat: Standard for μit estimation (rolling cash flow windows)
- Moody's default database: Used by structural model papers (Huang-Huang, Chen et al.)

## Output Location
C:\Users\jfimb\Documents\cloco-debt\paper\quality_reports\lit_review_credit_spreads_capital_supply\

## No Scooping Risk Found
No SSRN/NBER working paper found combining "Wasserstein distance" + "corporate debt capacity" + "capital supply distribution" as of 2026-06-14.

**Why:** As of the search date, this literature review found no paper that (a) uses W1/W2 Wasserstein distances, (b) applied to corporate debt capacity, (c) using the Fréchet mean of firm distributions to recover the aggregate capital supply distribution. The risk is elevated only for Bretscher et al. (RFS 2026) as a demand-system comparator (already published) and Siriwardane (JF 2019) as a capital-shocks comparator (already published).
