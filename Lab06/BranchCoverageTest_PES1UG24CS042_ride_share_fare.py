# Lab 6 - Branch Coverage Tests
# Name: Akshat Sharma
# SRN: PES1UG24CS042
# Aim: make every if/else in ride_share_fare.py go both True and False

import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ---------- extra_distance_fare ----------

def test_unknown_cab_type():
    with pytest.raises(ValueError):
        extra_distance_fare("bike", 10, "city", False)

def test_negative_distance():
    with pytest.raises(ValueError):
        extra_distance_fare("mini", -1, "city", False)

def test_zero_distance():
    # distance 0 is allowed (not negative)
    assert extra_distance_fare("mini", 0, "city", False) == 0

def test_within_included_distance():
    # sedan includes 8 km, so 5 km has no extra fare
    assert extra_distance_fare("sedan", 5, "city", False) == 0

def test_exactly_included_distance():
    # extra = 0, so fare is 0
    assert extra_distance_fare("sedan", 8, "city", False) == 0

def test_subscriber_gets_extra_km_city():
    # mini = 5 + 3 = 8 km included, extra = 2 km at 12
    assert extra_distance_fare("mini", 10, "city", True) == 24

def test_non_subscriber_city():
    # mini = 5 km included, extra = 5 km at 12
    assert extra_distance_fare("mini", 10, "city", False) == 60

def test_subscriber_suv_gets_no_bonus():
    # suv does not get the +3 km even for subscribers
    # included = 12, extra = 3 km at 18 (not city)
    assert extra_distance_fare("suv", 15, "suburb", True) == 54

def test_non_city_short_trip():
    # sedan = 8 km included, extra = 2 km at 18
    assert extra_distance_fare("sedan", 10, "outstation", False) == 36

def test_extra_exactly_20():
    # extra = 20 is not > 20, so normal city rate 12
    assert extra_distance_fare("mini", 25, "city", False) == 240

def test_long_city_trip():
    # extra = 25 (> 20) in city: rate = 12 + 8 = 20, no outstation charge
    assert extra_distance_fare("mini", 30, "city", False) == 500

def test_long_outstation_trip():
    # suv includes 12 km, extra = 25 km, rate = 18 + 8 + 4 = 30
    assert extra_distance_fare("suv", 37, "outstation", False) == 750

def test_long_suburb_trip():
    # extra = 25 (> 20), not city and not outstation: rate = 18 + 8 = 26
    assert extra_distance_fare("sedan", 33, "suburb", False) == 650


# ---------- seats_and_bags_ok ----------

def test_wheelchair_ok():
    assert seats_and_bags_ok(2, 0, True) is True

def test_wheelchair_too_many_passengers():
    assert seats_and_bags_ok(3, 0, True) is False

def test_too_many_passengers():
    assert seats_and_bags_ok(5, 1, False) is False

def test_four_passengers_allowed():
    assert seats_and_bags_ok(4, 2, False) is True

def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True

def test_too_many_bags():
    assert seats_and_bags_ok(2, 3, False) is False


# ---------- pickup_status ----------

def test_scheduled_on_time():
    # cutoff = 10
    assert pickup_status(12, True, False) == "on_time"

def test_scheduled_exactly_cutoff():
    assert pickup_status(10, True, False) == "on_time"

def test_scheduled_delayed():
    # cutoff = 10, delayed if >= -5
    assert pickup_status(-5, True, False) == "delayed"

def test_scheduled_airport_on_time():
    # cutoff = 10 + 10 = 20
    assert pickup_status(20, True, True) == "on_time"

def test_scheduled_airport_missed():
    # cutoff = 20, delayed needs >= 5
    assert pickup_status(4, True, True) == "missed"

def test_unscheduled_on_time():
    # cutoff = 5
    assert pickup_status(5, False, False) == "on_time"

def test_airport_delayed():
    # cutoff = 5 + 10 = 15, delayed if >= 0
    assert pickup_status(3, False, True) == "delayed"

def test_unscheduled_delayed_boundary():
    # cutoff = 5, 5 - 15 = -10
    assert pickup_status(-10, False, False) == "delayed"

def test_missed_pickup():
    assert pickup_status(-20, False, False) == "missed"
