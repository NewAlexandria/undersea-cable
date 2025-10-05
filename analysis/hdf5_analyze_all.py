#!/usr/bin/env python3
"""
HDF5 Complete Analysis Pipeline

Combines scanning and visualization in one convenient script.
"""

import argparse
import sys
from pathlib import Path

# Import our modules
from hdf5_metadata_scanner import HDF5MetadataScanner
from hdf5_metadata_visualizer import HDF5MetadataVisualizer


def main():
    parser = argparse.ArgumentParser(
        description="Complete HDF5 analysis: scan and visualize",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a directory and generate visualizations
  python hdf5_analyze_all.py das24_data/20240506/dphi

  # Force rescan and use custom metadata file
  python hdf5_analyze_all.py das24_data --force --metadata-file my_index.json

  # Only visualize existing metadata (skip scanning)
  python hdf5_analyze_all.py --visualize-only --metadata-file artifacts/hdf5_metadata_index.json
        """,
    )
    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        help="Directory to scan for HDF5 files (not needed if --visualize-only)",
    )
    parser.add_argument(
        "--metadata-file",
        type=str,
        default="analysis/artifacts/hdf5_metadata_index.json",
        help="Path to metadata index file (default: analysis/artifacts/hdf5_metadata_index.json)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rescan of all files, even if already indexed",
    )
    parser.add_argument(
        "--extensions",
        type=str,
        nargs="+",
        default=[".h5", ".hdf5"],
        help="File extensions to scan (default: .h5 .hdf5)",
    )
    parser.add_argument(
        "--scan-only", action="store_true", help="Only scan files, skip visualization"
    )
    parser.add_argument(
        "--visualize-only",
        action="store_true",
        help="Only generate visualizations from existing metadata",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.visualize_only and not args.input:
        parser.error("input directory is required unless --visualize-only is specified")

    metadata_file = Path(args.metadata_file)

    # Step 1: Scan (unless visualize-only)
    if not args.visualize_only:
        print("=" * 80)
        print("STEP 1: SCANNING HDF5 FILES")
        print("=" * 80)

        input_dir = Path(args.input)
        if not input_dir.exists():
            print(f"Error: Directory not found: {input_dir}", file=sys.stderr)
            return 1

        if not input_dir.is_dir():
            print(f"Error: Not a directory: {input_dir}", file=sys.stderr)
            return 1

        # Create scanner and scan
        scanner = HDF5MetadataScanner(metadata_file)
        extensions = set(args.extensions)
        scanned_count = scanner.scan_directory(
            input_dir, force=args.force, extensions=extensions
        )
        scanner.save_metadata()

        print(f"\n✅ Scan complete!")
        print(f"   Files scanned: {scanned_count}")
        print(f"   Total files in index: {len(scanner.metadata['files'])}")
        print(f"   Metadata file: {metadata_file}")

    # Step 2: Visualize (unless scan-only)
    if not args.scan_only:
        print("\n" + "=" * 80)
        print("STEP 2: GENERATING VISUALIZATIONS")
        print("=" * 80)

        if not metadata_file.exists():
            print(f"Error: Metadata file not found: {metadata_file}", file=sys.stderr)
            print("Run with a directory argument first to scan files", file=sys.stderr)
            return 1

        visualizer = HDF5MetadataVisualizer(metadata_file)
        visualizer.generate_all_visualizations()

        print(f"\n✅ Visualizations complete!")
        print(f"   Output directory: {visualizer.output_dir}")

    print("\n" + "=" * 80)
    print("COMPLETE!")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())



