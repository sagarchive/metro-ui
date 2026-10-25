# Contributing

Good contributions are **measurements** and **test pages**.

1. Add or correct a number in `references/`, with how you measured it (device photo, official document, screen capture).
2. Add an eval: a content-only brief in `evals/briefs/`, a band spec in `evals/specs/` (see `scripts/spec_check.py`), and a row in `evals/evals.json`.
3. Run the loop: fresh agent (or you, without looking at the spec) builds the page from `SKILL.md`, then `scripts/audit.py` and `scripts/spec_check.py`. Patch the kit or reference wherever the builder was misled.

Rules: no proprietary fonts or screenshots in pull requests, no line-height overrides, square corners only.
