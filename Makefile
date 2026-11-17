# The one test command. CI runs it on every push and pull request.
# Standard library Python only: no install step.
.PHONY: test
test:
	python3 evals/check_skill.py skills/loopify/SKILL.md
	python3 tests/test_manifests.py
	python3 tests/test_ticks_lint.py
	python3 tests/test_loop_status.py
	python3 evals/loop_line_lint.py "/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick."
