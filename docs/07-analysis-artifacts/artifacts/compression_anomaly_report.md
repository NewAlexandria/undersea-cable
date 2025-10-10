# Compression Anomaly Analysis Report

## Executive Summary

**Total Files Analyzed:** 906

**Anomalous Files:** 123 (13.6%)

### Key Findings

#### Hypothesis Validation

We investigated whether files with unusual compression ratios contain more interesting event data.

**Standard Deviation Comparison:**
- Anomalous files: 5.662
- Normal (low compression ~8): 2.161
- Normal (high compression ~14): 1.574

**Dynamic Range Comparison:**
- Anomalous files: 71.352
- Normal (low compression ~8): 34.581
- Normal (high compression ~14): 27.742

✓ **HYPOTHESIS SUPPORTED:** Anomalous compression files show higher variability, suggesting more complex/interesting signals.

## Detailed Analysis

### Compression Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| anomaly_low | 119 | 13.1% |
| anomaly_mid | 4 | 0.4% |
| normal_high | 348 | 38.4% |
| normal_low | 435 | 48.0% |

### Statistical Properties by Category

| Category | Count | Avg Compression | Avg Std Dev | Avg Dynamic Range | Signal Complexity |
|----------|-------|-----------------|-------------|-------------------|-------------------|
| anomaly_low | 119 | 5.38 | 5.742 | 72.328 | 1.106 |
| anomaly_mid | 4 | 10.56 | 3.279 | 42.321 | 0.310 |
| normal_high | 348 | 14.58 | 1.574 | 27.742 | 0.108 |
| normal_low | 435 | 8.25 | 2.161 | 34.581 | 0.270 |

## Recommendations

1. **PRIORITIZE TRANSMISSION** of files with compression ratios outside 7-9 and 13-15 ranges
2. **IMPLEMENT FILTERING**: Focus bandwidth on anomalous compression files
3. **REAL-TIME MONITORING**: Use compression ratio as a proxy for event detection

## Visualizations

See accompanying PNG files:
- `compression_vs_properties.png` - Scatter plots of compression vs data properties
- `distribution_comparison.png` - Histograms comparing categories
- `category_boxplots.png` - Box plots of key metrics
- `temporal_pattern.png` - Time series of compression factors

## Files of Interest

See `interesting_files.json` for specific file paths to investigate.
