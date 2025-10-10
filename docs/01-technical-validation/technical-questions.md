---
layout: default
title: "Technical Validation Questions"
description: "Key technical questions for validating DAS maritime surveillance technology"
---

# Technical Validation Questions

## new unsorted questions

- do we have existing vessel FFT data?It seems that we do. Is this company IP, or is it public research?
- Is there a limited number of vessels that have been detected with this method, and we need to expand that research?
- Do we know anything about the length of time to develop accurate models for any given vessel?
- Do we know if there's an obvious source of data for other kinds of marine signals? Like whales, landslides, etc?
- What can you tell me about the structure of a partnership deal? What format is data sent from their device? What kind of hardware actually collects the data and transformed it into a data stream? What type of chip or computer is it? Do we know things about performance, in a typical operational sense?

## Scale & Performance Insights

**Critical Questions**:

- What marine acoustic data throughputs do we see from large cable operators, like Google?
- Does managing large cable data volumes, like 200-500 TB/day, scale with the marine data?
- What were the bottlenecks at scale across many cables, and how do you overcome them?

**Why It Matters**: Understanding Google-scale solutions will help us architect for 100+ cables from day one.

## DAS-Specific Challenges

**Critical Questions**:

- How did you handle interrogator failures/glitches?
- What were the unique challenges of optical phase data vs. traditional sensors?
- How did you calibrate for environmental noise (currents, temperature)?

**Technical Deep-Dives**:

- Coherent noise removal techniques
- Channel-to-channel correlation methods
- Spatial-temporal filtering approaches

## Machine Learning & Signal Processing

### Vessel Classification

**Questions**:

- What features were most discriminative for vessel types?
- How did you handle overlapping vessel signatures?
- Training data collection strategies?

**Our Approach Validation**:

- CNN-LSTM hybrid architecture
- Spectrogram-based classification
- Transfer learning from sonar data

### Anomaly Detection

**Questions**:

- Baseline establishment methods?
- Seasonal/tidal adjustment techniques?
- False positive reduction strategies?

### Multi-Cable Fusion

**Questions**:

- How did you correlate detections across cables?
- Time synchronization strategies?
- Position estimation accuracy achievable?

## Key Metrics to Validate

From experience, what should our targets be?

- **Detection Accuracy**: Our target: >99%
- **False Positive Rate**: Our target: <1%
- **Processing Latency**: Our target: <1 second
- **Compression Ratio**: Our target: 6-10x
- **System Uptime**: Our target: >99.9%
- **Cost per TB**: Our target: <\$10/TB/month
