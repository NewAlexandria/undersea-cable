# Marine Cable DAS Data Analysis & Maritime Surveillance Architecture

## Overview

Distributed Acoustic Sensing (DAS) on marine cables converts fiber optic cables into arrays of thousands of seismic sensors. This repository includes data analysis tools and complete technical/business architecture for maritime surveillance applications.

## Hypothesis: Compression-Based Event Detection (Oct 2025)

Compression ratio could serve as a real-time event detector, enabling **62-86% bandwidth reduction** while maintaining useful data capture.

- **Files with compression < 7 contain 2.6x more signal variability** (p < 0.000001, n=906)
- **13% of files contain most interesting events**
- See [COMPRESSION_EVENT_DETECTION_SUMMARY.md](./COMPRESSION_EVENT_DETECTION_SUMMARY.md)
- **Potential savings**: \$8M+/year per site in satellite bandwidth costs

See [analysis/artifacts/QUICK_REFERENCE.md](./analysis/artifacts/QUICK_REFERENCE.md) LLM suggestions.

## HDF5 Format

Hierarchical Data Format 5 - scientific data container supporting:

- Large datasets with compression
- Metadata and attributes
- Multi-dimensional arrays
- Cross-platform compatibility

## Architecture Documentation

**Quick Start**: See [ARCHITECTURE_DECISION_SUMMARY.md](./ARCHITECTURE_DECISION_SUMMARY.md) for choosing between CPU/GPU architectures.

### Technical Architecture

- **[DAS_MARITIME_ARCHITECTURE.md](./DAS_MARITIME_ARCHITECTURE.md)** - GPU-at-edge system architecture
- **[DAS_CPU_ARCHITECTURE_ALTERNATIVE.md](./DAS_CPU_ARCHITECTURE_ALTERNATIVE.md)** - CPU-based compress-first strategy (cost-optimized)
- **[DAS_TECHNICAL_IMPLEMENTATION.md](./DAS_TECHNICAL_IMPLEMENTATION.md)** - Implementation details

### Analysis & Strategy

- **[INFORMATION_THEORY_ANALYSIS.md](./INFORMATION_THEORY_ANALYSIS.md)** - Compression vs. vectorization trade-offs
- **[analysis/COMPRESSION_EVENT_DETECTION.md](./analysis/COMPRESSION_EVENT_DETECTION.md)** - Event detection via compression ratio
- **[DAS_BUSINESS_STRATEGY.md](./DAS_BUSINESS_STRATEGY.md)** - Market analysis and business model
- **[GOOGLE_ENGINEER_DISCUSSION_GUIDE.md](./GOOGLE_ENGINEER_DISCUSSION_GUIDE.md)** - Technical validation questions

### Key Findings

**CPU vs GPU at Edge**: Modeling shows lossy compression (6-10x) preserves >97% of potential vessel detection information. CPU-based compression at edge with GPU processing in regional datacenters provides:

- **Cost savings**: \$150-250k per site
- **Flexibility**: Can reprocess with new algorithms
- **Acceptable latency**: 1-3 seconds vs. <1 second

**Compression-Based Event Detection** (Oct 2025): Analysis of 906 files shows that compression ratio is a proxy for event detection:

- **Files with compression < 7 contain 2.6x more signal variability** (p < 0.000001)
- **83% bandwidth savings possible** by transmitting only anomalous compression files
- **Strong correlates**: Higher std dev, dynamic range, and absolute range predict interesting events
- **Recommendation**: Implement real-time filtering to transmit compression < 7 files + 25% baseline sample
- See: `analysis/artifacts/compression_anomaly_report.md` and `transmission_recommendations.md`

## Tools

### `daspack/`

Data compression library for DAS datasets. Implements controlled compression algorithms to reduce storage while preserving scientific integrity.

### `OOI_DAS_2024/`

Jupyter notebook for analyzing Ocean Observatories Initiative DAS data from 2024. Includes visualization and processing workflows.

### `scrape_hdf5_files.sh`

Automated scraper for downloading HDF5 files from OOI DAS data server (`piweb.ooirsn.uw.edu/das24/data/`). Maintains directory structure and handles resume/retry.

## Data Source

Ocean Observatories Initiative Regional Cabled Array - distributed acoustic sensing data from submarine cables.

## Context

![DASPack LinkedIn Post](daspack-linkedin-post.png)
