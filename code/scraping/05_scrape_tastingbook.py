"""
Script  : 05_scrape_tastingbook.py
Purpose : Sitemap-based Tastingbook scraper.
            1. Downloads the public Tastingbook sitemaps (no auth needed)
            2. Extracts all wine URLs + producer slugs (61k+ URLs, 6k+ producers)
            3. Fuzzy-matches auction producers to sitemap producer slugs
            4. Scrapes #status-statistics (When to drink) for matched wine pages
            5. Merges with existing Xin Ning data → combined output

Input   : data/processed/auction_with_maturity.parquet  (unmatched lots)
          data/raw/tastingbook_xin_ning/data.xlsx        (existing scraped data)

Output  : data/raw/tastingbook_rescrape/sitemap_urls.csv      (all sitemap URLs, cached)
          data/raw/tastingbook_rescrape/producer_matches.csv  (auction→tb slug map)
          data/raw/tastingbook_rescrape/new_scrape.parquet    (newly scraped rows)
          data/raw/tastingbook_rescrape/data_combined.xlsx    (existing + new, deduped)

Usage   : python code/scraping/05_scrape_tastingbook.py
          python code/scraping/05_scrape_tastingbook.py --dry-run
          python code/scraping/05_scrape_tastingbook.py --step 1   # sitemap only
          python code/scraping/05_scrape_tastingbook.py --step 2   # match only
          python code/scraping/05_scrape_tastingbook.py --step 3   # scrape only
          python code/scraping/05_scrape_tastingbook.py --workers 16
          python code/scraping/05_scrape_tastingbook.py --max-pages 500

Requirements : requests, beautifulsoup4, lxml, pandas, openpyxl
"""

from __future__ import annotations

import argparse
import gzip
import io
import re
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT         = Path(__file__).resolve().parent.parent.parent
EXISTING_TB  = ROOT / "data" / "raw" / "tastingbook_xin_ning" / "data.xlsx"
AUCTION_PATH = ROOT / "data" / "processed" / "auction_with_maturity.parquet"
OUT_DIR      = ROOT / "data" / "raw" / "tastingbook_rescrape"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SITEMAP_CACHE = OUT_DIR / "sitemap_urls.csv"
MATCHES_OUT   = OUT_DIR / "producer_matches.csv"
SCRAPE_OUT    = OUT_DIR / "new_scrape.parquet"
COMBINED_OUT  = OUT_DIR / "data_combined.xlsx"

