# Price–Normalized-Age Analysis Report

**Date:** 2026-03-29  
**Sample:** 1,048,899 auction lots  
**Key variable:** age_norm = (sale_year − vintage) / years_to_maturity_final  
  → 0.0 = vintage year, 1.0 = maturity peak, >1.0 = past peak  

---

## 1. Sample Description

- Lots with TB maturity (imputed=False): 796,480 (75.9%)
- Lots with imputed maturity: 252,419 (24.1%)

**By region:**
- Bordeaux: 615,078
- Burgundy: 328,371
- Rhone: 105,450

**age_norm at maturity boundaries:**
  - age_norm < 1.0 → pre-maturity or approaching maturity
  - age_norm = 1.0 → at maturity peak
  - age_norm > 1.0 → past maturity peak

- Mean: 0.78
- Median: 0.60
- 10th–90th pct: [0.21, 1.55]
- Pre-maturity (age_norm < 1): 72.3%
- Post-maturity (age_norm > 1): 25.7%

---

## 2. Binned Medians (log price by normalized age)

Each bin is 0.1 units of age_norm. Key threshold: bin 0.9–1.0 = approaching maturity; bin 1.0–1.1 = just past maturity.

### Bordeaux
age_norm_bin          N     Median       Mean        IQR
--------------------------------------------------------
0.0-0.1           1,083      4.536      4.677      1.959
0.1-0.2          23,061      4.445      4.620      1.638
0.2-0.3          82,308      4.658      4.827      1.710
0.3-0.4          28,603      4.724      4.907      1.948
0.4-0.5          51,235      4.787      4.940      1.869
0.5-0.6          77,326      5.054      5.196      1.832
0.6-0.7          44,318      5.116      5.230      1.725
0.7-0.8          21,839      5.134      5.254      1.793
0.8-0.9          38,836      5.180      5.227      1.646
0.9-1.0          34,340      5.297      5.325      1.585
1.0-1.1          28,236      5.481      5.455      1.710
1.1-1.2          40,627      5.631      5.549      1.783
1.2-1.3          13,154      5.764      5.703      1.963
1.3-1.4          30,679      5.681      5.628      1.978
1.4-1.5           9,764      5.830      5.844      1.983
1.5-1.6          15,273      5.728      5.733      1.959
1.6-1.7          15,694      5.511      5.543      1.932
1.7-1.8           3,803      5.054      5.210      1.640
1.8-1.9          10,166      5.372      5.400      1.627
1.9-2.0           3,180      5.523      5.544      1.758
2.0-3.0          40,456      6.310      6.291      1.836

### Burgundy
age_norm_bin          N     Median       Mean        IQR
--------------------------------------------------------
0.0-0.1              56      4.653      4.551      0.623
0.1-0.2          22,017      4.554      4.717      1.248
0.2-0.3          61,315      4.775      4.963      1.662
0.3-0.4          25,090      5.039      5.184      1.913
0.4-0.5          40,248      5.115      5.250      1.889
0.5-0.6          47,102      5.394      5.492      1.841
0.6-0.7          24,205      5.631      5.677      1.919
0.7-0.8          10,587      5.817      5.802      1.943
0.8-0.9          18,326      5.907      5.924      1.939
0.9-1.0          14,823      6.061      6.041      1.945
1.0-1.1          10,495      6.354      6.326      2.018
1.1-1.2          13,919      6.596      6.520      1.945
1.2-1.3           3,956      6.577      6.491      2.180
1.3-1.4           8,055      6.680      6.601      2.199
1.4-1.5           2,676      6.699      6.651      2.122
1.5-1.6           3,072      6.579      6.521      2.233
1.6-1.7           3,428      6.639      6.546      2.537
1.7-1.8           1,217      6.887      6.812      2.305
1.8-1.9           3,560      6.750      6.734      2.277
1.9-2.0             972      6.759      6.644      2.076
2.0-3.0          12,938      6.924      6.878      1.909

### Rhone
age_norm_bin          N     Median       Mean        IQR
--------------------------------------------------------
0.0-0.1               9      4.094      3.605      1.106
0.1-0.2           7,622      4.290      4.337      1.061
0.2-0.3          26,935      4.500      4.519      1.197
0.3-0.4           8,732      4.601      4.641      1.360
0.4-0.5          13,479      4.605      4.673      1.245
0.5-0.6          14,378      4.700      4.802      1.460
0.6-0.7           6,926      4.701      4.830      1.427
0.7-0.8           2,980      4.860      4.997      1.602
0.8-0.9           5,594      5.158      5.221      1.705
0.9-1.0           4,487      5.389      5.306      1.783
1.0-1.1           3,056      5.517      5.446      1.824
1.1-1.2           4,419      5.635      5.563      1.660
1.2-1.3           1,291      5.873      5.670      1.707
1.3-1.4           1,777      5.489      5.516      1.896
1.4-1.5             533      5.790      5.918      2.124
1.5-1.6             784      5.643      5.683      2.030
1.6-1.7             621      5.777      5.931      2.016
1.7-1.8             196      6.658      6.166      2.004
1.8-1.9             476      6.395      6.212      2.054
1.9-2.0              68      5.693      5.759      1.836
2.0-3.0           1,076      6.925      6.939      2.674

