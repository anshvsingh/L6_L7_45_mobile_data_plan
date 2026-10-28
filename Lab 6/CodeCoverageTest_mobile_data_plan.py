"""Lab 6 - Code (line) coverage tests for mobile_data_plan.py
SRN: PES1UG24AM046   Name: Ansh Vardhan Singh
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

def test_loyal_basic_gets_bonus_gb():
    assert overage_charge("basic", 5, False, True) == 30

def test_non_roaming_overage():
    assert overage_charge("standard", 8, False, False) == 45

def test_roaming_overage():
    assert overage_charge("basic", 4, True, False) == 80

def test_heavy_overage_non_roaming():
    assert overage_charge("basic", 14, False, False) == 300

def test_heavy_overage_roaming():
    assert overage_charge("basic", 14, True, False) == 660


# ---------- recharge_allowed ----------
def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True

def test_recharge_kyc_pending_within_limit():
    assert recharge_allowed(200, 0, True) is True

def test_recharge_kyc_pending_over_limit():
    assert recharge_allowed(201, 0, True) is False

def test_recharge_amount_too_high():
    assert recharge_allowed(2001, 0, False) is False

def test_recharge_too_many_pending():
    assert recharge_allowed(500, 3, False) is False


# ---------- validity_status ----------
def test_validity_active():
    assert validity_status(10, True, False) == "active"

def test_validity_grace():
    assert validity_status(1, False, False) == "grace"

def test_validity_expired():
    assert validity_status(-20, True, False) == "expired"

def test_validity_with_addon():
    assert validity_status(1, True, True) == "grace"
