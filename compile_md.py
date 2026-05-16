#!/usr/bin/env python3
"""
compile_md.py — Convert paper/paper_coauthor.md to PDF via pandoc + latexmk.

Usage (from project root):
    python compile_md.py
    (On this machine use: C:/Users/jfimb/anaconda3/python.exe compile_md.py)

Steps:
  1. pandoc converts paper/paper_coauthor.md -> paper/sections_from_md.tex  (body only)
  2. latexmk compiles paper/main_from_md.tex -> paper/main_from_md.pdf
"""
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"\nFAILED at: {' '.join(cmd)}")
        sys.exit(1)


# Step 1: Markdown -> LaTeX body (no --standalone = body content only, no preamble)
run([
    "pandoc",
    "paper/paper_coauthor.md",
    "--from", "markdown+raw_tex",
    "--to", "latex",
    "--output", "paper/sections_from_md.tex",
])

# Step 2: Compile to PDF (-cd changes to paper/ dir so relative paths resolve)
run(["latexmk", "-pdf", "-cd", "paper/main_from_md.tex"])

print("\nDone — PDF at paper/main_from_md.pdf")
