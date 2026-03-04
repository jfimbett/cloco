# Separation of Powers (Rules 5 & 6)

**Critics never create. Creators never self-score.**

## Rule 5: Critics Never Create

A critic's job is to evaluate, not to produce artifacts. If a critic produces code, text, or data during its review, something is wrong.

**What critics DO:**
- Score artifacts against a rubric
- List issues with severity and deductions
- Suggest fixes (as recommendations, not implementations)

**What critics DON'T DO:**
- Write code to fix the issues they found
- Rewrite paper sections
- Produce alternative implementations

**Why:** A critic who fixes their own findings has incentive to find only fixable issues. Separation keeps criticism honest.

## Rule 6: Creators Can't Self-Score

A creator cannot evaluate the quality of its own work. The score always comes from the paired critic.

| Agent | Creates | Scored By |
|-------|---------|-----------|
| academic-librarian | Annotated bibliography | academic-editor |
| explorer | Data assessment | data-quality-surveyor |
| causal-strategist | Strategy memo | identification-critic |
| econ-finance-theorist | Theoretical model | theory-critic |
| structural-estimation-expert | Structural model | structural-critic |
| Coder (main Claude) | R/Stata/Python scripts | debugger |
| economics-paper-writer | Paper manuscript | academic-proofreader |

## Enforcement

The research-orchestrator flags violations:
- If a critic invocation produces a file in `code/`, `paper/`, or `talks/` → flag
- If a creator reports its own score → discard, dispatch critic
