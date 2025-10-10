---
layout: default
title: "Latency Requirements Validation"
description: "Questions and validation approach for real-time processing latency requirements"
---

# Latency Requirements Validation

## Real-time Processing Architecture

**Critical Questions**:

- Can you achieve sub-second latency for anomaly detection?
- What was the GPU/TPU strategy for real-time FFT processing?
- How did you handle processing failures without data loss?

**Follow-ups**:

- Edge vs. cloud processing split?
- Batch size optimization strategies?
- Memory management for continuous streams?

## Compress-First vs. Vectorize-First Architecture

**The Core Question**:

```
Strategy A: Vectorize-First (FFT at edge before compression)
- GPU at edge → FFT → Features → Compress → Cloud
- Pros: Sub-second latency, preserves all signal content
- Cons: $150-200k edge cost, complex edge systems

Strategy B: Compress-First (Compress then FFT in cloud/datacenter)
- CPU at edge → DASPack compress → Cloud/DC → GPU FFT
- Pros: $30-40k edge cost, flexible algorithms
- Cons: 1-30 second latency, potential signal loss

Which would a company like Google use, and why?
```

**Information Theory Questions**:

- Does lossy compression (6-10x) destroy vessel signature information?
- What's the minimum bits/sample needed to detect vessels reliably?
- Can you recover frequency domain features from compressed time-domain data?
- At what error threshold (0.1, 0.5, 1.0) does vessel detection degrade?

**Practical Experience**:

- Did you validate that compressed data retains detection accuracy?
- Lossless vs. lossy compression trade-offs?
- Was there a "sweet spot" compression ratio that preserved all useful info?

## Latency Requirements by Use Case

**Questions**:

- What were the latency requirements for your applications?
- Edge autonomy vs. cost trade-offs?
- At what scale does regional datacenter make sense?
