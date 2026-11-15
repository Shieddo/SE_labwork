# Lab 5: Issue Table: `scholarship_system.py`

Line numbers refer to the **original** starter file (commit `aa6e272`).
Reports: `reports/before/` (original) and `reports/after/` (fixed).

| Results | Before | After |
|---------|--------|-------|
| Pylint score | 4.69 / 10 | **10.00 / 10** |
| Bandit issues | 2 (1 Medium, 1 Low) | **0** |
| Flake8 issues | 12 | **0** |

## Issues found and fixed (high and medium severity first)

| # | Issue | Tool / Code | Type | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|---------|-------------|--------------|
| 1 | Use of `eval` (code injection) | Bandit B307 (Medium) · Pylint W0123 | Security | 12, 51-53 | The merit formula typed at the prompt is passed straight to `eval()`, so any Python code can run (e.g. `__import__("os").getcwd()`). A bad formula also crashes the program with a `TypeError`. | Parse the formula with `ast.parse(mode="eval")` and evaluate it with a small whitelist walker (`_safe_eval`) that only allows numbers, `gpa`, `credits` and `+ - * /`. `change_formula` checks a new formula first and keeps the default if it is rejected. |
| 2 | Bare `except: pass` | Bandit B110 (Low) · Pylint W0702 · Flake8 E722 | Security / Bug | 37-38 | Every error is caught and ignored, including `KeyboardInterrupt` and typos, so a corrupt or missing results file fails silently. | Catch only `OSError` and `json.JSONDecodeError` and print the reason. |
| 3 | Mutable default argument | Pylint W0102 | Bug | 14 | `logs=[]` is created once and shared by every call, so log entries leak between applicants. | Default to `None` and create a new list inside the function. |
| 4 | Invalid applicant data accepted | *No tool flags this* (found by running the program) | Logic bug | 47-50, 15-19 | U003 (GPA 12.5 on a 10-point scale, −3 credits, income −1) was **shortlisted** with score 119. U004 had no income, which was silently treated as 0 and passed the income check. | Added `validate_applicant()`: GPA must be 0–10, credits must be a non-negative integer, income must be declared and ≥ 0. Invalid applicants are recorded as ineligible with a reason, and that reason is printed. |
| 5 | `global` statements | Pylint W0603 | Design | 25, 34 | Module globals are reassigned from inside functions, which makes state hard to follow and test. | State lives in `results` and `settings` dicts that are changed in place (`clear()`/`update()`), so no `global` is needed. |
| 6 | `open()` without `with` / encoding | Pylint R1732, W1514 | Bug / Resource | 29-31, 36 | File handles may leak if an exception occurs, and the encoding depends on the platform. | `with open(..., encoding="utf-8")` and `json.dump` / `json.load`. |
| 7 | Unused imports | Pylint W0611 · Flake8 F401 | Style | 2, 3 | `math` and `sys` are imported but never used. | Removed. |
| 8 | Builtin `credits` shadowed | Pylint W0622 | Style / Bug risk | 11, 16 | A parameter and a local variable hide the builtin `credits`. | Renamed to `credit_count`. Inside the formula the user-facing name is still `credits`. |
| 9 | Comparison to `True` | Pylint C0121 · Flake8 E712 | Style | 43 | `if results[r]["eligible"] == True:` | `if record["eligible"]:`, iterating with `.items()`. |
| 10 | Non-snake_case name | Pylint C0103 | Style | 40 | `printShortlist` | Renamed to `print_shortlist`. |
| 11 | `%` string formatting | Pylint C0209 | Style | 21 | `"%s scored %s" % (...)` | f-string. |
| 12 | Missing docstrings | Pylint C0114 / C0116 | Documentation | 1, 11, 14, 24, 28, 33, 40, 46 | No module docstring and no function docstrings. | Added them. |
| 13 | `main()` runs on import | Pylint/design (not flagged as a code) | Design | 59 | Importing the module runs the program and blocks on `input()`. | Added an `if __name__ == "__main__":` guard. |
| 14 | Blank lines around definitions | Flake8 E302 / E305 | Formatting | 11, 14, 24, 28, 33, 40, 46, 59 | Only one blank line between top-level definitions. | Two blank lines, as PEP 8 requires. |
| 15 | Line too long | Flake8 E501 | Formatting | (new code) | Two lines over 79 characters after refactoring. | Wrapped. |
| 16 | Unused arguments | Pylint W0613 | Code smell | 11 | `gpa`/`credits` were only read indirectly through `eval`, so Pylint saw them as unused. | They are now passed explicitly to the safe evaluator. |

## Commits

1. `Add baseline Pylint, Bandit and Flake8 reports (before fixes)`
2. `Fix Bandit issues: ...` (issues 1, 2)
3. `Fix Pylint issues and validate applicant data` (issues 3–13, 16)
4. `Fix Flake8 style issues` (issues 14, 15)
5. `Add after-reports, issue table and reflection`
