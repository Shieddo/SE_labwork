"""Lab 6 - Branch coverage tests for amusement_park_ride_access.py.

Goal: make every decision (if / elif / loop) take BOTH outcomes (>= 90%
branch coverage). Run with:
    coverage run --branch -m pytest BranchCoverageTest_amusement_park_ride_access.py
    coverage report -m
"""
import pytest
from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints,
)


def patron(height=150, health_warning=False, is_child=False):
    return {"height_cm": height, "health_warning": health_warning,
            "is_child": is_child}


def group(ride_type="family", patrons=None, is_open=True, fast_lane=False):
    return {"is_open": is_open, "ride_type": ride_type,
            "has_fast_lane": fast_lane, "patrons": patrons or []}


# ---------------- process_ride_admissions ----------------

# Starter example test (kept)
def test_single_adult_family_ride():
    result = process_ride_admissions([group("family", [patron()])], 5.0)
    assert result["total_revenue"] == 10.0
    assert result["status"] == "COMPLETED"


def test_groups_not_a_list_raises():
    with pytest.raises(ValueError):
        process_ride_admissions("not a list", 5.0)


def test_negative_express_fee_raises():
    with pytest.raises(ValueError):
        process_ride_admissions([], -1.0)


def test_closed_group_is_skipped():
    closed = group("family", [patron()], is_open=False)
    result = process_ride_admissions([closed], 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_roller_coaster_adult_with_fast_lane():
    g = group("roller_coaster", [patron()], fast_lane=True)
    result = process_ride_admissions([g], 7.5)
    assert result == {"total_revenue": 32.5, "status": "COMPLETED"}


def test_water_ride_child_gets_discount():
    g = group("water_ride", [patron(is_child=True)])
    result = process_ride_admissions([g], 5.0)
    assert result == {"total_revenue": 10.8, "status": "COMPLETED"}


def test_unknown_ride_type_is_rejected():
    result = process_ride_admissions([group("bumper_cars", [patron()])], 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_invalid_height_and_short_patron_rejected():
    g = group("family", [patron(height=0), patron(height=110), patron()])
    result = process_ride_admissions([g], 5.0)
    assert result == {"total_revenue": 10.0, "status": "COMPLETED"}


def test_health_warning_on_roller_coaster_voids_group():
    g = group("roller_coaster", [patron(), patron(health_warning=True),
                                 patron()])
    result = process_ride_admissions([g], 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_health_warning_on_family_ride_charges_nothing_for_that_patron():
    g = group("family", [patron(health_warning=True), patron()])
    result = process_ride_admissions([g], 5.0)
    assert result == {"total_revenue": 10.0, "status": "COMPLETED"}


def test_more_than_four_rejections_triggers_safety_audit():
    g = group("family", [patron(height=100)] * 5 + [patron()])
    result = process_ride_admissions([g], 5.0)
    assert result == {"total_revenue": 10.0, "status": "SAFETY_AUDIT"}


# ---------------- inspect_safety_restraints ----------------

def test_no_restraint_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_two_consecutive_unlatched_readings_lock():
    assert inspect_safety_restraints([[1, 0, 0, 1]]) == "EMERGENCY_LOCK"


def test_isolated_unlatched_readings_are_safe():
    assert inspect_safety_restraints([[1, 0, 1, 1]]) == "SAFE"


# ======== Additional tests targeting decision branches and edges ========

def test_fast_lane_false_adds_no_fee():
    """has_fast_lane False -> fee not added (50 -> 53 branch)."""
    g = group("roller_coaster", [patron()], fast_lane=False)
    assert process_ride_admissions([g], 9.0)["total_revenue"] == 25.0


def test_fast_lane_only_group_with_no_patrons():
    """Empty patron list: inner loop body never runs, fee still added."""
    g = group("family", [], fast_lane=True)
    result = process_ride_admissions([g], 4.0)
    assert result == {"total_revenue": 4.0, "status": "COMPLETED"}


def test_zero_fee_is_valid_boundary():
    """express_pass_fee == 0 is allowed (False side of fee < 0)."""
    result = process_ride_admissions([group("family", [patron()])], 0)
    assert result["status"] == "COMPLETED"


def test_empty_groups_list():
    assert process_ride_admissions([], 5.0) == {"total_revenue": 0.0,
                                                "status": "ZERO_ADMISSIONS"}


def test_group_without_keys_uses_defaults():
    """Missing is_open -> treated as closed; missing ride_type -> family."""
    closed_by_default = {"patrons": [patron()]}
    open_defaults = {"is_open": True, "patrons": [{"height_cm": 130}]}
    result = process_ride_admissions([closed_by_default, open_defaults], 5.0)
    assert result == {"total_revenue": 10.0, "status": "COMPLETED"}


def test_height_exactly_120_is_admitted():
    """Boundary: height_cm < 120 is False at exactly 120."""
    g = group("water_ride", [patron(height=120)])
    assert process_ride_admissions([g], 5.0)["total_revenue"] == 18.0


def test_negative_height_rejected():
    g = group("family", [patron(height=-5), patron()])
    assert process_ride_admissions([g], 5.0)["total_revenue"] == 10.0


def test_exactly_four_rejections_is_not_an_audit():
    """Boundary: rejected_patrons > 4 is False at exactly 4."""
    g = group("family", [patron(height=100)] * 4 + [patron()])
    result = process_ride_admissions([g], 5.0)
    assert result == {"total_revenue": 10.0, "status": "COMPLETED"}


def test_safety_audit_with_zero_revenue():
    """Audit check is evaluated before the zero-revenue check."""
    g = group("family", [patron(height=0)] * 5)
    result = process_ride_admissions([g], 5.0)
    assert result == {"total_revenue": 0.0, "status": "SAFETY_AUDIT"}


def test_mixed_groups_total_and_rounding():
    groups = [
        group("roller_coaster", [patron(is_child=True)], fast_lane=True),
        group("water_ride", [patron(), patron(is_child=True)]),
        group("family", [patron(is_child=True)], is_open=False),
    ]
    result = process_ride_admissions(groups, 2.5)
    assert result == {"total_revenue": 46.3, "status": "COMPLETED"}


def test_health_warning_before_and_after_short_patron_on_coaster():
    """Rejections counted before the break still count."""
    g = group("roller_coaster", [patron(height=100),
                                 patron(health_warning=True)], fast_lane=True)
    result = process_ride_admissions([g], 3.0)
    assert result == {"total_revenue": 3.0, "status": "COMPLETED"}


def test_none_restraint_streams_is_no_data():
    assert inspect_safety_restraints(None) == "NO_DATA"


def test_empty_sensor_stream_is_safe():
    """Inner loop never entered for an empty reading list."""
    assert inspect_safety_restraints([[]]) == "SAFE"


def test_all_latched_multiple_streams_safe():
    assert inspect_safety_restraints([[1, 1], [1, 0], [0, 1]]) == "SAFE"


def test_lock_detected_in_later_stream():
    """Streak resets per stream; second stream has two zeros in a row."""
    assert inspect_safety_restraints([[1, 0], [0, 0]]) == "EMERGENCY_LOCK"


def test_zeros_split_across_streams_do_not_lock():
    """A single trailing 0 and a single leading 0 in different streams."""
    assert inspect_safety_restraints([[1, 0], [0, 1]]) == "SAFE"
