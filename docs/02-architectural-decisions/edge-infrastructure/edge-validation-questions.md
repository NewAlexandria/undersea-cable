---
layout: default
title: "Edge Infrastructure Validation Questions"
description: "Questions for validating edge infrastructure architecture decisions"
---

# Edge Infrastructure Validation Questions

## Validate Our Approach

```
Option A (GPU at Edge): 2x NVIDIA DGX A100 per cable site
- Cost: $150-200k
- Latency: <1 second
- Is this over/under-provisioned?

Option B (CPU at Edge + Regional GPU): Dual Xeon/EPYC
- Cost: $30-40k per edge
- Latency: 1-3 seconds
- Centralized GPU processing serving 10-20 cables

Option C (CPU + Cloud only):
- Cost: $30-40k per edge
- Latency: 5-30 seconds
- All FFT/ML in cloud

Questions:
- What were the latency requirements for your applications?
- Edge autonomy vs. cost trade-offs?
- At what scale does regional datacenter make sense?
```

## Network Architecture

**Key Decisions**:

```
Our Plan: 100GbE with QUIC for events, S3 for bulk
- Bandwidth sizing accurate?
- Protocol recommendations?
- Network reliability strategies?
```

## Data Compression & Storage

**Critical Questions**:

- Beyond DASPack, what compression strategies worked at scale?
- How did you balance compression ratio vs. signal fidelity?
- What was the storage architecture for hot/warm/cold data?

**Specific Techniques**:

- Adaptive compression based on signal content?
- Distributed storage strategies?
- Cost optimization methods?

## System Reliability

**Questions**:

- What were the common failure modes?
- How did you achieve 99.9%+ uptime?
- Disaster recovery strategies?

**Specific Scenarios**:

- Power outages at cable landing stations
- Fiber cuts affecting backhaul
- Interrogator hardware failures

## Monitoring & Alerting

**Questions**:

- Key metrics to track?
- Early warning indicators?
- Automation strategies that worked?

## Scaling Operations

**Questions**:

- How did you manage 10 → 100 cables operationally?
- Remote management strategies?
- Team structure recommendations?
