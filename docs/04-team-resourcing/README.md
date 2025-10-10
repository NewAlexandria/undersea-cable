---
layout: default
title: "Team & Resourcing"
description: "Team size and resourcing plans for scaling the DAS platform"
---

# Team & Resourcing

This section addresses Section 4 of the [INTERNAL_DECISION_QUESTIONS.md](../INTERNAL_DECISION_QUESTIONS.md): How many people, what roles, when hired?

## Key Team Areas

### Multi-Cloud Services Design Team

- Platform architects
- DevOps/SRE engineers
- Security engineers
- **Critical skills**: Kubernetes, Terraform, Docker, CI/CD

### Edge/Hardware Team

- Hardware design/procurement
- Installation/deployment field engineers
- Support/maintenance engineers
- **Scaling**: Team size at 5, 15, 30 cables

### Signal Processing & ML Team

- Signal processing experts (FFT, compression)
- ML/classification engineers
- Computer vision engineers
- **Expertise needed**: Acoustic signal processing, marine classification

### Data Engineering Team

- Streaming data engineers (Kafka, Kinesis)
- Batch data engineers (Spark, data lake)
- Data infrastructure engineers
- **Scaling trigger**: Add engineer per X cables?

## Budget Constraints

From [INTERNAL_DECISION_QUESTIONS.md](../INTERNAL_DECISION_QUESTIONS.md#45-overall-team-budget):

**Series A funding fit**:

- \$10M total Series A
- Engineering budget (30%): \$3M for 18 months
- ~15-20 engineers average
- Sufficient for: Multi-cloud (3), edge (4), ML (4), data (3), product (3) = 17 engineers

## Key Decisions

- Build vs hire vs outsource for each team?
- What's the hiring priority sequence?
- Engineering vs non-engineering split?

## Relationship to Other Sections

- **Previous**: [03-partner-engagement](../03-partner-engagement/) - Partners may reduce team needs
- **Next**: [05-cost-metrics](../05-cost-metrics/) - Team costs are major expense
- **Related**: [02-architectural-decisions](../02-architectural-decisions/) - Architecture drives team structure
