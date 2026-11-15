"""Lab 6 - Code (line) coverage tests for amusement_park_ride_access.py.

Goal: execute every statement of the module at least once (>= 90% line
coverage). Run with:
    coverage run -m pytest CodeCoverageTest_amusement_park_ride_access.py
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
