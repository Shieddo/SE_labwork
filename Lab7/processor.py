import math

MIN_HEIGHT_CM = 1
MAX_HEIGHT_CM = 300
REQUIRED_HEIGHT_CM = 120


def validate_height_and_fastpass(rider_spec):
    # Bug fix: None / non-string input used to raise AttributeError
    if not isinstance(rider_spec, str):
        return "Invalid input: rider spec must be text like 140:YES"

    # Bug fix: '' or '140' (no ':') and '1:2:3' raised ValueError on unpacking
    parts = rider_spec.strip().split(':')
    if len(parts) != 2:
        return "Invalid input: expected exactly one ':' (Height:FastPass)"
    height_str, pass_str = parts[0].strip(), parts[1].strip().upper()

    # Bug fix: int('') / int('abc') / int('0.0') raised ValueError.
    # Only plain ASCII digits are accepted (int() also allows '+', '_' and
    # non-ASCII digits, which are not valid heights).
    if not (height_str.isascii() and height_str.isdigit()):
        return "Invalid input: height must be a whole number of centimetres"
    height = int(height_str)
    # Bug fix: 0 cm or 99999 cm were accepted as real heights
    if not MIN_HEIGHT_CM <= height <= MAX_HEIGHT_CM:
        return (f"Invalid input: height must be between {MIN_HEIGHT_CM} "
                f"and {MAX_HEIGHT_CM} cm")

    # Bug fix: anything other than YES/NO raised KeyError
    pass_map = {"YES": True, "NO": False}
    if pass_str not in pass_map:
        return "Invalid input: FastPass must be YES or NO"
    has_fastpass = pass_map[pass_str]

    eligible = height >= REQUIRED_HEIGHT_CM
    status = "FastPass Priority" if has_fastpass else "Standard Entry"
    return f"Height {height}cm: {'Approved' if eligible else 'Denied'} ({status})"


def compute_dispatch_throughput(ride_metric_str):
    # Bug fix: None / non-string input raised AttributeError
    if not isinstance(ride_metric_str, str):
        return "Invalid input: expected text like 48/2.5"

    # Bug fix: missing or extra '/' raised ValueError on unpacking
    parts = ride_metric_str.split('/')
    if len(parts) != 2:
        return "Invalid input: expected exactly one '/' (riders/minutes)"

    # Bug fix: float('') / float('abc') raised ValueError
    try:
        riders = float(parts[0])
        cycle_mins = float(parts[1])
    except ValueError:
        return "Invalid input: riders and minutes must be numbers"

    # Bug fix: nan / inf were accepted and produced nonsense results
    if not (math.isfinite(riders) and math.isfinite(cycle_mins)):
        return "Invalid input: values must be finite numbers"
    if riders < 0:
        return "Invalid input: riders cannot be negative"
    # Bug fix: 0 minutes raised ZeroDivisionError; negative time is meaningless
    if cycle_mins <= 0:
        return "Invalid input: cycle minutes must be greater than 0"

    rate = riders / cycle_mins
    # Bug fix: e.g. 1e308/1e-308 overflows to inf
    if not math.isfinite(rate):
        return "Invalid input: throughput is too large to compute"
    return round(rate, 2)


def resolve_safety_restraint_code(zone_code):
    # Bug fix: None / non-string input raised AttributeError
    if not isinstance(zone_code, str):
        return "Invalid input: zone code must be text like CST_01"

    prefix = zone_code.strip().upper()[:3]
    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar"
    }
    # Bug fix: unknown or empty prefixes raised KeyError
    return restraint_types.get(
        prefix,
        f"Unknown zone code {zone_code.strip()!r}: expected a code starting "
        f"with one of {', '.join(restraint_types)}")


def read_input(prompt):
    # Bug fix: running out of input (Ctrl+Z / Ctrl+D) raised EOFError
    try:
        return input(prompt)
    except EOFError:
        return ""


def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = read_input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(r_input))

    print("\n==== Running compute_dispatch_throughput ====")
    t_input = read_input("Enter riders/mins (e.g. 48/2.5): ")
    print("Throughput (riders/min):", compute_dispatch_throughput(t_input))

    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = read_input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(z_input))


if __name__ == "__main__":
    main()
