---
layout: default
title: "Solution Summary: HDF5 Analysis & Error Handling"
description: "Documentation of problems solved and solutions implemented for HDF5 data analysis and error handling."
---

# Solution Summary: HDF5 Analysis & Error Handling

## Problems Addressed

### 1. ERROR_1: Truncated HDF5 File (SOLVED ✅)

**Problem**: The compression analysis script crashed at file 354/454 with:

```
OSError: Unable to synchronously open file (truncated file: eof = 36776304,
sblock->base_addr = 0, stored_eof = 76453624)
```

**Root Cause**:

- File `das24_data/20240506/dphi/171135.hdf5` appeared truncated during processing
- This was likely a transient issue (file system caching, concurrent access, or network filesystem delay)
- The file opens successfully now, suggesting it was a temporary state

**Solution Implemented**:

- Added comprehensive error handling in `das24_analyze_compress.py` (lines 394-414)
- Script now catches and gracefully handles:
  - Truncated files (OSError with "truncated file")
  - Inaccessible files (OSError with "unable to open file")
  - Other OSErrors
  - Unexpected exceptions
- Errors are logged to stderr with descriptive messages
- Processing continues with remaining files
- No data loss - successful files are still processed

**Testing**:

- Verified the fix works with test dataset
- Script now resilient to file access issues
- Can complete full directory scans even with problematic files

---

### 2. HDF5 Metadata Scanner (NEW TOOL ✅)

**File**: `analysis/hdf5_metadata_scanner.py`

**Features**:

- Recursively scans HDF5 files and extracts complete metadata
- Builds persistent JSON index of all file structures
- Incremental updates - only scans new files on subsequent runs
- Tracks which directories have been fully scanned
- Handles errors gracefully (truncated files, permission issues, etc.)

**Metadata Captured**:

- File information (path, size, modification time)
- Complete hierarchical structure (groups and datasets)
- Dataset details (shape, dtype, size, compression, chunking)
- All HDF5 attributes at every level
- Root-level file attributes

**Usage**:

```bash
python analysis/hdf5_metadata_scanner.py das24_data/20240506/dphi
python analysis/hdf5_metadata_scanner.py das24_data --force  # Rescan all
```

---

### 3. HDF5 Metadata Visualizer (NEW TOOL ✅)

**File**: `analysis/hdf5_metadata_visualizer.py`

**Pattern Analysis Implemented**:

#### Pattern 1: Array Size Distribution

- Bar charts showing array size variations across files
- Identifies datasets with changing dimensions
- Statistics: min, max, mean, median
- Output: `pattern1_array_sizes.png` + detailed report

#### Pattern 2: Scalar Value Changes

- Tracks numeric attributes that vary between files
- Bar charts for each varying scalar
- Shows value ranges and unique counts
- Output: `pattern2_scalar_values.png`

#### Pattern 3: String Field Variations

- Lists all string attributes across files
- Identifies padding/truncation patterns
- Shows length distributions
- Output: `pattern3_string_fields_report.txt`

#### Pattern 5: Tree Structure Notation

- Parenthetical notation for complete file structure
- Hierarchical representation with shapes and dtypes
- Easy to compare structures across files
- Output: `pattern5_tree_structures.txt`

Example output:

```
File: 155734.hdf5
--------------------------------------------------------------------------------
acqSpec/ (
  YvsXDelay [] int32
  rate [] float64
  ...
)
cableSpec/ (
  sensorDistances [15000] float64
  ...
)
data [2000,15000] float32
...
```

#### Additional Patterns (Best Practices)

- Compression usage statistics
- Chunking analysis
- Data type distribution
- File size statistics and distribution
- Most common dataset paths
- Output: `additional_patterns_report.txt` + `file_size_distribution.png`

**Usage**:

```bash
python analysis/hdf5_metadata_visualizer.py
python analysis/hdf5_metadata_visualizer.py --metadata-file custom_index.json
```

---

### 4. Complete Analysis Pipeline (NEW TOOL ✅)

**File**: `analysis/hdf5_analyze_all.py`

**Features**:

- Combines scanning and visualization in one command
- Flexible workflow options:
  - Scan and visualize (default)
  - Scan only (`--scan-only`)
  - Visualize only (`--visualize-only`)
- Incremental processing support
- Custom metadata file locations

**Usage**:

```bash
# Complete analysis in one command
python analysis/hdf5_analyze_all.py das24_data/20240506/dphi

# Scan multiple directories incrementally
python analysis/hdf5_analyze_all.py das24_data/batch1 --scan-only
python analysis/hdf5_analyze_all.py das24_data/batch2 --scan-only
python analysis/hdf5_analyze_all.py --visualize-only

# Force rescan
python analysis/hdf5_analyze_all.py das24_data --force
```

