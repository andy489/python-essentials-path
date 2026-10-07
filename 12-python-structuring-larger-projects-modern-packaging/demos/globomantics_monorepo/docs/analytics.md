# Analytics Service

The `globomantics_analytics` package is responsible for:

- Computing customer loyalty tiers
- Aggregating shipment metrics
- Powering dashboards and reports

## Public API

Example function:

```python
from globomantics_analytics.tiering import assign_tier

tier = assign_tier(total_spend=12000, shipments=48)
print(tier)  # e.g., "GOLD"
