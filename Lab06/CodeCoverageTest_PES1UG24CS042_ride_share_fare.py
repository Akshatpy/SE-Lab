# Lab 6 - Code (Line) Coverage Tests
# Name: Akshat Sharma
# SRN: PES1UG24CS042
# Aim: make every line of ride_share_fare.py run at least once

import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ---------- extra_distance_fare ----------

def test_unknown_cab_type():
    with pytest.raises(ValueError):
        extra_distance_fare("bike", 10, "city", False)

def test_negative_distance():
    with pytest.raises(ValueError):
        extra_distance_fare("mini", -1, "city", False)

def test_within_included_distance():
    # sedan includes 8 km, so 5 km has no extra fare
    assert extra_distance_fare("sedan", 5, "city", False) == 0

def test_subscriber_gets_extra_km_city():
    # mini = 5 km + 3 km for subscriber = 8 km included, extra = 2 km at 12
    assert extra_distance_fare("mini", 10, "city", True) == 24

def test_long_outstation_trip():
    # suv includes 12 km, extra = 25 km (> 20), rate = 18 + 8 + 4 = 30
    assert extra_distance_fare("suv", 37, "outstation", False) == 750


# ---------- seats_and_bags_ok ----------

def test_wheelchair_ok():
    assert seats_and_bags_ok(2, 0, True) is True

def test_too_many_passengers():
    assert seats_and_bags_ok(5, 1, False) is False

def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True


# ---------- pickup_status ----------

def test_scheduled_on_time():
    # cutoff = 10
    assert pickup_status(12, True, False) == "on_time"

def test_airport_delayed():
    # cutoff = 5 + 10 = 15, 15 - 15 = 0, so 3 is delayed
    assert pickup_status(3, False, True) == "delayed"

def test_missed_pickup():
    # cutoff = 5, 5 - 15 = -10, so -20 is missed
    assert pickup_status(-20, False, False) == "missed"