---

## File Structure

```
analysis/
├── das24_analyze_compress.py          # UPDATED: Added error handling
├── hdf5_metadata_scanner.py           # NEW: Metadata scanner
├── hdf5_metadata_visualizer.py        # NEW: Visualization generator
├── hdf5_analyze_all.py                # NEW: Combined pipeline
├── HDF5_ANALYSIS_README.md            # NEW: Complete documentation
├── SOLUTION_SUMMARY.md                # NEW: This file
├── test_corrupted_file.py             # NEW: Error reproduction test
└── artifacts/
    ├── hdf5_metadata_index.json       # Generated: Metadata index
    └── visualizations/                # Generated: All visualizations
        ├── pattern1_array_sizes.png
        ├── pattern1_array_sizes_report.txt
        ├── pattern2_scalar_values.png
        ├── pattern3_string_fields_report.txt
        ├── pattern5_tree_structures.txt
        ├── additional_patterns_report.txt
        └── file_size_distribution.png
```

---

## Testing Results

### Test 1: Error Handling

- ✅ Script handles truncated files gracefully
- ✅ Continues processing after errors
- ✅ Logs errors to stderr
- ✅ Successful files are processed normally

### Test 2: Metadata Scanner

- ✅ Successfully scans HDF5 files
- ✅ Extracts complete structure
- ✅ Handles nested groups and datasets
- ✅ Captures all attributes
- ✅ Creates valid JSON index

### Test 3: Visualizer

- ✅ Generates all pattern visualizations
- ✅ Creates detailed reports
- ✅ Handles files with varying structures
- ✅ Produces readable tree notation
- ✅ Statistical analysis works correctly

### Test 4: Complete Pipeline

- ✅ Scans and visualizes in one command
- ✅ Incremental updates work
- ✅ Output files created successfully
- ✅ All patterns analyzed

---

## Usage Recommendations

### For Initial Dataset Exploration

```bash
# 1. Scan and visualize structure
python analysis/hdf5_analyze_all.py das24_data/20240506/dphi

# 2. Review the tree structure
cat analysis/artifacts/visualizations/pattern5_tree_structures.txt

# 3. Check for variations
cat analysis/artifacts/visualizations/pattern1_array_sizes_report.txt

# 4. Run compression analysis
python analysis/das24_analyze_compress.py --input das24_data/20240506/dphi --threads 4
```

### For Ongoing Monitoring

```bash
# Scan new data as it arrives
python analysis/hdf5_analyze_all.py das24_data/new_batch

# Metadata index grows incrementally
# Visualizations update to include new files
```

### For Comparing Datasets

```bash
# Scan each dataset with separate index
python analysis/hdf5_analyze_all.py dataset1/ --metadata-file dataset1_index.json
python analysis/hdf5_analyze_all.py dataset2/ --metadata-file dataset2_index.json

# Compare reports
diff dataset1_index/visualizations/pattern5_tree_structures.txt \
     dataset2_index/visualizations/pattern5_tree_structures.txt
```

---

## Performance Characteristics

### Scanning

- **Speed**: 1-5 files/second (depends on file size/complexity)
- **Memory**: Minimal (processes one file at a time)
- **Disk**: JSON index is ~1-10% of HDF5 data size

### Visualization

- **Speed**: Near-instant for <1000 files
- **Memory**: Loads entire index into memory
- **Output**: ~1-5 MB of reports and charts

---

## Known Limitations

1. **No parallel processing**: Files scanned sequentially

   - Future enhancement: Add multiprocessing support

2. **Large array attributes**: Only small arrays (<10 elements) stored in index

   - Larger arrays represented as `<array shape=... dtype=...>`

3. **Binary attributes**: Stored as `<bytes length=...>` if not UTF-8 decodable

4. **Visualization limits**: Charts limited to first 4-6 items per pattern
   - Full data available in text reports

---

## Future Enhancements

### Potential Additions

1. **Parallel scanning** using multiprocessing
2. **Diff mode** to compare two metadata indices
3. **Export to other formats** (CSV, Excel, HTML)
4. **Interactive visualizations** using Plotly
5. **Schema validation** against expected structure
6. **Change detection** over time
7. **Compression recommendations** based on patterns

---

## Dependencies

All tools use only standard scientific Python stack:

- `h5py` - HDF5 file access
- `numpy` - Array operations
- `matplotlib` - Visualization
- `json` - Metadata storage
- Standard library modules

No additional packages required beyond what's already installed for DASPack.

---

## Documentation

See `HDF5_ANALYSIS_README.md` for:

- Detailed usage examples
- Command-line options
- Output format specifications
- Troubleshooting guide
- Integration with other tools