SITEMAP_URLS = [
    "https://tastingbook.com/sitemaps/publicsitemap.xml.gz",
    "https://tastingbook.com/sitemaps/publicsitemap-1.xml.gz",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize(s: str) -> str:
    """Lowercase, strip accents, remove punctuation, collapse spaces."""
    if not s or pd.isna(s):
        return ""
    s = str(s).lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", errors="ignore").decode()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def slug_to_words(slug: str) -> str:
    """Convert a TB slug like 'chateau_lynchbages' → 'chateau lynchbages'."""
    return slug.replace("_", " ").lower()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


# ---------------------------------------------------------------------------
# Step 1 — Download & cache sitemaps
# ---------------------------------------------------------------------------

def step1_download_sitemaps(force: bool = False) -> pd.DataFrame:
    """
    Download Tastingbook sitemaps and return DataFrame of wine URLs.
    Caches to SITEMAP_CACHE so subsequent runs skip the download.
    """
    if SITEMAP_CACHE.exists() and not force:
        print(f"  [cached] Loading sitemap from {SITEMAP_CACHE}")
        df = pd.read_csv(SITEMAP_CACHE)
        print(f"  {len(df):,} wine URLs, {df['producer_slug'].nunique():,} producers")
        return df

    session = make_session()
    all_urls: list[str] = []

    for url in SITEMAP_URLS:
        print(f"  Downloading {url} ...", end=" ", flush=True)
        r = session.get(url, timeout=60)
        r.raise_for_status()
        content = gzip.decompress(r.content).decode("utf-8")
        found = re.findall(r"<loc>(https://tastingbook\.com/wine/[^<]+)</loc>", content)
        all_urls.extend(found)
        print(f"{len(found):,} URLs")

    # Deduplicate
    all_urls = list(dict.fromkeys(all_urls))

    # Parse into columns
    rows = []
    for url in all_urls:
        m = re.match(r"https://tastingbook\.com/wine/([^/]+)/(.+)", url)
        if not m:
            continue
        producer_slug = m.group(1)
        wine_vintage  = m.group(2)
        # Extract vintage: last 4-digit number
        vm = re.search(r"_(\d{4})$", wine_vintage)
        vintage = int(vm.group(1)) if vm else None
        wine_slug = wine_vintage[: vm.start()] if vm else wine_vintage
        rows.append({
            "url": url,
            "producer_slug": producer_slug,
            "wine_slug": wine_slug,
            "vintage": vintage,
        })

    df = pd.DataFrame(rows)
    df.to_csv(SITEMAP_CACHE, index=False)
    print(f"  Saved {len(df):,} wine URLs ({df['producer_slug'].nunique():,} producers) → {SITEMAP_CACHE}")
    return df


# ---------------------------------------------------------------------------
# Step 2 — Match auction producers → sitemap producer slugs
# ---------------------------------------------------------------------------

def step2_match_producers(
    sitemap_df: pd.DataFrame,
    min_lots: int = 100,
    threshold: float = 0.70,
    force: bool = False,
) -> pd.DataFrame:
    """
    Fuzzy-match unmatched auction producers to Tastingbook producer slugs.
    Returns a DataFrame with columns: auction_producer, tb_slug, score, lots.
    """
    if MATCHES_OUT.exists() and not force:
        print(f"  [cached] Loading producer matches from {MATCHES_OUT}")
        df = pd.read_csv(MATCHES_OUT)
        print(f"  {len(df):,} matched producers")
        return df

    # Load auction unmatched producers
    print("  Loading auction data ...", end=" ", flush=True)
    auction = pd.read_parquet(AUCTION_PATH, columns=["norm_producer", "Region", "maturity_source"])
    unmatched = auction[auction["maturity_source"] == "unmatched"]
    producer_lots = (
        unmatched.groupby("norm_producer")
        .size()
        .reset_index(name="lots")
        .query("lots >= @min_lots")
        .sort_values("lots", ascending=False)
    )
    print(f"{len(producer_lots):,} auction producers with >= {min_lots} unmatched lots")

    # Build normalized TB slug lookup
    tb_producers = sitemap_df["producer_slug"].unique()
    tb_norm = {slug: normalize(slug_to_words(slug)) for slug in tb_producers}
    tb_norm_inv = {}
    for slug, norm in tb_norm.items():
        tb_norm_inv.setdefault(norm, slug)  # keep first if collision

    # For each auction producer, try exact → containment → fuzzy match
    rows = []
    for _, row in producer_lots.iterrows():
        ap = row["norm_producer"]
        lots = row["lots"]

        # 1. Exact normalized match
        if ap in tb_norm_inv:
            rows.append({"auction_producer": ap, "tb_slug": tb_norm_inv[ap],
                         "score": 1.0, "lots": lots, "match_type": "exact"})
            continue

        # 2. Word-boundary match — handles "ramonet" → "domaine ramonet",
        #    "leroy" → "domaine leroy", "armand rousseau" → "domaine armand rousseau"
        #    Require every word in the auction name to appear in the TB slug.
        ap_words = ap.split()
        word_slug, word_score = None, 0.0
        for slug, norm in tb_norm.items():
            norm_words = set(norm.split())
            if all(w in norm_words for w in ap_words):
                # Score: ratio of matched words to total TB words (penalise long slugs)
                s = len(ap_words) / len(norm_words)
                if s > word_score:
                    word_score, word_slug = s, slug

        if word_score >= 0.5:                       # auction name covers ≥ 50% of TB words
            rows.append({"auction_producer": ap, "tb_slug": word_slug,
                         "score": round(word_score, 3), "lots": lots,
                         "match_type": "word"})
            continue

        # 3. Containment match — handles partial overlaps
        contain_slug, contain_score = None, 0.0
        for slug, norm in tb_norm.items():
            if ap in norm:
                s = len(ap) / len(norm)
                if s > contain_score:
                    contain_score, contain_slug = s, slug
            elif norm in ap:
                s = len(norm) / len(ap)
                if s > contain_score:
                    contain_score, contain_slug = s, slug

        if contain_score >= 0.6:
            rows.append({"auction_producer": ap, "tb_slug": contain_slug,
                         "score": round(contain_score, 3), "lots": lots,
                         "match_type": "contain"})
            continue

        # 3. Fuzzy match
        best_slug, best_score = None, 0.0
        for slug, norm in tb_norm.items():
            s = similarity(ap, norm)
            if s > best_score:
                best_score, best_slug = s, slug

        if best_score >= threshold:
            rows.append({"auction_producer": ap, "tb_slug": best_slug,
                         "score": round(best_score, 3), "lots": lots,
                         "match_type": "fuzzy"})

    result = pd.DataFrame(rows).sort_values("lots", ascending=False)
    result.to_csv(MATCHES_OUT, index=False)
    print(f"  Matched {len(result):,} producers ({result['lots'].sum():,} lots)")
    return result


# ---------------------------------------------------------------------------
# Step 3 — Scrape wine pages
# ---------------------------------------------------------------------------

DRINK_RE = re.compile(
    r"""
    (?:from\s+)?(\d{4})\s*[-–to]+\s*(\d{4})   # 2018 - 2035 or 2018 to 2035
    | from\s+(\d{4})                            # from 2030
    | now\s*[-–to]+\s*(\d{4})                  # now - 2035
    | ^\s*(now)\s*$                             # just "Now"
    """,
    re.IGNORECASE | re.VERBOSE,
)


def parse_drink_window(text) -> tuple[int | None, int | None]:
    if not text or pd.isna(text):
        return None, None
    text = str(text).strip()
    m = DRINK_RE.search(text)
    if not m:
        return None, None
    g = m.groups()
    if g[0] and g[1]:          # YYYY-YYYY
        return int(g[0]), int(g[1])
    elif g[2]:                 # from YYYY
        return int(g[2]), None
    elif g[3]:                 # now - YYYY
        return 2026, int(g[3])
    elif g[4]:                 # Now
        return 2026, 2026
    return None, None


def scrape_wine_page(url: str, session: requests.Session) -> dict | None:
    """Fetch a single wine page and return its maturity data dict, or None."""
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "lxml")
        stat_ul = soup.find(id="status-statistics")
        if not stat_ul:
            return None

        result = {"url": url}
        for li in stat_ul.find_all("li"):
            h4 = li.find("h4")
            if not h4:
                continue
            title = h4.get_text(strip=True)
            val_div = li.find("div")
            value = val_div.get_text(" ", strip=True) if val_div else ""
            if title == "When to drink":
                result["when_to_drink"] = value
                df_val, du_val = parse_drink_window(value)
                result["drink_from"] = df_val
                result["drink_until"] = du_val
            elif title == "Decanting time":
                result["decanting_time"] = value
            elif title == "Country ranking":
                result["country_ranking"] = value
            elif title == "Producer ranking":
                result["producer_ranking"] = value
            elif title == "Food Pairing":
                result["food_pairing"] = value

        return result if "when_to_drink" in result else None

    except Exception:
        return None


