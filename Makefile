# cloco — shell entry points (everything here also works inside Claude Code via skills)
.PHONY: status watch audit data wrds paper lean lean-setup clean help

help:            ## list targets
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-10s %s\n", $$1, $$2}'

status:          ## pipeline dashboard: phase, scores, gates, git, data, lessons
	@python3 .claude/scripts/dashboard.py

watch:           ## same dashboard, refreshed every 30 s
	@python3 .claude/scripts/dashboard.py --watch

audit:           ## git hygiene audit (secrets, data files, big files, branches)
	@python3 .claude/scripts/git_tools.py audit

data:            ## is every registered dataset present on this machine?
	@python3 .claude/scripts/data_registry.py check

wrds:            ## test WRDS credentials
	@python3 .claude/scripts/wrds_client.py test

paper:           ## build paper/main.pdf
	latexmk -pdf -cd paper/main.tex

lean:            ## build lean/ and machine-check every proof in lean/ledger.json
	@python3 .claude/scripts/lean_tools.py verify

lean-setup:      ## install elan + Lean toolchain + Mathlib cache (first time ≈5 GB)
	@python3 .claude/scripts/lean_tools.py setup

clean:           ## remove LaTeX build artefacts
	latexmk -cd -C paper/main.tex
