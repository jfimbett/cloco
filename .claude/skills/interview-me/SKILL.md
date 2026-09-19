---
name: interview-me
description: Interactive interview to formalize a research idea into a structured specification with hypotheses and empirical strategy
disable-model-invocation: true
argument-hint: "[brief topic or 'start fresh']"
allowed-tools: ["Read", "Write"]
---

# Research Interview

Conduct a structured interview to help formalize a research idea into a concrete specification.

**Input:** `$ARGUMENTS` — a brief topic description or "start fresh" for an open-ended exploration.

---

## How This Works

This is a **conversational** skill. Instead of producing a report immediately, you conduct an interview by asking questions one at a time, probing deeper based on answers, and building toward a structured research specification.

**Do NOT use AskUserQuestion.** Ask questions directly in your text responses, one or two at a time. Wait for the user to respond before continuing.

---

## Interview Structure

### Phase 0: Project Type (always first — 1 question)

Ask this before anything else:

"Before we dig into your research question, it helps to understand what kind of paper you're aiming to write. Which of these best describes it?

**(A) Reduced-Form Empirical** — You want to identify causal effects using data (DiD, RDD, IV, event study, etc.). The core deliverable is an estimated causal effect.

**(B) Pure Theory** — You want to build a formal model: propositions, proofs, comparative statics. No data or estimation required.

**(C) Structural Estimation** — You want to build a formal model AND estimate its parameters using data (MLE, GMM, SMM, BLP, etc.). Theory and empirics are tightly coupled.

**(D) Empirical + Motivating Theory** — Primarily empirical, but with a formal theory section that generates testable predictions motivating your empirical design.

There's no wrong answer — this just determines which tools and agents we'll use."

Wait for the user to choose before proceeding to Phase 1.
Record the answer as `project_type` (one of: `empirical`, `theory`, `structural`, `empirical+theory`).

**Phase routing based on project type:**
- `theory`: Skip Phase 3 (Data) and Phase 4 (Identification). Probe model structure deeply in Phase 2.
- `structural`: Keep all phases. In Phase 3, add: "What will you estimate? What are the key structural parameters?"
- `empirical+theory`: Keep all phases. In Phase 2, probe how the theory generates testable predictions.
- `empirical`: Run all phases as normal.

---

### Phase 1: The Big Picture (1-2 questions)
- "What phenomenon or puzzle are you trying to understand?"
- "Why does this matter? Who should care about the answer?"

### Phase 2: Theoretical Motivation (1-2 questions)
- "What's your intuition for why X happens / what drives Y?"
- "What would standard theory predict? Do you expect something different?"

### Phase 3: Data and Setting (1-2 questions)
- "What data do you have access to, or what data would you ideally want?"
- "Is there a specific context, time period, or institutional setting you're focused on?"

### Phase 4: Identification (1-2 questions)
- "Is there a natural experiment, policy change, or source of variation you can exploit?"
- "What's the biggest threat to a causal interpretation?"

### Phase 5: Expected Results (1-2 questions)
- "What would you expect to find? What would surprise you?"
- "What would the results imply for policy or theory?"

### Phase 6: Contribution (1 question)
- "How does this differ from what's already been done? What's the gap you're filling?"

---

## After the Interview

Once you have enough information (typically 5-8 exchanges), produce TWO outputs:

### Output 1: Domain Profile

If `.claude/rules/domain-profile.md` still contains placeholders, fill it in based on the interview. This calibrates all agents to the researcher's field:

- **Field & adjacent subfields** — inferred from the topic
- **Target journals** — ranked by tier for this field
- **Common data sources** — datasets typical for this area
- **Common identification strategies** — designs used in this literature
- **Field conventions** — estimation quirks, outcome transformations, clustering norms
- **Seminal references** — papers every referee will expect you to cite
- **Field-specific referee concerns** — the "gotcha" questions referees always ask

Save directly to `.claude/rules/domain-profile.md` (overwrite the template).

If the domain profile is already filled (from a previous interview or manual entry), confirm with the user whether to update or keep the existing one.

### Output 2: Research Specification Document

Produce a **Research Specification Document**:

```markdown
# Research Specification: [Title]

**Date:** [YYYY-MM-DD]
**Researcher:** [from conversation context]

## Project Type
[empirical / theory / structural / empirical+theory]

## Recommended Pipeline
[List the relevant commands for this type — see .claude/WORKFLOW_QUICK_REF.md]

## Research Question

[Clear, specific question in one sentence]

## Motivation

[2-3 paragraphs: why this matters, theoretical context, policy relevance]

## Hypothesis

[Testable prediction with expected direction]

## Empirical Strategy
<!-- Skip this section for type = theory -->

- **Method:** [e.g., Difference-in-Differences with staggered adoption]
- **Treatment:** [What varies]
- **Control:** [Comparison group]
- **Key identifying assumption:** [What must hold]
- **Robustness checks:** [Pre-trends, placebo tests, etc.]

## Theoretical Model
<!-- Fill this section for type = theory, structural, or empirical+theory -->

- **Model type:** [e.g., principal-agent, search, spatial, dynamic discrete choice]
- **Key agents/players:** [Who decides what]
- **Core mechanism:** [The economic logic to be formalized]
- **Main predictions:** [Propositions you expect to derive]
- **Structural parameters (if applicable):** [What will be estimated]

## Data
<!-- Skip this section for type = theory -->

- **Primary dataset:** [Name, source, coverage]
- **Key variables:** [Treatment, outcome, controls]
- **Sample:** [Unit of observation, time period, N]

## Expected Results

[What the researcher expects to find and why]

## Contribution

[How this advances the literature — 2-3 sentences]

## Open Questions

[Issues raised during the interview that need further thought]
```

**Save to:** `quality_reports/research_spec_[sanitized_topic].md`

Include `project_name:`, `project_type:`, and `project_slug:` lines near the top (the session-welcome hook, `/pipeline-status`, and `/setup-project` parse them). `project_slug` is two or three memorable words in kebab-case (e.g. `branch-closures`); the project's repository and folder become `cloco-<project_slug>`.

### After saving

**Identity first.** Run `python3 .claude/scripts/project_setup.py status`. If it reports `needs-detach` (folder still `cloco`, origin still `cloco.git`), tell the user the checkout is now a project and must get its own name and GitHub repository before any push — offer `/setup-project` right away (it asks: repository name, create on GitHub?, private or public, rename the folder). Pushes to the template are blocked until this is done.

Then tell the user the next command is `/discovery` — it reads this spec and runs the literature and data lanes in parallel with their critics. If the researcher seemed unsure whether the idea is worth a full project, suggest `/scout` first.

---

## Interview Style

- **Be curious, not prescriptive.** Your job is to draw out the researcher's thinking, not impose your own ideas.
- **Probe weak spots gently.** If the identification strategy sounds fragile, ask "What would a skeptic say about...?" rather than "This won't work because..."
- **Build on answers.** Each question should follow from the previous response.
- **Know when to stop.** If the researcher has a clear vision after 4-5 exchanges, move to the specification. Don't over-interview.
