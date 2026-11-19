# SE_labwork

Software Engineering lab work: Syed Mohammed Hashir (PES2UG24AM167, Section 5C).

| Lab | Folder | Deliverables |
|-----|--------|--------------|
| 1: Requirements Engineering & Use Cases | [`Lab1/`](Lab1) | Requirements table (`.xlsx` / `.docx` / `.pdf`), use-case diagram (`UseCaseDiagram_CoffeeKiosk.pdf`), use-case flow (`Lab1_UseCase_Flow.docx` / `.pdf`) |
| 3: Component Modelling & Architecture | [`Lab3/`](Lab3) | Component diagram (`ComponentDiagram_CoffeeKiosk.png` / `.pdf`), one-page justification (`Lab3_Architecture_Justification.docx` / `.pdf`) |
| 5: Static Code Analysis | [`Lab5/`](Lab5) | Fixed `scholarship_system.py`, Pylint / Bandit / Flake8 reports in `reports/before/` and `reports/after/`, issue table (`issues.md`), reflection (`reflection.md`) |
| 6: Code & Branch Coverage | [`Lab6/`](Lab6) | `CodeCoverageTest_amusement_park_ride_access.py`, `BranchCoverageTest_amusement_park_ride_access.py`, terminal screenshots in `screenshots/` |
| 7: Fuzz Testing | [`Lab7/`](Lab7) | `Lab7_FuzzTesting_Report.pdf` (screenshots), fixed `processor.py`, updated `test_processor.py` |

## Results

- **Lab 5:** Pylint 4.69 → 10.00, Bandit 2 issues → 0, Flake8 12 issues → 0.
- **Lab 6:** 100% line coverage (14 tests) and 100% branch coverage (30 tests), up from 45% with the starter test.
- **Lab 7:** Hypothesis found 13 crashing inputs. After the fix, all 9 tests pass.

## Commit history

Labs 5, 6 and 7 were brought in with `git subtree`, so the original commits are kept. Each fix is its own commit: one per tool in Lab 5, one per test file in Lab 6, and tests then fix in Lab 7. To see them, run `git log --graph`.
