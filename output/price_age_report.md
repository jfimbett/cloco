# Price-Age Analysis Report

**Date:** 2026-03-29  
**Sample:** 1,064,371 auction lots (after filters)  
**Price variable:** log(P_$/Bt_Combi)  
**Age variable:** sale_year − vintage (integer years, 0–100)  

---

## 1. Sample Description

**By region:**
- Bordeaux: 627,198
- Burgundy: 331,626
- Rhone: 105,547

**By region × wine type:**
Region              red      white      other
Bordeaux        581,926     42,137      3,135
Burgundy        224,472    104,071      3,083
Rhone            90,992     14,153        402

**By region × maturity stage (lots with maturity data only):**
Region               pre   in_window        post     unknown
Bordeaux         525,592           2          18     101,586
Burgundy         140,560          96           0     190,970
Rhone             53,711           0           0      51,836

**By bottle size:**
- standard: 965,530 (90.7%)
- magnum: 45,594 (4.3%)
- large: 35,993 (3.4%)
- small: 17,234 (1.6%)
- half_mag: 20 (0.0%)

---

## 2. Binned Medians (log price per bottle)

Median log-price by region and 2-year age bin. Log-price is log(USD per bottle).

### Bordeaux
Age bin           N   Median     Mean      IQR
----------------------------------------------
0-2           1,085    4.536    4.675    1.959
2-4          23,189    4.454    4.623    1.650
4-6          57,679    4.654    4.844    1.716
6-8          53,702    4.696    4.846    1.783
8-10         50,997    4.796    4.945    1.875
10-12        51,809    5.033    5.178    1.842
12-14        47,534    5.104    5.238    1.766
14-16        43,779    5.127    5.239    1.754
16-18        38,835    5.180    5.227    1.646
18-20        34,340    5.297    5.325    1.585
20-22        28,236    5.481    5.455    1.710
22-24        28,069    5.586    5.502    1.765
24-26        25,712    5.731    5.679    1.891
26-28        21,397    5.620    5.547    1.975
28-30        19,046    5.825    5.830    1.960
30-32        15,273    5.728    5.733    1.959
32-34        12,208    5.629    5.665    1.944
34-36         7,289    5.033    5.166    1.664
36-38         7,141    5.385    5.368    1.659
38-40         6,205    5.458    5.511    1.670
40-42         5,531    5.713    5.745    1.794
42-44         5,022    5.768    5.777    1.760
44-46         5,882    5.905    5.934    1.830
46-48         4,724    6.198    6.234    1.825
48-50         3,647    6.355    6.376    1.801
50-52         4,317    6.646    6.618    1.734
52-54         3,912    6.893    6.913    1.647
54-56         3,020    6.824    6.788    1.605
56-58         2,245    6.762    6.758    1.550
58-60         2,156    6.854    6.869    1.525
60+          13,042    6.854    6.882    1.654

### Burgundy
Age bin           N   Median     Mean      IQR
----------------------------------------------
0-2              56    4.653    4.551    0.623
2-4          22,708    4.563    4.763    1.291
4-6          44,455    4.763    4.963    1.618
6-8          42,285    4.942    5.092    1.845
8-10         39,798    5.106    5.239    1.880
10-12        33,002    5.335    5.457    1.829
12-14        26,661    5.557    5.613    1.881
14-16        21,659    5.747    5.757    1.938
16-18        18,322    5.908    5.925    1.938
18-20        14,823    6.061    6.041    1.945
20-22        10,495    6.354    6.326    2.018
22-24         9,779    6.571    6.481    1.967
24-26         8,096    6.641    6.553    1.990
26-28         5,607    6.665    6.579    2.078
28-30         5,124    6.725    6.651    2.219
30-32         3,072    6.579    6.521    2.233
32-34         2,169    6.629    6.550    2.559
34-36         2,476    6.729    6.673    2.328
36-38         2,568    6.717    6.733    2.359
38-40         1,964    6.811    6.691    2.028
40-42         1,895    6.811    6.779    1.936
42-44         1,932    6.873    6.829    2.080
44-46         1,935    6.888    6.872    2.052
46-48         1,705    6.924    6.896    1.947
48-50         1,296    7.135    7.049    1.736
50-52         1,201    6.973    6.912    1.895
52-54           909    7.030    6.791    1.910
54-56           746    6.760    6.683    1.734
56-58           730    7.102    7.048    1.786
58-60           589    7.018    7.045    1.597
60+           3,567    6.907    7.068    1.899

