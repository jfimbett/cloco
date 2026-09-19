#!/usr/bin/env python3
"""
Paper intake — inventory the materials of an old / abandoned working paper so
the /revive skill can reconstruct where the project stood.

Usage:
    python3 .claude/scripts/paper_intake.py PATH [PATH ...] --slug SLUG
        [--out quality_reports/revival] [--max-chars 400000] [--json]

PATH may be a PDF, a .tex/.docx/.md/.txt file, a .bib, a data or code file,
or a whole directory (walked recursively; .git, build artefacts and hidden
folders are skipped).

Writes  <out>/<slug>/manifest.json     every file: role, size, mtime, hash
        <out>/<slug>/inventory.md      human-readable reconstruction
        <out>/<slug>/extracted/*.txt   text of manuscripts / notes (gitignored)
and prints a compact summary (or the JSON manifest with --json).

Stdlib only. PDF text uses `pdftotext` (poppler) if on PATH, else the `pypdf`
package if installed, else the PDF is listed but not read (the inventory says
so). .docx is read through zipfile. Nothing is copied or modified: data files
are described in place and left where they are — register them with
/data-registry, never move them into the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])

SKIP_DIRS = {".git", ".svn", "__pycache__", "node_modules", ".Rproj.user", ".ipynb_checkpoints", ".venv", "venv", ".claude"}
SKIP_SUFFIXES = {".aux", ".log", ".synctex.gz", ".fls", ".fdb_latexmk", ".bbl", ".blg", ".out", ".toc",
                 ".lof", ".lot", ".nav", ".snm", ".vrb", ".bcf", ".run.xml", ".xdv", ".pyc", ".pyo", ".DS_Store"}

ROLE_BY_SUFFIX = {
    ".tex": "manuscript", ".ltx": "manuscript", ".docx": "manuscript", ".rtf": "manuscript", ".odt": "manuscript",
    ".md": "notes", ".txt": "notes", ".org": "notes", ".rmd": "notes", ".qmd": "notes",
    ".bib": "bibliography",
    ".r": "code", ".py": "code", ".do": "code", ".ado": "code", ".jl": "code", ".m": "code", ".sas": "code",
    ".sql": "code", ".sh": "code", ".ipynb": "code", ".rmd_code": "code", ".java": "code", ".cpp": "code", ".c": "code",
    ".csv": "data", ".tsv": "data", ".parquet": "data", ".dta": "data", ".rds": "data", ".rdata": "data", ".rda": "data",
    ".xlsx": "data", ".xls": "data", ".sas7bdat": "data", ".feather": "data", ".sav": "data", ".zip": "data",
    ".gz": "data", ".db": "data", ".sqlite": "data", ".h5": "data", ".pkl": "data", ".json": "data",
    ".png": "figure", ".jpg": "figure", ".jpeg": "figure", ".eps": "figure", ".svg": "figure", ".tikz": "figure",
    ".pptx": "slides", ".key": "slides",
}
CODE_LANG = {".r": "R", ".py": "Python", ".do": "Stata", ".ado": "Stata", ".jl": "Julia", ".m": "MATLAB",
             ".sas": "SAS", ".sql": "SQL", ".sh": "shell", ".ipynb": "Jupyter"}

BIG_FILE_MB = 20

DATA_SOURCES = [
    "CRSP", "Compustat", "Compustat Global", "IBES", "I/B/E/S", "TAQ", "Execucomp", "BoardEx", "Dealscan", "DealScan",
    "TRACE", "OptionMetrics", "RavenPack", "FactSet", "Thomson Reuters", "Thomson", "SDC", "Refinitiv", "Datastream",
    "Worldscope", "Bloomberg", "Capital IQ", "Audit Analytics", "ISS", "RiskMetrics", "Mergent", "FISD", "Markit",
    "13F", "EDGAR", "SEC", "Call Reports", "FR Y-9C", "HMDA", "FFIEC", "FDIC", "FRED", "BLS", "BEA", "Census",
    "CPS", "ACS", "PSID", "SCF", "NLSY", "HRS", "LEHD", "QCEW", "IPUMS", "IRS", "SOI", "Zillow", "CoreLogic",
    "Nielsen", "Kilts", "Orbis", "Amadeus", "Zephyr", "BvD", "Bureau van Dijk", "Preqin", "PitchBook", "Crunchbase",
    "VentureXpert", "Kickstarter", "Eurostat", "ECB", "AnaCredit", "SIRENE", "FICUS", "FARE", "DADS", "INSEE",
    "Banque de France", "Bundesbank", "Bank of England", "BIS", "IMF", "World Bank", "OECD", "Penn World",
    "Fama-French", "Kenneth French", "WRDS", "Morningstar", "Lipper", "EDGAR Full-Text", "Google Trends", "Twitter",
    "LinkedIn", "Burning Glass", "Lightcast", "Glassdoor", "Yelp", "Mintel", "Comscore", "Homescan", "MSCI",
    "Sustainalytics", "Trucost", "CDP", "Bloomberg ESG", "Asset4", "KLD",
]
METHODS = {
    "difference-in-differences": r"difference[- ]in[- ]differences|\bDiD\b|\bDD\b estimat|diff[- ]in[- ]diff",
    "staggered adoption": r"staggered|cohort[- ]specific|Callaway|Sun and Abraham|Goodman-Bacon|stacked (?:DiD|regression)",
    "event study": r"event[- ]stud",
    "instrumental variables": r"instrumental variable|\bIV\b|two[- ]stage least squares|\b2SLS\b|first[- ]stage",
    "regression discontinuity": r"regression discontinuity|\bRDD?\b|running variable|bandwidth",
    "synthetic control": r"synthetic control",
    "fixed effects panel": r"fixed effects|within estimator|two[- ]way fixed",
    "matching / propensity": r"propensity score|matching estimator|nearest[- ]neighbou?r",
    "GMM / structural estimation": r"\bGMM\b|simulated method of moments|\bSMM\b|indirect inference|maximum likelihood|calibrat",
    "theory / model": r"\bproposition\b|\blemma\b|\bproof\b|equilibrium|first[- ]order condition",
    "machine learning": r"random forest|LASSO|neural net|gradient boosting|double machine learning",
    "text analysis": r"textual analysis|text analysis|topic model|LDA|word embedding|sentiment",
}
STALL_HINTS = {
    "referee / rejection": r"reject|referee report|revise and resubmit|R&R|desk[- ]reject",
    "data access": r"data (?:access|agreement|licen[cs]e) (?:expired|ended|lapsed)|lost access|no longer have access",
    "identification concern": r"pre[- ]trend|parallel trends? (?:fail|violat)|weak instrument|endogen",
    "explicit TODO": r"\bTODO\b|\bTBD\b|\bFIXME\b|XXX|\\todo\{",
    "co-author": r"co[- ]?author",
}
DATE_RANGE_RE = re.compile(r"\b(19[5-9]\d|20[0-4]\d)\s*(?:–|—|-|to|through|until|and)\s*(19[5-9]\d|20[0-4]\d)\b")
YEAR_RE = re.compile(r"\b(19[5-9]\d|20[0-4]\d)\b")
HARDCODED_PATH_RE = re.compile(r"([A-Za-z]:\\\\|/Users/|/home/|Dropbox|OneDrive|Google Drive|C:/Users)")


# --------------------------------------------------------------------------- #
# Walking + classification
# --------------------------------------------------------------------------- #
def iter_files(paths: list[Path]):
    for p in paths:
        p = p.expanduser()
        if p.is_file():
            yield p
        elif p.is_dir():
            for root, dirs, files in os.walk(p):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
                for f in sorted(files):
                    fp = Path(root) / f
                    if f.startswith(".") or fp.suffix.lower() in SKIP_SUFFIXES or fp.name in SKIP_SUFFIXES:
                        continue
                    yield fp


def classify(path: Path) -> str:
    suf = path.suffix.lower()
    name = path.name.lower()
    parts = {q.lower() for q in path.parts}
    if suf == ".pdf":
        if parts & {"figures", "figs", "fig", "plots", "graphs"} or re.match(r"^(fig|figure|plot|graph)", name):
            return "figure"
        if parts & {"slides", "talk", "talks", "presentation", "beamer"} or re.search(r"slides|talk|beamer|present", name):
            return "slides"
        if parts & {"references", "refs", "literature", "papers", "lit", "reading"}:
            return "reference-pdf"
        return "manuscript-pdf"
    if suf == ".tex" and (parts & {"tables", "tabs"} or re.match(r"^(tab|table)", name)):
        return "table"
    if suf == ".tex" and (parts & {"figures", "figs"}):
        return "figure"
    if suf in (".md", ".txt", ".org") and re.search(r"readme|notes?|todo|log|journal|archive|diary|memo", name):
        return "notes"
    if suf == ".json" and name in ("registry.json", "package.json"):
        return "other"
    if suf == ".rmd" or suf == ".qmd":
        return "code"
    return ROLE_BY_SUFFIX.get(suf, "other")


def sha1_head(path: Path, n: int = 1 << 20) -> str:
    h = hashlib.sha1()
    try:
        with path.open("rb") as fh:
            h.update(fh.read(n))
    except OSError:
        return ""
    return h.hexdigest()[:12]


def pretty_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve()))
    except ValueError:
        pass
    home = str(Path.home())
    s = str(path.resolve())
    return "~" + s[len(home):] if s.startswith(home) else s


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f}{unit}" if unit == "B" else f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}GB"


# --------------------------------------------------------------------------- #
# Text extraction
# --------------------------------------------------------------------------- #
def pdf_text(path: Path, max_chars: int) -> tuple[str, str, dict]:
    """Return (text, method, meta). method in {pdftotext, pypdf, none}."""
    meta: dict = {}
    if shutil.which("pdftotext"):
        try:
            out = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
                                 capture_output=True, text=True, timeout=120)
            if out.returncode == 0 and out.stdout.strip():
                if shutil.which("pdfinfo"):
                    info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, timeout=30).stdout
                    for line in info.splitlines():
                        if ":" in line:
                            k, v = line.split(":", 1)
                            if k.strip() in ("Title", "Author", "Pages", "CreationDate", "ModDate", "Page size"):
                                meta[k.strip().lower().replace(" ", "_")] = v.strip()
                return out.stdout[:max_chars], "pdftotext", meta
        except (subprocess.SubprocessError, OSError):
            pass
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        chunks: list[str] = []
        total = 0
        for page in reader.pages:
            t = page.extract_text() or ""
            chunks.append(t)
            total += len(t)
            if total > max_chars:
                break
        meta["pages"] = str(len(reader.pages))
        try:
            box = reader.pages[0].mediabox
            meta["page_size"] = f"{float(box.width):.0f}x{float(box.height):.0f} pts"
            meta["landscape"] = bool(float(box.width) > float(box.height))
        except Exception:
            pass
        md = reader.metadata or {}
        for k in ("title", "author", "creation_date", "modification_date"):
            try:
                v = getattr(md, k, None)
                if v:
                    meta[k] = str(v)
            except Exception:
                pass
        return "\n".join(chunks)[:max_chars], "pypdf", meta
    except Exception:
        return "", "none", meta


def docx_text(path: Path, max_chars: int) -> str:
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    except (zipfile.BadZipFile, KeyError, OSError):
        return ""
    xml = re.sub(r"</w:p>", "\n", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    return re.sub(r"\n{3,}", "\n\n", text)[:max_chars]


def read_text(path: Path, max_chars: int) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError:
        return ""


# --------------------------------------------------------------------------- #
# Analysers
# --------------------------------------------------------------------------- #
def strip_tex(src: str) -> str:
    src = re.sub(r"(?<!\\)%.*", "", src)
    src = re.sub(r"\\(?:cite[tp]?|ref|label|eqref|autoref|input|include|includegraphics)\*?(?:\[[^\]]*\])?\{[^}]*\}", " ", src)
    src = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", src)
    return re.sub(r"[{}$]", " ", src)


def tex_facts(src: str) -> dict:
    f: dict = {}
    m = re.search(r"\\title\*?(?:\[[^\]]*\])?\{(.+?)\}\s*(?:\n|\\)", src, re.S)
    if m:
        f["title"] = re.sub(r"\s+", " ", strip_tex(m.group(1))).strip()
    m = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", src, re.S)
    if m:
        f["abstract"] = re.sub(r"\s+", " ", strip_tex(m.group(1))).strip()
    m = re.search(r"\\(?:jel|JEL)[a-zA-Z]*\{([^}]*)\}|JEL(?: [Cc]odes?| [Cc]lassification)?[:\s]+([A-Z]\d\d(?:[,;\s]+[A-Z]\d\d)*)", src)
    if m:
        f["jel"] = (m.group(1) or m.group(2) or "").strip()
    m = re.search(r"\\keywords?\{([^}]*)\}|Keywords?[:\s]+(.+)", src)
    if m:
        f["keywords"] = re.sub(r"\s+", " ", strip_tex(m.group(1) or m.group(2) or "")).strip()[:200]
    f["is_main"] = bool(re.search(r"\\documentclass", src) and re.search(r"\\begin\{document\}", src))
    f["is_beamer"] = bool(re.search(r"\\documentclass(?:\[[^\]]*\])?\{beamer\}", src))
    f["inputs"] = re.findall(r"\\(?:input|include|subfile)\{([^}]+)\}", src)
    f["n_tables"] = len(re.findall(r"\\begin\{table\*?\}", src))
    f["n_figures"] = len(re.findall(r"\\begin\{figure\*?\}", src))
    f["n_cites"] = len(re.findall(r"\\(?:cite|citet|citep|citealt|citealp|textcite|parencite|autocite)\*?\b", src))
    f["n_todos"] = len(re.findall(r"\\todo\{|%\s*TODO|\bTODO\b|\bTBD\b|\bXXX\b", src))
    f["sections"] = [re.sub(r"\s+", " ", strip_tex(s)).strip() for s in re.findall(r"\\section\*?\{([^}]+)\}", src)][:20]
    f["bibliography"] = re.findall(r"\\(?:bibliography|addbibresource)\{([^}]+)\}", src)
    return f


def bib_facts(src: str) -> dict:
    entries = re.findall(r"@(\w+)\s*\{", src)
    years = [int(y) for y in re.findall(r"\byear\s*=\s*[{\"]?\s*(\d{4})", src, re.I)]
    return {
        "n_entries": len([e for e in entries if e.lower() not in ("comment", "preamble", "string")]),
        "newest_year": max(years) if years else None,
        "year_hist": dict(sorted(Counter(y for y in years if y >= 1990).items())),
    }


def code_facts(src: str, suffix: str) -> dict:
    f: dict = {"lines": src.count("\n") + 1}
    f["hardcoded_paths"] = len(HARDCODED_PATH_RE.findall(src))
    if suffix == ".r":
        f["packages"] = sorted(set(re.findall(r"(?:library|require)\(\s*[\"']?([A-Za-z0-9.]+)", src)))[:25]
        f["reads"] = len(re.findall(r"read\.\w+\(|read_\w+\(|fread\(|readRDS\(|load\(", src))
    elif suffix == ".py":
        f["packages"] = sorted(set(re.findall(r"^\s*(?:import|from)\s+([A-Za-z0-9_]+)", src, re.M)))[:25]
        f["reads"] = len(re.findall(r"read_\w+\(|\.load\(|open\(", src))
    elif suffix == ".do":
        f["packages"] = sorted(set(re.findall(r"^\s*(?:ssc install|net install)\s+(\w+)", src, re.M)))[:25]
        f["reads"] = len(re.findall(r"^\s*(?:use|import\s+\w+|insheet|merge)\b", src, re.M))
    f["seed"] = bool(re.search(r"set\.seed\(|np\.random\.seed\(|random\.seed\(|set seed|Random\.seed!", src))
    return f


def text_facts(text: str) -> dict:
    f: dict = {}
    low = text.lower()
    m = re.search(r"\babstract\b\s*[:.]?\s*(.{200,2500}?)(?:\n\s*\n|\bkeywords?\b|\bjel\b|\b1\s+introduction\b|\bintroduction\b)", text, re.S | re.I)
    if m:
        f["abstract"] = re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(r"JEL(?: [Cc]odes?| [Cc]lassification)?[:\s]+([A-Z]\d\d(?:\s*[,;]\s*[A-Z]\d\d)*)", text)
    if m:
        f["jel"] = m.group(1)
    ranges = Counter((a, b) for a, b in DATE_RANGE_RE.findall(text) if int(a) < int(b) and int(b) - int(a) <= 80)
    if ranges:
        (a, b), n = ranges.most_common(1)[0]
        f["sample_period_guess"] = f"{a}–{b}"
        f["sample_period_mentions"] = n
    years = [int(y) for y in YEAR_RE.findall(text)]
    if years:
        f["latest_year_mentioned"] = max(years)
    f["data_sources"] = sorted({s for s in DATA_SOURCES if re.search(r"(?<![A-Za-z])" + re.escape(s.lower()) + r"(?![a-z])", low)})
    f["methods"] = [k for k, pat in METHODS.items() if re.search(pat, text, re.I)]
    f["stall_hints"] = {k: len(re.findall(pat, text, re.I)) for k, pat in STALL_HINTS.items()}
    f["stall_hints"] = {k: v for k, v in f["stall_hints"].items() if v}
    f["words"] = len(re.findall(r"\w+", text))
    return f


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def build_manifest(paths: list[Path], out_dir: Path, max_chars: int) -> dict:
    extracted_dir = out_dir / "extracted"
    extracted_dir.mkdir(parents=True, exist_ok=True)
    files: list[dict] = []
    corpus: list[tuple[str, str, str]] = []  # (role, stem, text)
    notes_hints: Counter = Counter()
    tex_main: dict | None = None
    tex_all: list[dict] = []
    bibs: list[dict] = []
    codes: list[dict] = []
    pdf_methods: Counter = Counter()
    seen_hashes: dict[str, str] = {}

    for fp in iter_files(paths):
        try:
            st = fp.stat()
        except OSError:
            continue
        role = classify(fp)
        rec: dict = {
            "path": pretty_path(fp), "name": fp.name, "role": role, "suffix": fp.suffix.lower(),
            "size": st.st_size, "size_h": human(st.st_size),
            "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d"),
        }
        h = sha1_head(fp)
        rec["hash"] = h
        if h and h in seen_hashes:
            rec["duplicate_of"] = seen_hashes[h]
        elif h:
            seen_hashes[h] = rec["path"]
        if st.st_size >= BIG_FILE_MB * 1024 * 1024:
            rec["big_file"] = True
        try:
            fp.resolve().relative_to(PROJECT_ROOT.resolve())
            rec["inside_repo"] = True
            if role == "data" and not any(part in ("data",) for part in fp.parts):
                rec["data_in_repo_warning"] = True
        except ValueError:
            rec["inside_repo"] = False

        text = ""
        if role in ("manuscript-pdf", "slides", "reference-pdf") and fp.suffix.lower() == ".pdf":
            text, method, meta = pdf_text(fp, max_chars)
            pdf_methods[method] += 1
            rec["extract_method"] = method
            if meta:
                rec["pdf_meta"] = meta
                if meta.get("landscape") and role == "manuscript-pdf":
                    rec["role"] = role = "slides"
        elif fp.suffix.lower() == ".docx":
            text = docx_text(fp, max_chars)
            rec["extract_method"] = "docx"
        elif role in ("manuscript", "notes", "table") or fp.suffix.lower() in (".tex", ".md", ".txt", ".org"):
            text = read_text(fp, max_chars)
            if fp.suffix.lower() in (".tex", ".ltx"):
                tf = tex_facts(text)
                rec["tex"] = tf
                tex_all.append({**tf, "path": rec["path"]})
                if tf.get("is_main") and not tf.get("is_beamer") and (tex_main is None or len(text) > tex_main.get("_len", 0)):
                    tex_main = {**tf, "path": rec["path"], "_len": len(text)}
                if tf.get("is_beamer"):
                    rec["role"] = role = "slides"
                text = strip_tex(text)
        elif role == "bibliography":
            src = read_text(fp, max_chars)
            bf = bib_facts(src)
            rec["bib"] = bf
            bibs.append({**bf, "path": rec["path"]})
        elif role == "code":
            src = read_text(fp, max_chars)
            cf = code_facts(src, fp.suffix.lower())
            cf["language"] = CODE_LANG.get(fp.suffix.lower(), fp.suffix.lstrip(".").upper() or "unknown")
            rec["code"] = cf
            codes.append({**cf, "path": rec["path"]})

        if text.strip() and role in ("manuscript-pdf", "manuscript", "notes", "slides"):
            rec["text_facts"] = text_facts(text)
            out_txt = extracted_dir / (re.sub(r"[^A-Za-z0-9._-]+", "_", fp.name)[:80] + ".txt")
            out_txt.write_text(text, encoding="utf-8")
            rec["extracted_text"] = pretty_path(out_txt)
            rec["_abs_txt"] = str(out_txt)
            if role in ("manuscript-pdf", "manuscript"):
                corpus.append((role, fp.stem, text))
            else:
                notes_hints.update(rec["text_facts"].get("stall_hints", {}))
        files.append(rec)

    main_stem = Path(tex_main["path"]).stem if tex_main else None
    corpus_text = "\n\n".join(t for role, stem, t in corpus if not (role == "manuscript-pdf" and stem == main_stem))
    overall = text_facts(corpus_text) if corpus_text.strip() else {}
    if notes_hints:
        merged = Counter(overall.get("stall_hints", {}))
        merged.update(notes_hints)
        overall["stall_hints"] = dict(merged)
    title = (tex_main or {}).get("title")
    if not title:
        for r in files:
            t = (r.get("pdf_meta") or {}).get("title")
            if t and len(t) > 8 and not t.lower().endswith((".dvi", ".tex", ".pdf")):
                title = t
                break
    if not title:
        for r in files:
            if r["role"] == "manuscript-pdf" and r.get("_abs_txt"):
                picked: list[str] = []
                for line in Path(r["_abs_txt"]).read_text(encoding="utf-8", errors="replace").splitlines()[:15]:
                    line = line.strip()
                    ok = 10 <= len(line) <= 160 and not re.search(r"\d{4}|@|http|draft|preliminary|university|abstract", line, re.I)
                    if ok:
                        picked.append(line)
                        if len(picked) == 3 or line.endswith((".", "?", "!")):
                            break
                    elif picked:
                        break
                if picked:
                    title = " ".join(picked)
            if title:
                break
    for r in files:
        r.pop("_abs_txt", None)
    abstract = (tex_main or {}).get("abstract") or overall.get("abstract")

    roles = Counter(r["role"] for r in files)
    newest = max((r["mtime"] for r in files), default=None)
    oldest = min((r["mtime"] for r in files), default=None)
    data_files = [r for r in files if r["role"] == "data"]
    bib_newest = max((b["newest_year"] for b in bibs if b.get("newest_year")), default=None)
    langs = Counter(c["language"] for c in codes)

    summary = {
        "title_guess": title,
        "abstract": abstract,
        "jel": (tex_main or {}).get("jel") or overall.get("jel"),
        "keywords": (tex_main or {}).get("keywords"),
        "main_tex": (tex_main or {}).get("path"),
        "sections": (tex_main or {}).get("sections", []),
        "n_files": len(files),
        "roles": dict(roles),
        "files_modified": {"oldest": oldest, "newest": newest},
        "literature_horizon_year": bib_newest,
        "latest_year_in_text": overall.get("latest_year_mentioned"),
        "sample_period_guess": overall.get("sample_period_guess"),
        "data_sources_mentioned": overall.get("data_sources", []),
        "methods_detected": overall.get("methods", []),
        "stall_hints": overall.get("stall_hints", {}),
        "manuscript_words": overall.get("words"),
        "code_languages": dict(langs),
        "code_hardcoded_paths": sum(c.get("hardcoded_paths", 0) for c in codes),
        "code_files_without_seed": sum(1 for c in codes if not c.get("seed")),
        "data_total_bytes": sum(r["size"] for r in data_files),
        "data_total_h": human(sum(r["size"] for r in data_files)),
        "big_files": [r["path"] for r in files if r.get("big_file")],
        "data_in_repo": [r["path"] for r in files if r.get("data_in_repo_warning")],
        "duplicates": [(r["path"], r["duplicate_of"]) for r in files if r.get("duplicate_of")],
        "pdf_extraction": dict(pdf_methods),
        "n_bib_entries": sum(b.get("n_entries", 0) for b in bibs),
        "tables_in_tex": sum(t.get("n_tables", 0) for t in tex_all),
        "figures_in_tex": sum(t.get("n_figures", 0) for t in tex_all),
        "todos_in_tex": sum(t.get("n_todos", 0) for t in tex_all),
    }
    return {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "inputs": [pretty_path(p.expanduser()) for p in paths],
        "summary": summary,
        "files": files,
    }


def render_inventory(m: dict, slug: str) -> str:
    s = m["summary"]
    L: list[str] = [f"# Paper Intake — {s.get('title_guess') or slug}", "",
                    f"**Generated:** {m['generated']}  ", f"**Inputs:** {', '.join('`' + i + '`' for i in m['inputs'])}  ",
                    f"**Files:** {s['n_files']} — " + ", ".join(f"{k} {v}" for k, v in sorted(s["roles"].items())), ""]
    L += ["## What the materials say", ""]
    L.append("- **Title (guess):** " + (s.get("title_guess") or "UNKNOWN — no \\title{} or PDF title found"))
    if s.get("jel"):
        L.append(f"- **JEL:** {s['jel']}")
    if s.get("keywords"):
        L.append(f"- **Keywords:** {s['keywords']}")
    if s.get("main_tex"):
        L.append(f"- **Main .tex:** `{s['main_tex']}` — sections: {', '.join(s.get('sections') or []) or 'none found'}")
    L.append(f"- **Last file modified:** {s['files_modified']['newest'] or '—'} (oldest {s['files_modified']['oldest'] or '—'})")
    L.append(f"- **Literature horizon:** newest .bib year {s.get('literature_horizon_year') or '—'}; latest year mentioned in text {s.get('latest_year_in_text') or '—'}")
    L.append(f"- **Sample period (guess):** {s.get('sample_period_guess') or 'not detected'}")
    L.append(f"- **Data sources mentioned:** {', '.join(s.get('data_sources_mentioned') or []) or 'none recognised'}")
    L.append(f"- **Methods detected:** {', '.join(s.get('methods_detected') or []) or 'none recognised'}")
    L.append(f"- **Manuscript length:** {s.get('manuscript_words') or 0:,} words · {s['tables_in_tex']} tables · {s['figures_in_tex']} figures (from .tex) · {s['n_bib_entries']} bib entries")
    if s.get("stall_hints"):
        L.append("- **Stall hints in text:** " + ", ".join(f"{k} ({v})" for k, v in s["stall_hints"].items()))
    if s.get("todos_in_tex"):
        L.append(f"- **Open TODOs in .tex:** {s['todos_in_tex']}")
    L.append("")
    if s.get("abstract"):
        L += ["### Abstract (as found)", "", "> " + s["abstract"][:2000], ""]

    L += ["## Code", ""]
    if s.get("code_languages"):
        L.append(f"- Languages: {', '.join(f'{k} ({v})' for k, v in s['code_languages'].items())}")
        L.append(f"- Hard-coded paths found: {s['code_hardcoded_paths']} → must go through `code/utils/data_paths.*`")
        L.append(f"- Scripts without a seed call: {s['code_files_without_seed']}")
    else:
        L.append("- No code files found. Results are not reproducible from these materials alone.")
    L.append("")

    L += ["## Data", ""]
    data_files = [f for f in m["files"] if f["role"] == "data"]
    if data_files:
        L.append(f"- {len(data_files)} data file(s), {s['data_total_h']} total. **Do not copy into the repo** — register in place: `/data-registry add NAME --path <template> --stage external --source '<provider, pulled YYYY>'`.")
        L.append("")
        L += ["| File | Size | Modified | Flags |", "|------|------|----------|-------|"]
        for f in data_files[:40]:
            flags = " ".join(x for x in ("≥20MB" if f.get("big_file") else "", "IN-REPO" if f.get("data_in_repo_warning") else "", "dup" if f.get("duplicate_of") else "") if x)
            L.append(f"| `{f['path']}` | {f['size_h']} | {f['mtime']} | {flags} |")
        if len(data_files) > 40:
            L.append(f"| … {len(data_files) - 40} more | | | |")
    else:
        L.append("- No data files among the inputs. Data must be re-obtained: check the registry, WRDS, or the provider named in the text.")
    L.append("")

    L += ["## File manifest", "", "| Role | File | Size | Modified | Notes |", "|------|------|------|----------|-------|"]
    for f in sorted(m["files"], key=lambda r: (r["role"], r["path"])):
        if f["role"] == "data":
            continue
        notes = []
        if f.get("extract_method") == "none":
            notes.append("PDF not readable (install poppler or `pip install pypdf`)")
        if f.get("tex", {}).get("is_main"):
            notes.append("main document")
        if f.get("bib"):
            notes.append(f"{f['bib']['n_entries']} entries, newest {f['bib'].get('newest_year')}")
        if f.get("code"):
            c = f["code"]
            notes.append(f"{c['language']}, {c['lines']} lines" + (f", {c['hardcoded_paths']} hard-coded path(s)" if c.get("hardcoded_paths") else ""))
        if f.get("duplicate_of"):
            notes.append(f"duplicate of `{f['duplicate_of']}`")
        if f.get("big_file"):
            notes.append("≥20MB")
        if f.get("extracted_text"):
            notes.append(f"text → `{f['extracted_text']}`")
        L.append(f"| {f['role']} | `{f['path']}` | {f['size_h']} | {f['mtime']} | {'; '.join(notes)} |")
    L.append("")
    if s.get("pdf_extraction", {}).get("none"):
        L += ["> ⚠ " + str(s["pdf_extraction"]["none"]) + " PDF(s) could not be read: no `pdftotext` on PATH and no `pypdf` package. "
              "Install one (`brew install poppler` or `pip install pypdf`) and re-run.", ""]
    L += ["---", "*Generated by `.claude/scripts/paper_intake.py`. Nothing was copied or modified; extracted text lives in `extracted/` (gitignored).*"]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Inventory an abandoned paper's materials for /revive.")
    ap.add_argument("paths", nargs="+", help="files or directories")
    ap.add_argument("--slug", required=True, help="short kebab-case name for the revival folder")
    ap.add_argument("--out", default="quality_reports/revival", help="base output folder (default quality_reports/revival)")
    ap.add_argument("--max-chars", type=int, default=400_000, help="cap on extracted text per file")
    ap.add_argument("--json", action="store_true", help="print the manifest as JSON instead of the summary")
    a = ap.parse_args()

    paths = [Path(p) for p in a.paths]
    missing = [str(p) for p in paths if not p.expanduser().exists()]
    if missing:
        print("not found: " + ", ".join(missing), file=sys.stderr)
        return 2
    slug = re.sub(r"[^a-z0-9-]+", "-", a.slug.lower()).strip("-") or "paper"
    out_dir = (PROJECT_ROOT / a.out / slug) if not Path(a.out).is_absolute() else Path(a.out) / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(paths, out_dir, a.max_chars)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    (out_dir / "inventory.md").write_text(render_inventory(manifest, slug), encoding="utf-8")

    if a.json:
        print(json.dumps(manifest, indent=2, default=str))
        return 0
    s = manifest["summary"]
    print(f"📦 PAPER INTAKE — {s.get('title_guess') or slug}")
    print(f"   files {s['n_files']} · " + ", ".join(f"{k} {v}" for k, v in sorted(s["roles"].items())))
    print(f"   last modified {s['files_modified']['newest']} · lit horizon {s.get('literature_horizon_year') or '—'} · sample {s.get('sample_period_guess') or '?'}")
    print(f"   data sources: {', '.join(s.get('data_sources_mentioned') or []) or '—'}")
    print(f"   methods: {', '.join(s.get('methods_detected') or []) or '—'}")
    print(f"   code: {', '.join(f'{k} ({v})' for k, v in s['code_languages'].items()) or 'none'} · hard-coded paths {s['code_hardcoded_paths']}")
    print(f"   data: {len([f for f in manifest['files'] if f['role'] == 'data'])} file(s), {s['data_total_h']}" + (f" · ≥20MB: {len(s['big_files'])}" if s["big_files"] else ""))
    if s.get("stall_hints"):
        print("   stall hints: " + ", ".join(f"{k} ({v})" for k, v in s["stall_hints"].items()))
    if s.get("pdf_extraction", {}).get("none"):
        print(f"   ⚠ {s['pdf_extraction']['none']} PDF(s) unreadable — brew install poppler or pip install pypdf")
    print(f"   → {pretty_path(out_dir / 'inventory.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
