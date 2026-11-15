# Lab 5: Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the style and formatting issues: unused imports (F401/W0611), missing blank lines (E302/E305), `== True` (E712/C0121), the camelCase name `printShortlist`, %-formatting and missing docstrings. Each warning names the exact line and the fix is mechanical.

The hardest was the `eval()` finding (Bandit B307). Deleting `eval` was not enough, because the program lets the user type a custom merit formula and should keep doing that. I replaced `eval` with a small evaluator built on `ast` that only accepts numbers, `gpa`, `credits` and `+ - * /`. Removing the `global` statements was also harder than it looks, because the module-level `results` dict is shared, so I had to change it in place (`clear()`/`update()`) instead of reassigning it.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

There were no true false positives, but some warnings were really symptoms of a bigger problem. Pylint's W0613 "unused argument `gpa`/`credits`" is technically wrong, because the arguments *were* used, only invisibly through the string passed to `eval()`. The real problem was the `eval` itself, and once that was replaced the warning went away. Bandit rates `try/except/pass` (B110) as only *Low* severity, but here it hid every possible error during loading, so I treated it as more important than its rating.

The tools also missed things. None of them flagged that applicant U003 (GPA 12.5, −3 credits, income −1) was shortlisted, or that a missing income counted as 0. I only found that logic bug by running the program and reading the output.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- **Locally:** run Flake8 and Pylint in the editor on save, and add a `pre-commit` hook that runs `flake8`, `pylint --fail-under=9.5` and `bandit -r .` so bad code never reaches a commit.
- **In CI (e.g. GitHub Actions):** run all three tools on every push and pull request. The build fails on any Bandit Medium/High finding, any Flake8 error, or a Pylint score below the agreed threshold, and the reports are uploaded as build artifacts.
- **Configuration:** keep the rules in a shared `pyproject.toml` / `.flake8` so everyone uses the same rules. Suppress a warning only with an inline comment that explains why (e.g. `# nosec B110 - reason`).

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

- **Security:** the formula prompt can no longer run arbitrary code. `__import__("os").getcwd()` is now rejected and the default formula is kept. Before, a bad formula crashed the program with a `TypeError`.
- **Correctness:** invalid applicants are rejected with a clear reason instead of being shortlisted. Logs no longer leak between calls (mutable default fixed), and files are always closed.
- **Robustness:** load errors are reported instead of silently ignored, and importing the module no longer runs the program.
- **Readability / metrics:** Pylint went from **4.69 to 10.00/10**, Bandit from **2 issues to 0**, and Flake8 from **12 to 0**. Every function now has a docstring and a PEP 8 name, so the code is easier to read and to test.
