"""Preprocess main.tex for pandoc: remove \\IfFileExists guards and expand macros."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

src = (BASE / "main.tex").read_text(encoding="utf-8")

# Remove \IfFileExists{file}{content}{} → just content
# Pattern: \IfFileExists{...}{%\n ... \n}{}
# The content is between the second { and its matching }
def remove_iffileexists(text):
    result = []
    i = 0
    tag = r"\IfFileExists{"
    while i < len(text):
        pos = text.find(tag, i)
        if pos == -1:
            result.append(text[i:])
            break
        result.append(text[i:pos])
        # Skip \IfFileExists{filename}
        j = text.index("}", pos + len(tag)) + 1
        # Now we're at {%  or { — the "true" branch
        # Find matching brace
        assert text[j] == "{", f"Expected {{ at pos {j}, got {text[j]}"
        depth = 1
        k = j + 1
        while k < len(text) and depth > 0:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        true_branch = text[j+1:k-1]
        # Remove leading/trailing %\n
        true_branch = re.sub(r"^%\s*\n", "", true_branch)
        result.append(true_branch)
        # Skip the false branch {}
        # Find next {}
        rest = text[k:].lstrip()
        if rest.startswith("{}"):
            i = k + text[k:].index("{}") + 2
        else:
            i = k
    return "".join(result)

src = remove_iffileexists(src)

# Remove \def macros' trailing \, to prevent \mspace issues
src = src.replace(r"\def\E{{\mathbb{E}}\,}", r"\newcommand{\E}{\mathbb{E}}")
src = src.replace(r"\def\V{{\mathbb{V}}\,}", r"\newcommand{\V}{\mathbb{V}}")
src = src.replace(r"\def\Cov{{\mathrm{Cov}}}", r"\newcommand{\Cov}{\mathrm{Cov}}")
src = src.replace(r"\def\1{{\mathds{1}}}", r"\newcommand{\1}{\mathds{1}}")
src = src.replace(r"\def\posreal{{\mathbb{R_{++}}}\,}", r"\newcommand{\posreal}{\mathbb{R_{++}}}")
src = src.replace(r"\def\nnegreal{{\mathbb{R_{+}}}\,}", r"\newcommand{\nnegreal}{\mathbb{R_{+}}}")

(BASE / "main_pandoc.tex").write_text(src, encoding="utf-8")
print("Wrote main_pandoc.tex")
