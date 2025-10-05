# HDF5 Analysis Tools

Comprehensive toolkit for analyzing, indexing, and visualizing HDF5 file structures and metadata.

## Overview

This toolkit provides three main components:

1. **Metadata Scanner** (`hdf5_metadata_scanner.py`) - Recursively scans HDF5 files and builds a persistent JSON index
2. **Metadata Visualizer** (`hdf5_metadata_visualizer.py`) - Analyzes patterns and generates visualizations from the metadata
3. **Complete Pipeline** (`hdf5_analyze_all.py`) - Combines scanning and visualization in one command

## Quick Start

### Scan and Visualize in One Command

```bash
# Scan a directory and generate all visualizations
python analysis/hdf5_analyze_all.py das24_data/20240506/dphi

# Use custom metadata file location
python analysis/hdf5_analyze_all.py das24_data --metadata-file my_index.json

# Force rescan of all files (even if already indexed)
python analysis/hdf5_analyze_all.py das24_data --force
```

### Individual Tools

```bash
# 1. Scan files only (no visualization)
python analysis/hdf5_metadata_scanner.py das24_data/20240506/dphi

# 2. Visualize existing metadata only (no scanning)
python analysis/hdf5_metadata_visualizer.py --metadata-file analysis/artifacts/hdf5_metadata_index.json

# Or use the combined tool with flags
python analysis/hdf5_analyze_all.py das24_data --scan-only
python analysis/hdf5_analyze_all.py --visualize-only --metadata-file artifacts/hdf5_metadata_index.json
```

## Features

### Persistent Metadata Index

The scanner creates a JSON index that stores:

- **File metadata**: path, size, modification time
- **Structure tree**: complete hierarchy of groups and datasets
- **Dataset details**: shape, dtype, size, compression, chunking
- **Attributes**: all HDF5 attributes at every level
- **Incremental updates**: only scans new files on subsequent runs

### Pattern Analysis & Visualizations

The visualizer generates comprehensive reports and charts:

#### Pattern 1: Array Size Distribution

- Bar charts showing how array sizes vary across files
- Identifies datasets that change size between files
- Statistics: min, max, mean sizes

#### Pattern 2: Scalar Value Changes

- Tracks numeric attributes that vary across files
- Bar charts showing value distributions
- Useful for finding configuration differences

#### Pattern 3: String Field Variations

- Lists all string attributes and their variations
- Identifies padding or truncation patterns
- Shows length distributions

#### Pattern 5: Tree Structure Notation

- Parenthetical notation showing complete file structure
- Easy-to-read hierarchical representation
- Includes shapes and dtypes

#### Additional Patterns & Best Practices

- Compression usage statistics
- Chunking analysis
- Data type distribution
- File size statistics
- Common dataset paths across files

## Output Structure

```
analysis/
├── artifacts/
│   ├── hdf5_metadata_index.json      # Persistent metadata index
│   └── visualizations/               # Generated visualizations
│       ├── pattern1_array_sizes.png
│       ├── pattern1_array_sizes_report.txt
│       ├── pattern2_scalar_values.png
│       ├── pattern3_string_fields_report.txt
│       ├── pattern5_tree_structures.txt
│       ├── additional_patterns_report.txt
│       └── file_size_distribution.png
```

## Metadata Index Format

The JSON index has this structure:

```json
{
  "version": "1.0",
  "created": "2025-10-04T12:00:00",
  "last_updated": "2025-10-04T12:30:00",
  "scanned_directories": [
    "/path/to/scanned/dir1",
    "/path/to/scanned/dir2"
  ],
  "files": {
    "/path/to/file1.h5": {
      "file_path": "/path/to/file1.h5",
      "file_name": "file1.h5",
      "file_size": 123456789,
      "modified_time": "2025-10-04T10:00:00",
      "scanned_time": "2025-10-04T12:00:00",
      "root_attributes": {...},
      "structure": {
        "dataset1": {
          "type": "dataset",
          "path": "dataset1",
          "shape": [1000, 2000],
          "dtype": "float32",
          "size": 2000000,
          "attributes": {...}
        },
        "group1": {
          "type": "group",
          "path": "group1",
          "attributes": {...},
          "children": {...}
        }
      }
    }
  }
}
```

