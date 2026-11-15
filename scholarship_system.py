"""Student scholarship eligibility screener.

Computes a merit score from GPA and extracurricular credits, checks the
declared family income against a limit and saves the shortlist to
``scholarships.json``.
"""
import ast
import json
import operator

INCOME_LIMIT = 800000
CUTOFF = 85
MAX_GPA = 10.0
DEFAULT_FORMULA = "gpa * 10 + credits * 2"
RESULTS_FILE = "scholarships.json"

# Mutable state lives in dictionaries so no ``global`` statements are needed.
results = {}
settings = {"merit_formula": DEFAULT_FORMULA}

_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
_FORMULA_VARIABLES = ("gpa", "credits")


def _safe_eval(node, variables):
    """Evaluate a parsed arithmetic formula without using eval()."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body, variables)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id in variables:
        return variables[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left, variables),
                                           _safe_eval(node.right, variables))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand, variables))
    raise ValueError("Formula may only use gpa, credits, numbers and + - * /")


def calculate_merit_score(gpa, credit_count):
    """Return the merit score for a GPA and extracurricular credits."""
    tree = ast.parse(settings["merit_formula"], mode="eval")
    values = dict(zip(_FORMULA_VARIABLES, (gpa, credit_count)))
    return round(float(_safe_eval(tree, values)), 2)


def validate_applicant(test_scores):
    """Return an error message if the applicant data is invalid, else None."""
    gpa = test_scores.get("gpa")
    credit_count = test_scores.get("credits", 0)
    income = test_scores.get("income")
    if not isinstance(gpa, (int, float)) or not 0 <= gpa <= MAX_GPA:
        return f"GPA must be between 0 and {MAX_GPA}"
    if not isinstance(credit_count, int) or credit_count < 0:
        return "credits must be a non-negative whole number"
    if not isinstance(income, (int, float)) or income < 0:
        return "family income must be declared and non-negative"
    return None


def evaluate_applicant(student_id, test_scores, logs=None):
    """Score one applicant, record the result and return eligibility."""
    if logs is None:
        logs = []
    error = validate_applicant(test_scores)
    if error:
        results[student_id] = {"score": None, "eligible": False,
                               "error": error}
        logs.append(f"{student_id} rejected: {error}")
        return False
    score = calculate_merit_score(test_scores["gpa"],
                                  test_scores.get("credits", 0))
    eligible = score >= CUTOFF and test_scores["income"] < INCOME_LIMIT
    results[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Switch to a new merit formula if it is a safe arithmetic expression."""
    try:
        _safe_eval(ast.parse(new_formula, mode="eval"),
                   {"gpa": 1, "credits": 1})
    except (SyntaxError, ValueError, ZeroDivisionError) as err:
        print("Rejected formula, keeping default:", err)
        return False
    settings["merit_formula"] = new_formula
    return True


def persist_results(file=RESULTS_FILE):
    """Write all results to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)


def load_results(file=RESULTS_FILE):
    """Replace the in-memory results with the ones saved in a JSON file."""
    try:
        with open(file, encoding="utf-8") as handle:
            loaded = json.load(handle)
    except (OSError, json.JSONDecodeError) as err:
        print("Could not load saved results:", err)
        return
    results.clear()
    results.update(loaded)


def print_shortlist():
    """Print eligible applicants, then any rejected for invalid data."""
    print("Shortlisted applicants:")
    for student_id, record in results.items():
        if record["eligible"]:
            print(" ", student_id, "score =", record["score"])
    for student_id, record in results.items():
        if record.get("error"):
            print(" ", student_id, "rejected:", record["error"])


def main():
    """Screen the sample applicants and print the shortlist."""
    evaluate_applicant("U001", {"gpa": 9.1, "credits": 4, "income": 450000})
    evaluate_applicant("U002", {"gpa": 7.2, "credits": 1, "income": 300000})
    evaluate_applicant("U003", {"gpa": 12.5, "credits": -3, "income": -1})
    evaluate_applicant("U004", {"gpa": 6.5})
    formula = input("Merit formula (Enter to keep default): ").strip()
    if formula:
        change_formula(formula)
    evaluate_applicant("U005", {"gpa": 8.4, "credits": 3, "income": 600000})
    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
