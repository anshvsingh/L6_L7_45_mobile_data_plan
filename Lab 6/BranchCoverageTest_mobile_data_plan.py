"""Lab 6 - Branch coverage tests for mobile_data_plan.py
SRN: PES1UG24AM046   Name: Ansh Vardhan Singh
Every decision is driven to both True and False, including boundary values.
"""
import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


# ---------- overage_charge ----------
def test_within_included_data():
    assert overage_charge("standard", 3, False, False) == 0

def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 3, False, False)

def test_negative_usage_raises():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)

def test_zero_usage_is_valid():
    # data_gb < 0 False branch at boundary
    assert overage_charge("basic", 0, False, False) == 0

def test_loyal_basic_gets_bonus_gb():
    # is_loyal True and plan != premium True
    assert overage_charge("basic", 5, False, True) == 30

def test_loyal_premium_no_bonus():
    # is_loyal True but plan == premium -> bonus skipped; 12 - 10 = 2 * 15
    assert overage_charge("premium", 12, False, True) == 30

def test_not_loyal_no_bonus():
    # is_loyal False -> bonus skipped
    assert overage_charge("standard", 8, False, False) == 45

def test_exactly_included_is_free():
    # extra == 0 -> extra <= 0 True
    assert overage_charge("standard", 5, False, False) == 0

def test_loyal_exactly_at_boosted_limit_is_free():
    assert overage_charge("basic", 3, False, True) == 0

def test_one_over_included_is_charged():
    # extra == 1 -> extra <= 0 False
    assert overage_charge("standard", 6, False, False) == 15

def test_roaming_overage():
    assert overage_charge("basic", 4, True, False) == 80

def test_extra_exactly_10_no_surcharge_non_roaming():
    # extra == 10 -> extra > 10 False
    assert overage_charge("basic", 12, False, False) == 150

def test_extra_exactly_10_no_surcharge_roaming():
    assert overage_charge("basic", 12, True, False) == 400

def test_heavy_overage_non_roaming():
    # extra 11 -> rate 15 + 10
    assert overage_charge("basic", 13, False, False) == 275

def test_heavy_overage_roaming():
    # extra 12 -> rate 40 + 10 + 5
    assert overage_charge("basic", 14, True, False) == 660


# ---------- recharge_allowed ----------
def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True

def test_recharge_kyc_pending_at_limit():
    assert recharge_allowed(200, 0, True) is True

def test_recharge_kyc_pending_over_limit():
    assert recharge_allowed(201, 0, True) is False

def test_recharge_amount_at_max():
    # amount > 2000 False at boundary
    assert recharge_allowed(2000, 0, False) is True

def test_recharge_amount_too_high():
    assert recharge_allowed(2001, 0, False) is False

def test_recharge_pending_at_limit():
    assert recharge_allowed(500, 2, False) is True

def test_recharge_too_many_pending():
    assert recharge_allowed(500, 3, False) is False


# ---------- validity_status ----------
def test_prepaid_active_at_cutoff():
    # prepaid cutoff 0; days_left >= 0
    assert validity_status(0, True, False) == "active"

def test_postpaid_active():
    assert validity_status(3, False, False) == "active"

def test_postpaid_grace():
    assert validity_status(2, False, False) == "grace"

def test_postpaid_grace_lower_boundary():
    # cutoff 3 -> grace down to -12
    assert validity_status(-12, False, False) == "grace"

def test_postpaid_expired():
    assert validity_status(-13, False, False) == "expired"

def test_prepaid_expired():
    assert validity_status(-16, True, False) == "expired"

def test_prepaid_with_addon_active():
    # cutoff 0 + 2 = 2
    assert validity_status(2, True, True) == "active"

def test_prepaid_with_addon_grace():
    assert validity_status(1, True, True) == "grace"

def test_postpaid_with_addon_active():
    # cutoff 3 + 2 = 5
    assert validity_status(5, False, True) == "active"

def test_postpaid_with_addon_expired():
    # cutoff 5 -> grace down to -10
    assert validity_status(-11, False, True) == "expired"