## Advanced Usage

### Incremental Scanning

The scanner tracks which directories have been fully scanned. On subsequent runs, it only processes new files:

```bash
# First scan
python analysis/hdf5_analyze_all.py das24_data/batch1

# Later, scan a new directory - previous data is preserved
python analysis/hdf5_analyze_all.py das24_data/batch2

# Force rescan everything
python analysis/hdf5_analyze_all.py das24_data --force
```

### Custom File Extensions

```bash
# Scan .hdf and .h5 files
python analysis/hdf5_analyze_all.py data_dir --extensions .hdf .h5
```

### Working with Large Datasets

For large datasets (1000+ files), consider:

1. **Scan in batches** by subdirectory
2. **Use --scan-only** to defer visualization
3. **Generate visualizations separately** when convenient

```bash
# Scan multiple directories incrementally
python analysis/hdf5_analyze_all.py das24_data/dir1 --scan-only
python analysis/hdf5_analyze_all.py das24_data/dir2 --scan-only
python analysis/hdf5_analyze_all.py das24_data/dir3 --scan-only

# Generate visualizations once
python analysis/hdf5_analyze_all.py --visualize-only
```

## Error Handling

The scanner gracefully handles:

- **Truncated files**: Skips with warning
- **Corrupted files**: Skips with error message
- **Permission errors**: Skips inaccessible files
- **Invalid HDF5**: Skips non-HDF5 files

All errors are logged to stderr while continuing to process other files.

## Integration with Compression Analysis

The HDF5 analysis tools complement the compression analysis script:

```bash
# 1. Analyze HDF5 structure first
python analysis/hdf5_analyze_all.py das24_data/20240506/dphi

# 2. Review the structure and patterns
cat analysis/artifacts/visualizations/pattern5_tree_structures.txt

# 3. Run compression analysis with appropriate parameters
python analysis/das24_analyze_compress.py --input das24_data/20240506/dphi --threads 4
```

## Troubleshooting

### "Metadata file not found"

Run the scanner first:

```bash
python analysis/hdf5_metadata_scanner.py your_data_directory
```

### "Directory already scanned"

Use `--force` to rescan:

```bash
python analysis/hdf5_analyze_all.py your_data_directory --force
```

### Visualization errors

Ensure matplotlib is installed:

```bash
pip install matplotlib
```

## Performance Tips

- **Scanning speed**: ~1-5 files/second depending on file size and complexity
- **Memory usage**: Minimal - processes one file at a time
- **Disk usage**: JSON index is typically 1-10% of total HDF5 data size
- **Parallelization**: Not currently parallelized (processes files sequentially)

## Examples

### Example 1: Quick Analysis of New Dataset

```bash
python analysis/hdf5_analyze_all.py new_dataset/
# Review outputs in analysis/artifacts/visualizations/
```

### Example 2: Compare Two Dataset Versions

```bash
# Scan version 1
python analysis/hdf5_analyze_all.py data_v1/ --metadata-file v1_index.json

# Scan version 2
python analysis/hdf5_analyze_all.py data_v2/ --metadata-file v2_index.json

# Compare the generated reports
diff v1_index/visualizations/pattern5_tree_structures.txt \
     v2_index/visualizations/pattern5_tree_structures.txt
```

### Example 3: Monitor Dataset Growth

```bash
# Initial scan
python analysis/hdf5_analyze_all.py monitoring_dir/

# Later, add new files and rescan
python analysis/hdf5_analyze_all.py monitoring_dir/ --force

# Compare file counts and sizes in additional_patterns_report.txt
```

## See Also

- `das24_analyze_compress.py` - DASPack compression analysis
- `ANALYSIS_PLAN.md` - Overall analysis strategy
- `RESULTS.md` - Compression analysis results
