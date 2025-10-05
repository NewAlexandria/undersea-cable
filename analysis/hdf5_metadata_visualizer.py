#!/usr/bin/env python3
"""
HDF5 Metadata Visualizer

Analyzes and visualizes patterns in HDF5 metadata collected by hdf5_metadata_scanner.py

Patterns analyzed:
1. Array size distribution across files
2. Scalar value changes across files
3. String field variations (padding/truncation)
4. File structure trees in parenthetical notation
5. Common HDF5 patterns and best practices
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend
import numpy as np


class HDF5MetadataVisualizer:
    """Visualizes patterns in HDF5 metadata."""

    def __init__(self, metadata_file: Path):
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()
        self.output_dir = metadata_file.parent / "visualizations"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from file."""
        if not self.metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_file}")

        with open(self.metadata_file, "r") as f:
            return json.load(f)

    def _traverse_structure(
        self, structure: Dict[str, Any], callback, path: str = "", level: int = 0
    ):
        """Recursively traverse HDF5 structure and call callback for each item."""
        for name, item in structure.items():
            current_path = f"{path}/{name}" if path else name
            callback(name, item, current_path, level)

            if item.get("type") == "group" and "children" in item:
                self._traverse_structure(
                    item["children"], callback, current_path, level + 1
                )

    def pattern1_array_sizes(self):
        """Pattern 1: Array size distribution across files."""
        print("\n=== Pattern 1: Array Size Distribution ===")

        # Collect array sizes by dataset path
        array_sizes = defaultdict(list)  # path -> [(file, shape, size)]

        def collect_arrays(name, item, path, level):
            if item.get("type") == "dataset":
                shape = tuple(item.get("shape", []))
                size = item.get("size", 0)
                if len(shape) > 0:  # Only arrays, not scalars
                    array_sizes[path].append(
                        {
                            "file": item.get("file_path", "unknown"),
                            "shape": shape,
                            "size": size,
                            "dtype": item.get("dtype", "unknown"),
                        }
                    )

        for file_path, file_meta in self.metadata["files"].items():
            structure = file_meta.get("structure", {})
            self._traverse_structure(structure, collect_arrays)

        # Create visualizations for arrays that appear in multiple files
        multi_file_arrays = {
            path: data for path, data in array_sizes.items() if len(data) > 1
        }

        print(f"Found {len(array_sizes)} unique array paths")
        print(f"  {len(multi_file_arrays)} appear in multiple files")

        if not multi_file_arrays:
            print("No arrays found in multiple files")
            return

        # Create bar charts for top varying arrays
        fig, axes = plt.subplots(
            min(4, len(multi_file_arrays)),
            1,
            figsize=(12, 4 * min(4, len(multi_file_arrays))),
        )
        if len(multi_file_arrays) == 1:
            axes = [axes]

        for idx, (path, data) in enumerate(list(multi_file_arrays.items())[:4]):
            ax = axes[idx] if len(multi_file_arrays) > 1 else axes[0]

            # Extract sizes and file names
            sizes = [d["size"] for d in data]
            file_names = [Path(d["file"]).name for d in data]

            # Create bar chart
            x_pos = np.arange(len(sizes))
            ax.bar(x_pos, sizes, color="steelblue", alpha=0.7)
            ax.set_xlabel("File Index")
            ax.set_ylabel("Array Size (elements)")
            ax.set_title(f"Array Size Variation: {path}\n({len(data)} files)")
            ax.grid(axis="y", alpha=0.3)

            # Add statistics
            if len(sizes) > 0:
                stats_text = f"Min: {min(sizes):,} | Max: {max(sizes):,} | Mean: {np.mean(sizes):,.0f}"
                ax.text(
                    0.02,
                    0.98,
                    stats_text,
                    transform=ax.transAxes,
                    verticalalignment="top",
                    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
                )

        plt.tight_layout()
        output_file = self.output_dir / "pattern1_array_sizes.png"
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved: {output_file}")

        # Save detailed report
        report_file = self.output_dir / "pattern1_array_sizes_report.txt"
        with open(report_file, "w") as f:
            f.write("Array Size Distribution Report\n")
            f.write("=" * 80 + "\n\n")

            for path, data in sorted(multi_file_arrays.items()):
                f.write(f"\nPath: {path}\n")
                f.write(f"  Files: {len(data)}\n")
                sizes = [d["size"] for d in data]
                shapes = [str(d["shape"]) for d in data]
                f.write(f"  Size range: {min(sizes):,} - {max(sizes):,}\n")
                f.write(f"  Unique shapes: {len(set(shapes))}\n")
                if len(set(shapes)) <= 5:
                    f.write(f"  Shapes: {', '.join(set(shapes))}\n")

        print(f"  Saved: {report_file}")

    def pattern2_scalar_values(self):
        """Pattern 2: Scalar value changes across files."""
        print("\n=== Pattern 2: Scalar Value Changes ===")

        # Collect scalar attributes
        scalar_attrs = defaultdict(list)  # path.attr_name -> [values]

        def collect_scalars(name, item, path, level):
            attrs = item.get("attributes", {})
            for attr_name, attr_value in attrs.items():
                # Check if scalar (not array or string)
                if isinstance(attr_value, (int, float)) and not isinstance(
                    attr_value, bool
                ):
                    key = f"{path}.{attr_name}"
                    scalar_attrs[key].append(attr_value)

        for file_path, file_meta in self.metadata["files"].items():
            structure = file_meta.get("structure", {})
            self._traverse_structure(structure, collect_scalars)

            # Also check root attributes
            for attr_name, attr_value in file_meta.get("root_attributes", {}).items():
                if isinstance(attr_value, (int, float)) and not isinstance(
                    attr_value, bool
                ):
                    scalar_attrs[f"ROOT.{attr_name}"].append(attr_value)

        # Find scalars that vary
        varying_scalars = {
            k: v for k, v in scalar_attrs.items() if len(set(v)) > 1 and len(v) > 1
        }

        print(f"Found {len(scalar_attrs)} scalar attributes")
        print(f"  {len(varying_scalars)} vary across files")

        if not varying_scalars:
            print("No varying scalar values found")
            return

        # Create visualizations
        n_plots = min(6, len(varying_scalars))
        fig, axes = plt.subplots(n_plots, 1, figsize=(12, 4 * n_plots))
        if n_plots == 1:
            axes = [axes]

        for idx, (attr_path, values) in enumerate(list(varying_scalars.items())[:6]):
            ax = axes[idx]

            # Create bar chart
            x_pos = np.arange(len(values))
            ax.bar(x_pos, values, color="coral", alpha=0.7)
            ax.set_xlabel("File Index")
            ax.set_ylabel("Value")
            ax.set_title(f"Scalar Value Variation: {attr_path}\n({len(values)} files)")
            ax.grid(axis="y", alpha=0.3)

            # Add statistics
            stats_text = f"Min: {min(values):.3g} | Max: {max(values):.3g} | Unique: {len(set(values))}"
            ax.text(
                0.02,
                0.98,
                stats_text,
                transform=ax.transAxes,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
            )

        plt.tight_layout()
        output_file = self.output_dir / "pattern2_scalar_values.png"
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved: {output_file}")

    def pattern3_string_fields(self):
        """Pattern 3: String field variations (padding/truncation)."""
        print("\n=== Pattern 3: String Field Variations ===")

        # Collect string attributes
        string_attrs = defaultdict(list)  # path.attr_name -> [values]

        def collect_strings(name, item, path, level):
            attrs = item.get("attributes", {})
            for attr_name, attr_value in attrs.items():
                if isinstance(attr_value, str) and not attr_value.startswith("<"):
                    key = f"{path}.{attr_name}"
                    string_attrs[key].append(attr_value)

        for file_path, file_meta in self.metadata["files"].items():
            structure = file_meta.get("structure", {})
            self._traverse_structure(structure, collect_strings)

            # Also check root attributes
            for attr_name, attr_value in file_meta.get("root_attributes", {}).items():
                if isinstance(attr_value, str) and not attr_value.startswith("<"):
                    string_attrs[f"ROOT.{attr_name}"].append(attr_value)

        print(f"Found {len(string_attrs)} string attributes")

        # Analyze for padding/truncation
        report_file = self.output_dir / "pattern3_string_fields_report.txt"
        with open(report_file, "w") as f:
            f.write("String Field Variations Report\n")
            f.write("=" * 80 + "\n\n")

            for attr_path, values in sorted(string_attrs.items()):
                if len(set(values)) > 1:  # Only varying strings
                    f.write(f"\nAttribute: {attr_path}\n")
                    f.write(f"  Files: {len(values)}\n")
                    f.write(f"  Unique values: {len(set(values))}\n")

                    # Check for padding patterns
                    lengths = [len(v) for v in values]
                    f.write(f"  Length range: {min(lengths)} - {max(lengths)}\n")

                    # Show unique values (limit to 10)
                    unique_vals = list(set(values))[:10]
                    f.write(f"  Sample values:\n")
                    for val in unique_vals:
                        f.write(f"    '{val}' (len={len(val)})\n")

                    if len(set(values)) > 10:
                        f.write(f"    ... and {len(set(values)) - 10} more\n")

        print(f"  Saved: {report_file}")

    def pattern5_tree_structures(self):
        """Pattern 5: Parenthetical notation for file structures."""
        print("\n=== Pattern 5: File Structure Trees ===")

        def structure_to_notation(structure: Dict[str, Any], indent: int = 0) -> str:
            """Convert structure to parenthetical notation."""
            lines = []
            for name, item in sorted(structure.items()):
                item_type = item.get("type", "unknown")

                if item_type == "dataset":
                    shape = item.get("shape", [])
                    dtype = item.get("dtype", "?")
                    shape_str = f"[{','.join(map(str, shape))}]" if shape else "[]"
                    lines.append(f"{'  ' * indent}{name} {shape_str} {dtype}")
                elif item_type == "group":
                    lines.append(f"{'  ' * indent}{name}/ (")
                    if "children" in item:
                        child_notation = structure_to_notation(
                            item["children"], indent + 1
                        )
                        lines.append(child_notation)
                    lines.append(f"{'  ' * indent})")
                else:
                    lines.append(f"{'  ' * indent}{name} <{item_type}>")

            return "\n".join(lines)

        # Generate tree for each file
        output_file = self.output_dir / "pattern5_tree_structures.txt"
        with open(output_file, "w") as f:
            f.write("HDF5 File Structure Trees\n")
            f.write("=" * 80 + "\n\n")

            for file_path, file_meta in sorted(self.metadata["files"].items()):
                f.write(f"\nFile: {Path(file_path).name}\n")
                f.write(f"Path: {file_path}\n")
                f.write(f"Size: {file_meta.get('file_size', 0):,} bytes\n")
                f.write("-" * 80 + "\n")

                structure = file_meta.get("structure", {})
                notation = structure_to_notation(structure)
                f.write(notation)
                f.write("\n\n")

        print(f"  Saved: {output_file}")

    def additional_patterns(self):
        """Additional pattern analysis and best practices."""
        print("\n=== Additional Patterns & Best Practices ===")

        # Collect statistics
        stats = {
            "total_files": len(self.metadata["files"]),
            "compression_usage": 0,
            "chunked_datasets": 0,
            "total_datasets": 0,
            "dtype_distribution": Counter(),
            "file_sizes": [],
            "common_paths": Counter(),
        }

        def analyze_item(name, item, path, level):
            if item.get("type") == "dataset":
                stats["total_datasets"] += 1
                if item.get("compression"):
                    stats["compression_usage"] += 1
                if item.get("chunks"):
                    stats["chunked_datasets"] += 1
                stats["dtype_distribution"][item.get("dtype", "unknown")] += 1
                stats["common_paths"][path] += 1

        for file_path, file_meta in self.metadata["files"].items():
            structure = file_meta.get("structure", {})
            self._traverse_structure(structure, analyze_item)
            stats["file_sizes"].append(file_meta.get("file_size", 0))

        # Generate report
        report_file = self.output_dir / "additional_patterns_report.txt"
        with open(report_file, "w") as f:
            f.write("Additional Patterns & Best Practices Report\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"Total Files: {stats['total_files']}\n")
            f.write(f"Total Datasets: {stats['total_datasets']}\n")
            f.write(
                f"Compression Usage: {stats['compression_usage']}/{stats['total_datasets']} "
                f"({100*stats['compression_usage']/max(1,stats['total_datasets']):.1f}%)\n"
            )
            f.write(
                f"Chunked Datasets: {stats['chunked_datasets']}/{stats['total_datasets']} "
                f"({100*stats['chunked_datasets']/max(1,stats['total_datasets']):.1f}%)\n"
            )

            f.write(f"\nFile Size Statistics:\n")
            if stats["file_sizes"]:
                f.write(f"  Min: {min(stats['file_sizes']):,} bytes\n")
                f.write(f"  Max: {max(stats['file_sizes']):,} bytes\n")
                f.write(f"  Mean: {np.mean(stats['file_sizes']):,.0f} bytes\n")
                f.write(f"  Median: {np.median(stats['file_sizes']):,.0f} bytes\n")

            f.write(f"\nData Type Distribution:\n")
            for dtype, count in stats["dtype_distribution"].most_common(10):
                f.write(
                    f"  {dtype}: {count} ({100*count/stats['total_datasets']:.1f}%)\n"
                )

            f.write(f"\nMost Common Dataset Paths:\n")
            for path, count in stats["common_paths"].most_common(10):
                f.write(f"  {path}: {count} files\n")

        print(f"  Saved: {report_file}")

        # Create visualization for file sizes
        if stats["file_sizes"]:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

            # Histogram
            ax1.hist(
                stats["file_sizes"],
                bins=30,
                color="green",
                alpha=0.7,
                edgecolor="black",
            )
            ax1.set_xlabel("File Size (bytes)")
            ax1.set_ylabel("Frequency")
            ax1.set_title("File Size Distribution")
            ax1.grid(axis="y", alpha=0.3)

            # Box plot
            ax2.boxplot(stats["file_sizes"], vert=True)
            ax2.set_ylabel("File Size (bytes)")
            ax2.set_title("File Size Box Plot")
            ax2.grid(axis="y", alpha=0.3)

            plt.tight_layout()
            output_file = self.output_dir / "file_size_distribution.png"
            plt.savefig(output_file, dpi=150, bbox_inches="tight")
            plt.close()
            print(f"  Saved: {output_file}")

    def generate_all_visualizations(self):
        """Generate all visualizations and reports."""
        print(f"\nGenerating visualizations from: {self.metadata_file}")
        print(f"Output directory: {self.output_dir}")

        self.pattern1_array_sizes()
        self.pattern2_scalar_values()
        self.pattern3_string_fields()
        self.pattern5_tree_structures()
        self.additional_patterns()

        print(f"\n✅ All visualizations complete!")
        print(f"   Output directory: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Visualize patterns in HDF5 metadata")
    parser.add_argument(
        "--metadata-file",
        type=str,
        default="analysis/artifacts/hdf5_metadata_index.json",
        help="Path to metadata index file",
    )

    args = parser.parse_args()

    metadata_file = Path(args.metadata_file)
    if not metadata_file.exists():
        print(f"Error: Metadata file not found: {metadata_file}", file=sys.stderr)
        print(
            "Run hdf5_metadata_scanner.py first to generate metadata", file=sys.stderr
        )
        return 1

    visualizer = HDF5MetadataVisualizer(metadata_file)
    visualizer.generate_all_visualizations()

    return 0


if __name__ == "__main__":
    sys.exit(main())
