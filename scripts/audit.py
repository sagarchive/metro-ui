#!/usr/bin/env python3
"""Lint an HTML/CSS file for non-Metro styling. usage: audit.py page.html [more.css ...]"""
import re, sys
RULES = [
    (r"border-radius\s*:\s*(?!0\b|50%)[^;}]*\d", "rounded corners (only rings and dots may be round: use 50%)"),
    (r"box-shadow\s*:\s*(?!none)", "shadow"),
    (r"text-shadow\s*:\s*(?!none)", "text shadow"),
    (r"(linear|radial)-gradient", "gradient"),
    (r"backdrop-filter|filter\s*:\s*blur", "blur"),
    (r"line-height\s*:", "explicit line-height (use natural; pitches assume it)"),
    (r"font-family\s*:[^;}]*(Roboto|Inter|Arial|Helvetica|system-ui|-apple-system)", "non-Segoe font"),
    (r"font-weight\s*:\s*(700|bold|800|900)", "bold weight (Metro uses Light/Semilight/Regular/Semibold)"),
    (r"\bopacity\s*:\s*0?\.[0-9]+", "fractional opacity (check it is a documented dim)"),
]
bad = 0
for path in sys.argv[1:]:
    txt = open(path, encoding="utf-8").read()
    for rx, msg in RULES:
        for m in re.finditer(rx, txt, re.I):
            ln = txt.count("\n", 0, m.start()) + 1
            print(f"{path}:{ln}: {msg}: {m.group(0)[:60]}"); bad += 1
    for h in set(re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", txt)):
        pass
print("clean" if not bad else f"{bad} issue(s)")
sys.exit(1 if bad else 0)