def step3_scrape(
    sitemap_df: pd.DataFrame,
    matches: pd.DataFrame,
    workers: int = 8,
    max_pages: int | None = None,
    delay: float = 0.1,
    force: bool = False,
) -> pd.DataFrame:
    """
    Scrape wine pages for matched producers.
    Skips URLs already in existing Xin Ning data and SCRAPE_OUT if present.
    """
    # Already-scraped URLs (Xin Ning)
    existing_urls: set[str] = set()
    if EXISTING_TB.exists():
        xn = pd.read_excel(EXISTING_TB)
        existing_urls = set(xn["year_url"].dropna().tolist())
        print(f"  Xin Ning baseline: {len(existing_urls):,} URLs already scraped")

    # Previously scraped in this run
    if SCRAPE_OUT.exists() and not force:
        prev = pd.read_parquet(SCRAPE_OUT)
        existing_urls.update(prev["url"].tolist())
        print(f"  Previous run cache: {len(prev):,} rows — will skip already-scraped URLs")
    else:
        prev = pd.DataFrame()

    # Build target URL list
    matched_slugs = set(matches["tb_slug"].tolist())
    target_df = sitemap_df[sitemap_df["producer_slug"].isin(matched_slugs)].copy()
    target_urls = [u for u in target_df["url"].tolist() if u not in existing_urls]

    if max_pages:
        target_urls = target_urls[:max_pages]

    print(f"  Target URLs: {len(target_urls):,} (from {len(matched_slugs):,} matched producers)")

    if not target_urls:
        print("  Nothing new to scrape.")
        return prev

    session = make_session()
    results: list[dict] = []
    done = 0
    errors = 0

    print(f"  Scraping with {workers} workers ...")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(scrape_wine_page, url, session): url for url in target_urls}
        for future in as_completed(futures):
            row = future.result()
            if row:
                results.append(row)
            else:
                errors += 1
            done += 1
            if done % 500 == 0 or done == len(target_urls):
                print(f"    {done:>6}/{len(target_urls):,}  scraped={len(results):,}  no-data={errors:,}")
            time.sleep(delay / workers)  # gentle rate limit

    new_df = pd.DataFrame(results)
    if not new_df.empty:
        # Attach producer_slug + wine_slug + vintage from sitemap
        url_meta = target_df.set_index("url")[["producer_slug", "wine_slug", "vintage"]]
        new_df = new_df.join(url_meta, on="url", how="left")

    # Merge with previous run cache
    combined = pd.concat([prev, new_df], ignore_index=True).drop_duplicates("url")
    combined.to_parquet(SCRAPE_OUT, index=False)
    print(f"  Saved {len(combined):,} rows → {SCRAPE_OUT}")
    return combined