### Rhone
Age bin           N   Median     Mean      IQR
----------------------------------------------
2-4           7,652    4.290    4.339    1.061
4-6          18,545    4.500    4.532    1.197
6-8          17,178    4.536    4.569    1.244
8-10         13,418    4.605    4.673    1.244
10-12        10,126    4.687    4.780    1.452
12-14         7,938    4.739    4.841    1.466
14-16         6,195    4.768    4.913    1.494
16-18         5,594    5.158    5.221    1.705
18-20         4,487    5.389    5.306    1.783
20-22         3,056    5.517    5.446    1.824
22-24         3,025    5.509    5.509    1.725
24-26         2,685    5.804    5.676    1.608
26-28         1,273    5.465    5.458    1.875
28-30         1,037    5.656    5.795    2.011
30-32           784    5.643    5.683    2.030
32-34           441    5.746    5.817    1.933
34-36           376    6.681    6.187    2.057
36-38           353    6.514    6.228    2.211
38-40           191    5.777    6.021    1.812
40-42           150    5.903    6.149    2.109
42-44           130    6.342    6.230    2.083
44-46           176    7.142    6.828    2.688
46-48           174    7.855    7.593    2.402
48-50           113    7.516    7.232    2.623
50-52           124    6.959    7.032    3.927
52-54            85    8.271    7.794    2.407
54-56            55    6.733    6.990    2.247
56-58            29    6.640    6.972    1.917
58-60            40    7.021    6.820    1.992
60+             107    6.842    6.927    1.435

**Predicted log-price from Spec 2 polynomial at key ages:**
Age       Bordeaux    Burgundy       Rhone
------------------------------------------
2            4.737       4.636       4.370
5            4.854       4.963       4.506
10           5.042       5.441       4.759
15           5.221       5.838       5.035
20           5.392       6.162       5.328
30           5.713       6.620       5.923
40           6.007       6.873       6.476
50           6.280       6.977       6.916
60           6.537       6.988       7.173

---

## 3. Polynomial Regression Results

Robust (HC1) standard errors in parentheses. * p<0.10, ** p<0.05, *** p<0.01

### Spec 1 — Pooled cubic (no fixed effects)
Dependent variable: log_price | N = 1,064,371 | R² = 0.1411

  age                                                     0.0716*** (0.0005)
  age2                                                    -0.0009*** (0.0000)
  age3                                                    0.0000*** (0.0000)
  C(Region)[T.Burgundy]                                   0.4634*** (0.0030)
  C(Region)[T.Rhone]                                      -0.1793*** (0.0036)

### Spec 2 — Region × cubic interactions (no fixed effects)
Dependent variable: log_price | N = 1,064,371 | R² = 0.1502

  age                                                     0.0404*** (0.0007)
  age2                                                    -0.0002*** (0.0000)
  age3                                                    0.0000*** (0.0000)
  C(Region)[T.Burgundy]                                   -0.2576*** (0.0088)
  C(Region)[T.Rhone]                                      -0.3705*** (0.0118)
  age:C(Region)[T.Burgundy]                               0.0816*** (0.0012)
  age:C(Region)[T.Rhone]                                  -0.0004 (0.0022)
  age2:C(Region)[T.Burgundy]                              -0.0017*** (0.0000)
  age2:C(Region)[T.Rhone]                                 0.0010*** (0.0001)
  age3:C(Region)[T.Burgundy]                              0.0000*** (0.0000)
  age3:C(Region)[T.Rhone]                                 -0.0000*** (0.0000)

