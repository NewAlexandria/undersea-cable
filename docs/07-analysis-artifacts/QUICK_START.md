# Quick Start Guide

## TL;DR - Just Run This

```bash
cd /Users/zak/src/undersea-cable
source .venv/bin/activate

# Analyze HDF5 structure and patterns
python analysis/hdf5_analyze_all.py das24_data/20240506/dphi

# Run compression analysis (now with error handling)
python analysis/das24_analyze_compress.py --input das24_data/20240506/dphi --threads 4
```

## What You Get

### From `hdf5_analyze_all.py`:

```
analysis/artifacts/
├── hdf5_metadata_index.json          # Complete metadata index
└── visualizations/
    ├── pattern1_array_sizes.png      # Array size variations
    ├── pattern2_scalar_values.png    # Scalar attribute changes
    ├── pattern5_tree_structures.txt  # File structure trees
    └── additional_patterns_report.txt # Statistics & best practices
```

### From `das24_analyze_compress.py`:

```
analysis/
├── artifacts/
│   ├── stats.csv                     # Compression statistics
│   └── hist_*.png                    # Data histograms
├── outputs/
│   ├── *.dasp                        # Compressed files
│   └── daspack_compressed.h5         # Aggregated compressed data
└── RESULTS.md                        # Human-readable results
```

## Common Commands

```bash
# Activate environment
source .venv/bin/activate

# Quick structure analysis (3 files for testing)
python analysis/hdf5_analyze_all.py das24_data/20240506/dphi --limit 3

# Full structure analysis
python analysis/hdf5_analyze_all.py das24_data/20240506/dphi

# Compression analysis with error handling
python analysis/das24_analyze_compress.py \
    --input das24_data/20240506/dphi \
    --threads 4 \
    --uniform-steps 0.5 0.1

# Force rescan (ignore existing index)
python analysis/hdf5_analyze_all.py das24_data --force

# Scan only (no visualization)
python analysis/hdf5_analyze_all.py das24_data --scan-only

# Visualize only (no scanning)
python analysis/hdf5_analyze_all.py --visualize-only
```

## View Results

```bash
# View file structures
cat analysis/artifacts/visualizations/pattern5_tree_structures.txt

# View array size variations
cat analysis/artifacts/visualizations/pattern1_array_sizes_report.txt

# View compression results
cat analysis/RESULTS.md

# View statistics
cat analysis/artifacts/visualizations/additional_patterns_report.txt

# Open visualizations
open analysis/artifacts/visualizations/pattern1_array_sizes.png
open analysis/artifacts/visualizations/file_size_distribution.png
```

## Troubleshooting

### "Metadata file not found"

```bash
# Run scanner first
python analysis/hdf5_metadata_scanner.py das24_data/20240506/dphi
```

### "Directory already scanned"

```bash
# Use --force to rescan
python analysis/hdf5_analyze_all.py das24_data --force
```

### Truncated file errors

The scripts now handle these automatically - they'll skip bad files and continue.

### Import errors

```bash
# Reinstall dependencies
pip install h5py numpy pandas matplotlib tqdm

# Reinstall DASPack
cd daspack && maturin develop --release && cd ..
```

## What's New

### Fixed Issues ✅

1. **ERROR_1 (Truncated HDF5)**: Now handled gracefully with error logging
2. **Crash on bad files**: Script continues processing other files

### New Tools ✅

1. **hdf5_metadata_scanner.py**: Build persistent metadata index
2. **hdf5_metadata_visualizer.py**: Generate pattern visualizations
3. **hdf5_analyze_all.py**: Combined scan + visualize pipeline

### New Features ✅

1. Incremental scanning (only new files)
2. Pattern detection (array sizes, scalar values, strings)
3. Tree structure visualization
4. Compression/chunking analysis
5. File size distribution
6. Best practices recommendations

## Next Steps

1. **Explore your data**:

   ```bash
   python analysis/hdf5_analyze_all.py das24_data/20240506/dphi
   cat analysis/artifacts/visualizations/pattern5_tree_structures.txt
   ```

2. **Review patterns**:

   ```bash
   cat analysis/artifacts/visualizations/pattern1_array_sizes_report.txt
   cat analysis/artifacts/visualizations/additional_patterns_report.txt
   ```

3. **Run compression**:

   ```bash
   python analysis/das24_analyze_compress.py --input das24_data/20240506/dphi --threads 4
   ```

4. **Check results**:
   ```bash
   cat analysis/RESULTS.md
   cat analysis/artifacts/stats.csv
   ```

## Documentation

- **Full guide**: `HDF5_ANALYSIS_README.md`
- **Solution details**: `SOLUTION_SUMMARY.md`
- **Analysis plan**: `ANALYSIS_PLAN.md`



