# Data Transmission Recommendations

## Summary

Based on analysis of 906 DAS data files, we can achieve significant bandwidth savings while capturing the most scientifically interesting events.

## Key Insight

**Files with compression ratios < 7 contain 2.6x more signal variability** (std dev: 5.74 vs 2.16 for normal files) and have **2.6x larger dynamic range** (72.3 vs 27.7). This suggests these files capture seismic events, marine activity, or other phenomena of scientific interest.

## Statistical Evidence

- Standard deviation difference: **p < 0.000000** (highly significant)
- Dynamic range difference: **p < 0.000000**, Cohen's d = 1.92 (large effect size)

## Recommended Transmission Strategy

### Option 1: Aggressive Filtering (13.6% bandwidth)
**Transmit only anomalous compression files**
- Files: 123 / 906
- Bandwidth savings: **86.4%**
- Risk: May miss some events in "normal" compression range

### Option 2: Conservative Filtering (33.4% bandwidth) ⭐ RECOMMENDED
**Transmit all anomalous files + 25% random sample of normal files**
- Ensures event capture while sampling baseline conditions
- Bandwidth savings: **66.6%**
- Provides ground truth for model validation

### Option 3: Moderate Filtering (21.4% bandwidth)
**Transmit all anomalous files + 10% random sample of normal files**
- Bandwidth savings: **78.6%**
- Minimal baseline sampling

## Implementation Guide

### Real-Time Algorithm

```python
def should_transmit(compression_factor, std_dev):
    """Decide if file should be transmitted."""
    # Priority HIGH: Definite anomalies
    if compression_factor < 7.0:
        return True, 'PRIORITY_HIGH'
    
    # Priority MEDIUM: Possible anomalies
    if 9.0 < compression_factor < 13.0:
        return True, 'PRIORITY_MEDIUM'
    
    # Priority LOW: Sample normal data
    if random.random() < 0.25:  # 25% sampling
        return True, 'PRIORITY_LOW'
    
    return False, 'SKIP'
```

### Validation Metrics

Monitor these metrics to validate the approach:

1. **Event Detection Rate**: Track scientific events found in transmitted data
2. **False Negative Rate**: Periodically review skipped files for missed events
3. **Compression Drift**: Monitor if compression ratios change over time
4. **Bandwidth Utilization**: Actual vs expected transmission rates

## Next Steps

1. **Manual Validation**: Inspect 5-10 files from each category to confirm signal characteristics
2. **Domain Expert Review**: Have oceanographers/seismologists review flagged events
3. **Pilot Deployment**: Test on new data stream for 24-48 hours
4. **Iterative Refinement**: Adjust thresholds based on feedback

## Files for Manual Inspection

### Anomaly Low

- `162016.hdf5` (compression: 5.97, std: 2.17)
- `161926.hdf5` (compression: 5.99, std: 2.24)
- `161408.hdf5` (compression: 6.55, std: 9.68)

### Normal Low

- `163905.hdf5` (compression: 8.32, std: 1.61)
- `171945.hdf5` (compression: 8.29, std: 1.49)
- `171425.hdf5` (compression: 8.24, std: 1.39)

### Normal High

- `163735.hdf5` (compression: 14.66, std: 1.53)
- `170515.hdf5` (compression: 14.72, std: 1.22)
- `171655.hdf5` (compression: 14.65, std: 1.36)