### Spec 3 — Hedonic: producer within-demeaning + vintage + auction house FE
Dependent variable: log_price (producer-demeaned) | N = 1,064,371 | R² = 0.3967

  age                                                     0.0347*** (0.0006)
  age2                                                    0.0008*** (0.0000)
  age3                                                    -0.0000*** (0.0000)
  C(Region)[T.Burgundy]                                   -0.0697*** (0.0062)
  C(Region)[T.Rhone]                                      0.2886*** (0.0110)
  age:C(Region)[T.Burgundy]                               0.0160*** (0.0009)
  age:C(Region)[T.Rhone]                                  -0.0448*** (0.0022)
  age2:C(Region)[T.Burgundy]                              0.0001*** (0.0000)
  age2:C(Region)[T.Rhone]                                 0.0029*** (0.0001)
  age3:C(Region)[T.Burgundy]                              -0.0000*** (0.0000)
  age3:C(Region)[T.Rhone]                                 -0.0000*** (0.0000)

*Maturity stage, wine type, bottle size, vintage FE, and auction house FE included but not shown above.*

---

## 4. Turning Points by Region

Price trough = age where d(log_price)/d(age) = 0 and 2nd derivative > 0 (local minimum).
Price peak = age where d(log_price)/d(age) = 0 and 2nd derivative < 0 (local maximum).
All roots restricted to age ∈ [0, 100].

Spec                      Region         Trough (yrs)   Peak (yrs)
------------------------------------------------------------------
Spec 2 (no FE)            Bordeaux                  —            —
Spec 2 (no FE)            Burgundy               75.9         56.5
Spec 2 (no FE)            Rhone                     —         65.3
Spec 3 (producer FE)      Bordeaux                  —            —
Spec 3 (producer FE)      Burgundy                  —         80.8
Spec 3 (producer FE)      Rhone                   1.4         66.9

---

## 5. Maturity Stage Premia (Spec 3)

Coefficients relative to baseline stage (pre-maturity).

Parameter                                                Coef         SE      p-val
----------------------------------------------------------------------------------
C(maturity_stage)[T.post]                             -0.2201     0.1645     0.1810
C(maturity_stage)[T.pre]                              -0.0200     0.0821     0.8078
C(maturity_stage)[T.unknown]                           0.0155     0.0821     0.8500

## 6. Wine Type and Bottle Size Premia (Spec 3)

**Wine type** (relative to 'other'):
  C(wine_type)[T.red]                                0.3742*** (0.0101)
  C(wine_type)[T.white]                              0.5577*** (0.0103)

**Bottle size** (relative to 'half_mag' or first category):
  C(bottle_size_cat)[T.large]                        1.8453*** (0.3044)
  C(bottle_size_cat)[T.magnum]                       0.7013** (0.3044)
  C(bottle_size_cat)[T.small]                        -0.7451** (0.3044)
  C(bottle_size_cat)[T.standard]                     -0.0981 (0.3044)

---

## 7. Key Findings

*(Auto-generated from regression results)*

- **Bordeaux:** No turning points found within age 0–100 (monotone profile).
- **Burgundy:** Price reaches a local maximum at ~80.8 years (no trough within age 0–100).
- **Rhone:** Price reaches a local minimum at ~1.4 years and a local maximum at ~66.9 years of age (Spec 3).

- **Post-maturity:** Lots sold past their peak drinking window trade at a 22.0% discount vs pre-maturity lots.
- **Wine type:** Red wines trade at exp(0.374)=1.454x relative to other; white at exp(0.558)=1.747x.
- **Magnum premium:** Magnums trade at a 70.1% premium per bottle vs standard (exp=2.016).
