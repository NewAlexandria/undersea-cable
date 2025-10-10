---
layout: default
title: "Cost Metrics & Dashboards"
description: "Platform cost metrics, dashboards, and optimization strategies"
---

# Cost Metrics & Dashboards

This section addresses Section 5 of the [INTERNAL_DECISION_QUESTIONS.md](../INTERNAL_DECISION_QUESTIONS.md): What do we track and what are our targets?

## Key Areas

### Cost Metrics

- Cost per cable per month: Target \$X
- Cost per TB processed: Target \$Y
- Cost per vessel detection: Target \$Z
- Gross margin per cable: Target X%

### Cost Structure

```
Total Cost per Cable
├── Edge Infrastructure
│   ├── Hardware (amortized)
│   ├── Power & Cooling
│   ├── Bandwidth
│   └── Maintenance
├── Cloud/Datacenter Compute
│   ├── FFT Processing
│   ├── ML Inference
│   ├── Data Storage
│   └── Network egress
└── Personnel (allocated)
```

### Optimization Strategy

- **[cost-optimization-strategy.md](./cost-optimization-strategy.md)** - Tiered storage and optimization approaches

## Dashboard Requirements

From [INTERNAL_DECISION_QUESTIONS.md](../INTERNAL_DECISION_QUESTIONS.md#52-cost-dashboard-requirements):

**Dashboards needed**:

- Executive: Total cost, cost per cable, gross margin (monthly)
- Engineering: Cloud costs by service, utilization (daily)
- Operations: Edge costs, bandwidth, outages (real-time)
- Finance: P&L by segment, unit economics (monthly)

## Cost Targets by Phase

- Phase 1 (5 cables): Accept higher costs
- Phase 2 (15 cables): 20% cost reduction
- Phase 3 (30 cables): 40% cost reduction

## Relationship to Other Sections

- **Previous**: [04-team-resourcing](../04-team-resourcing/) - Team costs are major component
- **Next**: [06-business-strategy](../06-business-strategy/) - Cost drives pricing strategy
- **Related**: [02-architectural-decisions](../02-architectural-decisions/) - Architecture determines costs
