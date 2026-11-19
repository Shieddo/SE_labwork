from hypothesis import given, settings, strategies as st
from processor import validate_height_and_fastpass, compute_dispatch_throughput, resolve_safety_restraint_code

# ---------------------------------------------------------------------------
# 1. "No crash" fuzz tests (starter tests, completed with try/except).
#    Any exception raised for ANY input (random text or None) is a bug.
# ---------------------------------------------------------------------------


@settings(max_examples=500)
@given(st.text() | st.none())
def test_validate_height_and_fastpass_no_crash(s):
    try:
        validate_height_and_fastpass(s)
    except Exception as e:
        assert False, f"validate_height_and_fastpass crashed on {s!r} with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_compute_dispatch_throughput_safe(s):
    try:
        compute_dispatch_throughput(s)
    except Exception as e:
        assert False, f"compute_dispatch_throughput crashed on {s!r} with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_resolve_safety_restraint_code_safe(s):
    try:
        resolve_safety_restraint_code(s)
    except Exception as e:
        assert False, f"resolve_safety_restraint_code crashed on {s!r} with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 2. Structured fuzzing: inputs that LOOK valid (right separators) but carry
#    edge-case values, so Hypothesis reaches the deeper code paths.
# ---------------------------------------------------------------------------

numberish = st.one_of(
    st.integers(-10**6, 10**6).map(str),
    st.floats(allow_nan=True, allow_infinity=True).map(str),
    st.sampled_from(["", " ", "abc", "0", "-0", "1e309", "nan", "inf", "١٢٠"]),
)


@given(numberish, st.sampled_from(["YES", "no", " Yes ", "MAYBE", "", "Y"]))
def test_rider_spec_with_edge_values_no_crash(height, fastpass):
    try:
        validate_height_and_fastpass(f"{height}:{fastpass}")
    except Exception as e:
        assert False, f"crashed on {height}:{fastpass} with: {type(e).__name__}: {e}"


@given(numberish, numberish)
def test_throughput_with_edge_values_no_crash(riders, mins):
    try:
        compute_dispatch_throughput(f"{riders}/{mins}")
    except Exception as e:
        assert False, f"crashed on {riders}/{mins} with: {type(e).__name__}: {e}"


@given(st.text(alphabet="CSTWRDPHLX_-0123456789 ", max_size=8))
def test_restraint_code_with_near_valid_codes_no_crash(code):
    try:
        resolve_safety_restraint_code(code)
    except Exception as e:
        assert False, f"crashed on {code!r} with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 3. Property tests: valid inputs must still give the correct answer.
# ---------------------------------------------------------------------------

@given(st.integers(1, 300), st.booleans())
def test_valid_rider_spec_is_correct(height, fastpass):
    result = validate_height_and_fastpass(f"{height}:{'YES' if fastpass else 'NO'}")
    assert result.startswith(f"Height {height}cm: ")
    assert ("Approved" in result) == (height >= 120)
    assert ("FastPass Priority" in result) == fastpass


@given(st.integers(0, 500), st.floats(0.1, 60, allow_nan=False))
def test_valid_throughput_is_correct(riders, mins):
    assert compute_dispatch_throughput(f"{riders}/{mins}") == round(riders / mins, 2)


@given(st.sampled_from(["CST", "WTR", "DRP", "WHL"]), st.text(max_size=5))
def test_known_prefixes_resolve(prefix, suffix):
    result = resolve_safety_restraint_code(f"{prefix.lower()}{suffix}")
    assert result in {"Over-the-Shoulder Harness", "Lap Bar and Seatbelt",
                      "Hydraulic Shoulder Vest", "Manual Safety Bar"}