---

## 3. Polynomial Regression Results

Robust (HC1) standard errors in parentheses. * p<0.10, ** p<0.05, *** p<0.01

### Spec 1 — Pooled cubic (no FE)
Dependent variable: log_price | N = 1,048,899 | R² = 0.1302

  an                                                 2.2605*** (0.0170)
  an2                                                -1.1837*** (0.0156)
  an3                                                0.2526*** (0.0039)
  C(Region)[T.Burgundy]                              0.4627*** (0.0030)
  C(Region)[T.Rhone]                                 -0.1776*** (0.0036)

### Spec 2 — Region × cubic (no FE)
Dependent variable: log_price | N = 1,048,899 | R² = 0.1402

  an                                                 1.8942*** (0.0221)
  an2                                                -1.1432*** (0.0194)
  an3                                                0.2777*** (0.0047)
  C(Region)[T.Burgundy]                              -0.0346*** (0.0109)
  an:C(Region)[T.Burgundy]                           0.6188*** (0.0391)
  an2:C(Region)[T.Burgundy]                          0.3797*** (0.0369)
  an3:C(Region)[T.Burgundy]                          -0.2109*** (0.0093)
  C(Region)[T.Rhone]                                 -0.1616*** (0.0139)
  an:C(Region)[T.Rhone]                              -0.8436*** (0.0585)
  an2:C(Region)[T.Rhone]                             1.1873*** (0.0641)
  an3:C(Region)[T.Rhone]                             -0.2841*** (0.0189)

### Spec 3 — Hedonic (producer demeaning + FE)
Dependent variable: log_price_dm | N = 1,048,899 | R² = 0.3877

  an                                                 0.7869*** (0.0143)
  an2                                                0.2549*** (0.0131)
  an3                                                -0.0447*** (0.0034)
  C(Region)[T.Burgundy]                              0.1196*** (0.0076)
  an:C(Region)[T.Burgundy]                           -0.6091*** (0.0276)
  an2:C(Region)[T.Burgundy]                          1.0138*** (0.0267)
  an3:C(Region)[T.Burgundy]                          -0.2833*** (0.0069)
  C(Region)[T.Rhone]                                 0.3432*** (0.0117)
  an:C(Region)[T.Rhone]                              -1.2219*** (0.0498)
  an2:C(Region)[T.Rhone]                             1.5043*** (0.0549)
  an3:C(Region)[T.Rhone]                             -0.3284*** (0.0162)

---

## 4. Turning Points in Normalized Age Space

Trough = local minimum; Peak = local maximum. Values are in units of age_norm (1.0 = maturity peak).

Spec                       Region                 Trough               Peak
---------------------------------------------------------------------------
Spec 2 (no FE)             Bordeaux                    —                  —
Spec 2 (no FE)             Burgundy                    —              2.404
Spec 2 (no FE)             Rhone                       —                  —
Spec 3 (producer FE)       Bordeaux                    —                  —
Spec 3 (producer FE)       Burgundy                    —              2.647
Spec 3 (producer FE)       Rhone                   0.129                  —

---

## 5. Maturity Stage Premia (Spec 3)

  C(maturity_stage)[T.pre]                     0.4267   SE=0.0824   p=0.0000
  C(maturity_stage)[T.unknown]                 0.4646   SE=0.0824   p=0.0000

---

## 6. Shape of Price-Age Profile (Key Finding)

**Predicted log-price from Spec 2 polynomial at key normalized age values:**
age_norm      Bordeaux      Burgundy      Rhone       
------------------------------------------------------
0.2           4.731         4.834         4.446       
0.4           4.989         5.249         4.661       
0.6           5.181         5.609         4.879       
0.8           5.322         5.917         5.100       
1.0           5.425         6.178         5.323       
1.2           5.503         6.393         5.548       
1.5           5.602         6.639         5.888       
2.0           5.833         6.868         6.461       

---

## 7. Key Findings

*(Auto-generated from regression results)*

- **Bordeaux:** Monotone profile — no trough or peak found within age_norm ∈ [0, 3].
- **Burgundy:** Price peaks at age_norm=2.647 (past maturity) with no trough. Monotone increase up to ~2.647x maturity.
- **Rhone:** Price shows a trough at age_norm=0.129 then rises. No peak found within age_norm ≤ 3.

- **Post- vs pre-maturity (raw medians):** Lots past peak (age_norm > 1) trade at +63.2% vs lots approaching maturity (age_norm 0.8–1.0). N(post)=269,450, N(pre)=116,406.

- **Post-maturity lot count:** 269,450 lots (25.7%) have age_norm > 1.0 (sold past maturity peak).
- **Pre-maturity concentration:** 72.3% of lots were sold before reaching maturity peak — consistent with investment/speculative demand dominating auction supply.