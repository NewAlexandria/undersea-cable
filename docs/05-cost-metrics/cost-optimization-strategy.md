---
layout: default
title: "Cost Optimization Strategy"
description: "Cost optimization strategies and validation questions for DAS platform"
---

# Cost Optimization Strategy

## Proposed Tiering

```yaml
# Proposed tiering
data_tiers:
  realtime:
    retention: 24h
    sampling: full
    cost_per_tb: $100

  nearline:
    retention: 7d
    sampling: 10x_downsample
    cost_per_tb: $20

  archive:
    retention: 1y
    sampling: events_only
    cost_per_tb: $4
```

**Get Feedback On**: Optimal retention/sampling trade-offs?

## Key Cost Questions

- What was the storage architecture for hot/warm/cold data?
- Cost optimization methods that worked at scale?
- What's the realistic cost per TB target we should aim for?

## Cost per TB Target

Our target: <\$10/TB/month - is this realistic at scale?