# ---------------------------------------------------------------------------
# Step 4 — Combine with Xin Ning data and save xlsx
# ---------------------------------------------------------------------------

def step4_combine(scraped_df: pd.DataFrame) -> pd.DataFrame:
    """Merge new scraped data with Xin Ning baseline and save combined xlsx."""
    # Load Xin Ning
    xn = pd.read_excel(EXISTING_TB)
    # "url" is producer URL, "year_url" is wine page URL — drop the producer URL first
    xn = xn.drop(columns=["url"], errors="ignore").rename(
        columns={"year_url": "url", "When to drink": "when_to_drink"}
    )

    # Parse drink window in Xin Ning data
    parsed = xn["when_to_drink"].apply(parse_drink_window)
    xn["drink_from"]  = [p[0] for p in parsed]
    xn["drink_until"] = [p[1] for p in parsed]

    # Attach producer_slug from URL
    xn["producer_slug"] = xn["url"].str.extract(r"tastingbook\.com/wine/([^/]+)/")
    xn["vintage"]       = xn["url"].str.extract(r"_(\d{4})$").astype("Int64")

    # Align columns
    keep_cols = ["url", "producer_slug", "wine_slug", "vintage",
                 "when_to_drink", "drink_from", "drink_until",
                 "decanting_time", "country_ranking", "producer_ranking", "food_pairing"]
    for c in keep_cols:
        if c not in xn.columns:
            xn[c] = None
        if c not in scraped_df.columns:
            scraped_df[c] = None

    combined = pd.concat([xn[keep_cols], scraped_df[keep_cols]], ignore_index=True)
    combined = combined.drop_duplicates("url")

    combined.to_excel(COMBINED_OUT, index=False)
    print(f"  Combined: {len(combined):,} rows → {COMBINED_OUT}")
    print(f"    Xin Ning baseline : {len(xn):,}")
    print(f"    New scrape        : {len(scraped_df):,}")
    print(f"    After dedup       : {len(combined):,}")
    return combined


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Tastingbook sitemap scraper")
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4],
                        help="Run only a single step (1=sitemap, 2=match, 3=scrape, 4=combine)")
    parser.add_argument("--workers", type=int, default=8,
                        help="Parallel HTTP workers for scraping (default: 8)")
    parser.add_argument("--max-pages", type=int, default=None,
                        help="Limit number of pages to scrape (for testing)")
    parser.add_argument("--min-lots", type=int, default=100,
                        help="Min unmatched lots to include a producer (default: 100)")
    parser.add_argument("--threshold", type=float, default=0.70,
                        help="Fuzzy match score threshold 0-1 (default: 0.70)")
    parser.add_argument("--force", action="store_true",
                        help="Re-download/re-compute even if cache exists")
    parser.add_argument("--dry-run", action="store_true",
                        help="Steps 1+2 only: show what would be scraped, no HTTP requests to wine pages")
    args = parser.parse_args()

    print("=" * 60)
    print("Step 05: Tastingbook sitemap scraper")
    print("=" * 60)

    # --- Step 1 ---
    if args.step in (None, 1, 2, 3, 4):
        print("\n[1] Downloading sitemaps ...")
        sitemap_df = step1_download_sitemaps(force=args.force)

    if args.step == 1:
        return

    # --- Step 2 ---
    if args.step in (None, 2, 3, 4):
        print(f"\n[2] Matching producers (min_lots={args.min_lots}, threshold={args.threshold}) ...")
        matches = step2_match_producers(
            sitemap_df,
            min_lots=args.min_lots,
            threshold=args.threshold,
            force=args.force,
        )
        print(f"\n  Top 20 matched producers:")
        print(f"  {'Auction producer':<40} {'TB slug':<40} {'Score':>6} {'Lots':>8}")
        print("  " + "-" * 100)
        for _, row in matches.head(20).iterrows():
            print(f"  {row['auction_producer']:<40} {row['tb_slug']:<40} {row['score']:>6.3f} {row['lots']:>8,}")

    if args.step == 2 or args.dry_run:
        matched_slugs = set(matches["tb_slug"].tolist())
        target_count = sitemap_df[sitemap_df["producer_slug"].isin(matched_slugs)]["url"].nunique()
        print(f"\n  Would scrape {target_count:,} wine pages for {len(matched_slugs):,} producers")
        print("  (dry-run: no scraping performed)")
        return

    if args.step == 3 or args.step is None:
        print(f"\n[3] Scraping wine pages (workers={args.workers}) ...")
        scraped_df = step3_scrape(
            sitemap_df,
            matches,
            workers=args.workers,
            max_pages=args.max_pages,
            force=args.force,
        )

    if args.step == 3:
        return

    # --- Step 4 ---
    if args.step in (None, 4):
        if args.step == 4:
            # Load from cache
            scraped_df = pd.read_parquet(SCRAPE_OUT) if SCRAPE_OUT.exists() else pd.DataFrame()
        print(f"\n[4] Combining with Xin Ning baseline ...")
        combined = step4_combine(scraped_df)
        print(f"\nDone. Run 04_merge_maturity.py pointing at {COMBINED_OUT} to update the parquet.")


if __name__ == "__main__":
    main()
