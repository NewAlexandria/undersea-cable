---
layout: default
title: "Project Context for LLMs"
description: "Structured context about the DAS Maritime Surveillance project optimized for LLM consumption"
---

# Project Context: DAS Maritime Surveillance Platform

## Project Overview

**What**: Transform submarine fiber optic cables into a global maritime surveillance network using Distributed Acoustic Sensing (DAS)

**Why**: 
- 1000x faster vessel detection than satellites
- 10x lower cost than existing solutions
- Global coverage through 500+ existing cables

**How**: 
- DAS technology converts fiber into 15,000+ acoustic sensors
- Edge processing with selective compression
- Cloud-based ML for vessel classification

## Technical Foundation

### Core Technology
- **DAS (Distributed Acoustic Sensing)**: Uses laser interrogation to detect vibrations along fiber optic cables
- **Data Volume**: 20-500 TB/day per cable
- **Sampling**: 8-10 kHz, 15,000 channels per cable

### Key Innovation
- **Compression-First Strategy**: 6-10x lossy compression at edge preserves 97% of vessel information
- **Information Theory Validated**: 2.9/3.0 bits preserved for vessel detection
- **Cost Optimization**: CPU-only edge ($30-40k) vs GPU edge ($150-200k)

## Business Model

### Market
- **Size**: $3.2B maritime security market, 7.3% CAGR
- **Segments**: Ports, Coast Guard, Environmental agencies, Research institutions

### Revenue Model
- Subscription-based per cable
- Tiered pricing by features
- Target: $1M ARR per cable at scale

### Competitive Advantage
- Real-time detection (vs satellite delays)
- Persistent monitoring (24/7 coverage)
- Multi-use data (vessels, earthquakes, marine life)

## Current Status

### Technical Validation
- ✓ Information theory analysis complete
- ✓ Monte Carlo simulations validate compression
- ✓ Architecture options documented
- ⏳ Real-world data validation needed

### Business Development
- ⏳ Series A funding preparation
- ⏳ Lighthouse customer identification
- ⏳ Partnership strategy development

## Key Decisions Pending

### Technical
1. Edge architecture: Option B (Regional DC) vs Option C (Cloud-only)
2. Compression thresholds: ε=0.1 vs ε=0.5
3. Multi-cable correlation requirements

### Business
1. Initial target segment prioritization
2. Partnership vs direct sales model
3. Geographic market entry sequence

## File Organization

The repository is organized around [INTERNAL_DECISION_QUESTIONS.md](../INTERNAL_DECISION_QUESTIONS.md) with 87 critical questions across 7 areas:

1. **Technical Validation** - Proving feasibility
2. **Architectural Scale** - Infrastructure decisions
3. **Partner Engagement** - Strategic relationships
4. **Team Resourcing** - Hiring and scaling
5. **Cost Metrics** - Financial tracking
6. **Business Strategy** - Market approach
7. **Analysis Artifacts** - Supporting evidence

## Key Relationships

### Technical Dependencies
- Compression fidelity → Architecture choice
- Architecture choice → Cost structure
- Cost structure → Pricing model

### Business Dependencies
- Customer latency requirements → Architecture
- Partnership model → Go-to-market strategy
- Team size → Series A funding needs

## Success Metrics

### Technical
- Detection accuracy: >99%
- False positive rate: <1%
- Processing latency: <3 seconds
- System uptime: >99.9%

### Business
- Cost per cable: <$50k/month
- Gross margin: >60%
- Customer acquisition: 3 cables Year 1
- ARR growth: 10x Year 2

## Risk Factors

### Technical Risks
- Compression may lose critical information
- Multi-cable correlation complexity
- Real-time processing at scale

### Business Risks
- Long sales cycles (6-18 months)
- Regulatory approvals needed
- Competition from established players

---

*This context document provides LLMs with essential project understanding for assisting with technical decisions, business strategy, and development planning.*
