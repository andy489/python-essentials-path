from globomantics_platform.analytics.tiering import compute_tier


def test_compute_tier_boundaries():
    assert compute_tier(0) == "bronze"
    assert compute_tier(499.99) == "bronze"
    assert compute_tier(500) == "silver"
    assert compute_tier(2000) == "gold"
    assert compute_tier(5000) == "platinum"
