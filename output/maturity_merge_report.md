# Maturity Merge Report

**Date:** 2026-03-29  
**Auction rows:** 1,068,703  
**Tastingbook rows:** 17,701  

---

## 1. Match Rates by Stage

| Stage | Count | % of auction |
|-------|-------|--------------|
| fuzzy | 448,098 | 41.9% |
| producer_vintage | 279,556 | 26.2% |
| unmatched | 256,296 | 24.0% |
| producer_avg | 81,447 | 7.6% |
| exact | 3,306 | 0.3% |

**Total matched:** 812,407 / 1,068,703 (76.0%)

---

## 2. Distribution of years_to_maturity

- N: 812,407
- Mean: 37.8 years
- Median: 34.0 years
- Std: 14.9 years
- Range: [8, 242]
- 10th pct: 23.5
- 90th pct: 56.0

---

## 3. Distribution of age_relative_to_maturity

- N: 812,407
- Mean: -20.3 years
- Median: -20.0 years
- Std: 5.9 years
- Range: [-47, 92]
- % pre-maturity (< 0): 100.0%
- % at maturity ([-1,1]): 0.0%
- % post-maturity (> 0): 0.0%

---

## 4. Match Rates by Region

```
Region    maturity_source 
Bordeaux  fuzzy               47.5
          producer_vintage    36.9
          unmatched            7.6
          producer_avg         7.5
          exact                0.5
Burgundy  unmatched           51.6
          fuzzy               29.8
          producer_vintage    13.0
          producer_avg         5.6
Loire     producer_vintage    56.7
          fuzzy               39.7
          unmatched            3.2
          producer_avg         0.4
Rhone     fuzzy               46.9
          unmatched           34.1
          producer_avg        15.0
          producer_vintage     3.8
          exact                0.2
```

---

## 5. Data Quality Notes

- Tastingbook coverage: 829 unique producers across Bordeaux, Burgundy, Rhône
- Burgundy and Rhône now partially covered via sitemap rescrape (05_scrape_tastingbook.py)
- 'producer_avg' matches use the mean maturity peak across all vintages for the producer
- 'fuzzy' matches use difflib SequenceMatcher >= 0.80 on producer name
- 'exact' matches on (norm_producer, norm_wine, vintage) — most reliable
- 'producer_vintage' matches on (norm_producer, vintage) using main-wine entry

---

## 6. Bimodal Pattern Test

- Pre-maturity (< -2 yrs): 812,177 lots
- At maturity (±2 yrs):    0 lots
- Post-maturity (> +2 yrs): 230 lots

Bimodal pattern: visible if there is a dip in volume / price near 0 (consumption consumption window)
and separate peaks before (young investor demand) and after (drinking window) maturity.