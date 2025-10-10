#!/usr/bin/env python3
"""
HDF5 Structure Comparator

Analyzes and compares HDF5 file structures to identify:
- Added/removed groups and datasets
- Changed dataset shapes, dtypes, or attributes
- Structural differences between files
- Evolution of file structure over time
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class HDF5StructureComparator:
    """Compares HDF5 file structures and identifies differences."""

    def __init__(self, metadata_file: Path):
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()
        self.output_dir = metadata_file.parent / "structure_analysis"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from file."""
        if not self.metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_file}")

        with open(self.metadata_file, "r") as f:
            return json.load(f)

    def _extract_structure_paths(
        self, structure: Dict[str, Any], prefix: str = ""
    ) -> Dict[str, Dict[str, Any]]:
        """Extract all paths and their properties from structure."""
        paths = {}

        for name, item in structure.items():
            current_path = f"{prefix}/{name}" if prefix else name

            if item.get("type") == "dataset":
                paths[current_path] = {
                    "type": "dataset",
                    "shape": item.get("shape", []),
                    "dtype": item.get("dtype", "unknown"),
                    "size": item.get("size", 0),
                    "attributes": item.get("attributes", {}),
                    "compression": item.get("compression"),
                    "chunks": item.get("chunks"),
                }
            elif item.get("type") == "group":
                paths[current_path] = {
                    "type": "group",
                    "attributes": item.get("attributes", {}),
                    "children_count": len(item.get("children", {})),
                }
                # Recursively extract children
                if "children" in item:
                    child_paths = self._extract_structure_paths(
                        item["children"], current_path
                    )
                    paths.update(child_paths)
            else:
                paths[current_path] = {
                    "type": item.get("type", "unknown"),
                    "error": item.get("error", "Unknown item type"),
                }

        return paths

    def _compare_structures(
        self, paths1: Dict[str, Dict[str, Any]], paths2: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare two structure dictionaries and return differences."""
        all_paths = set(paths1.keys()) | set(paths2.keys())

        differences = {
            "added": {},  # paths in paths2 but not in paths1
            "removed": {},  # paths in paths1 but not in paths2
            "changed": {},  # paths in both but with different properties
            "unchanged": {},  # paths in both with same properties
        }

        for path in all_paths:
            if path in paths1 and path not in paths2:
                differences["removed"][path] = paths1[path]
            elif path in paths2 and path not in paths1:
                differences["added"][path] = paths2[path]
            elif path in paths1 and path in paths2:
                if self._structures_equal(paths1[path], paths2[path]):
                    differences["unchanged"][path] = paths1[path]
                else:
                    differences["changed"][path] = {
                        "old": paths1[path],
                        "new": paths2[path],
                        "changes": self._get_property_changes(
                            paths1[path], paths2[path]
                        ),
                    }

        return differences

    def _structures_equal(
        self, struct1: Dict[str, Any], struct2: Dict[str, Any]
    ) -> bool:
        """Check if two structure items are equal."""
        if struct1.get("type") != struct2.get("type"):
            return False

        if struct1.get("type") == "dataset":
            return (
                struct1.get("shape") == struct2.get("shape")
                and struct1.get("dtype") == struct2.get("dtype")
                and struct1.get("attributes") == struct2.get("attributes")
            )
        elif struct1.get("type") == "group":
            return struct1.get("attributes") == struct2.get("attributes")

        return True

    def _get_property_changes(
        self, old: Dict[str, Any], new: Dict[str, Any]
    ) -> List[str]:
        """Get list of specific property changes between two structures."""
        changes = []

        if old.get("type") != new.get("type"):
            changes.append(f"type: {old.get('type')} → {new.get('type')}")

        if old.get("type") == "dataset" and new.get("type") == "dataset":
            if old.get("shape") != new.get("shape"):
                changes.append(f"shape: {old.get('shape')} → {new.get('shape')}")

            if old.get("dtype") != new.get("dtype"):
                changes.append(f"dtype: {old.get('dtype')} → {new.get('dtype')}")

            if old.get("size") != new.get("size"):
                changes.append(f"size: {old.get('size')} → {new.get('size')}")

            if old.get("compression") != new.get("compression"):
                changes.append(
                    f"compression: {old.get('compression')} → {new.get('compression')}"
                )

            if old.get("chunks") != new.get("chunks"):
                changes.append(f"chunks: {old.get('chunks')} → {new.get('chunks')}")

            # Compare attributes
            old_attrs = old.get("attributes", {})
            new_attrs = new.get("attributes", {})

            attr_changes = self._compare_attributes(old_attrs, new_attrs)
            changes.extend(attr_changes)

        elif old.get("type") == "group" and new.get("type") == "group":
            if old.get("children_count") != new.get("children_count"):
                changes.append(
                    f"children_count: {old.get('children_count')} → {new.get('children_count')}"
                )

            # Compare group attributes
            old_attrs = old.get("attributes", {})
            new_attrs = new.get("attributes", {})

            attr_changes = self._compare_attributes(old_attrs, new_attrs)
            changes.extend(attr_changes)

        return changes

    def _compare_attributes(
        self, old_attrs: Dict[str, Any], new_attrs: Dict[str, Any]
    ) -> List[str]:
        """Compare attributes between two structures."""
        changes = []

        all_attr_keys = set(old_attrs.keys()) | set(new_attrs.keys())

        for key in all_attr_keys:
            if key in old_attrs and key not in new_attrs:
                changes.append(f"attribute removed: {key}")
            elif key in new_attrs and key not in old_attrs:
                changes.append(f"attribute added: {key} = {new_attrs[key]}")
            elif key in old_attrs and key in new_attrs:
                if old_attrs[key] != new_attrs[key]:
                    changes.append(
                        f"attribute changed: {key} = {old_attrs[key]} → {new_attrs[key]}"
                    )

        return changes

    def generate_structure_comparison_report(self):
        """Generate comprehensive structure comparison report."""
        print("\n=== HDF5 Structure Comparison Analysis ===")

        files = list(self.metadata["files"].items())
        if len(files) < 2:
            print("Need at least 2 files to compare structures")
            return

        # Extract structures for all files
        file_structures = {}
        for file_path, file_meta in files:
            structure = file_meta.get("structure", {})
            file_structures[file_path] = self._extract_structure_paths(structure)

        # Generate pairwise comparisons
        comparison_results = []

        for i in range(len(files) - 1):
            file1_path, file1_meta = files[i]
            file2_path, file2_meta = files[i + 1]

            file1_name = Path(file1_path).name
            file2_name = Path(file2_path).name

            print(f"Comparing: {file1_name} → {file2_name}")

            paths1 = file_structures[file1_path]
            paths2 = file_structures[file2_path]

            differences = self._compare_structures(paths1, paths2)

            comparison_results.append(
                {
                    "file1": file1_name,
                    "file2": file2_name,
                    "file1_path": file1_path,
                    "file2_path": file2_path,
                    "differences": differences,
                }
            )

        # Generate detailed report
        self._write_comparison_report(comparison_results)

        # Generate summary statistics
        self._write_summary_statistics(comparison_results)

        # Generate structure evolution timeline
        self._write_evolution_timeline(file_structures)

        print(f"\n✅ Structure comparison complete!")
        print(f"   Output directory: {self.output_dir}")

    def _write_comparison_report(self, comparison_results: List[Dict[str, Any]]):
        """Write detailed comparison report."""
        report_file = self.output_dir / "structure_comparison_report.txt"

        with open(report_file, "w") as f:
            f.write("HDF5 Structure Comparison Report\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Total file pairs compared: {len(comparison_results)}\n\n")

            for result in comparison_results:
                f.write(f"\n{'='*80}\n")
                f.write(f"COMPARISON: {result['file1']} → {result['file2']}\n")
                f.write(f"{'='*80}\n\n")

                differences = result["differences"]

                # Check if there are any changes
                total_changes = (
                    len(differences["added"])
                    + len(differences["removed"])
                    + len(differences["changed"])
                )

                if total_changes == 0:
                    f.write("✅ No structural changes detected.\n\n")
                    continue

                # Summary counts
                f.write(f"Summary:\n")
                f.write(f"  Added: {len(differences['added'])} items\n")
                f.write(f"  Removed: {len(differences['removed'])} items\n")
                f.write(f"  Changed: {len(differences['changed'])} items\n")
                f.write(f"  Unchanged: {len(differences['unchanged'])} items\n\n")

                # Added items
                if differences["added"]:
                    f.write(f"ADDED ITEMS ({len(differences['added'])}):\n")
                    f.write("-" * 40 + "\n")
                    for path, item in sorted(differences["added"].items()):
                        f.write(f"  + {path}\n")
                        f.write(f"    Type: {item.get('type', 'unknown')}\n")
                        if item.get("type") == "dataset":
                            f.write(f"    Shape: {item.get('shape', [])}\n")
                            f.write(f"    Dtype: {item.get('dtype', 'unknown')}\n")
                            f.write(f"    Size: {item.get('size', 0):,}\n")
                        elif item.get("type") == "group":
                            f.write(f"    Children: {item.get('children_count', 0)}\n")
                        f.write("\n")

                # Removed items
                if differences["removed"]:
                    f.write(f"REMOVED ITEMS ({len(differences['removed'])}):\n")
                    f.write("-" * 40 + "\n")
                    for path, item in sorted(differences["removed"].items()):
                        f.write(f"  - {path}\n")
                        f.write(f"    Type: {item.get('type', 'unknown')}\n")
                        if item.get("type") == "dataset":
                            f.write(f"    Shape: {item.get('shape', [])}\n")
                            f.write(f"    Dtype: {item.get('dtype', 'unknown')}\n")
                        f.write("\n")

                # Changed items
                if differences["changed"]:
                    f.write(f"CHANGED ITEMS ({len(differences['changed'])}):\n")
                    f.write("-" * 40 + "\n")
                    for path, change_info in sorted(differences["changed"].items()):
                        f.write(f"  ~ {path}\n")
                        for change in change_info["changes"]:
                            f.write(f"    {change}\n")
                        f.write("\n")

                # Only show unchanged items if there are changes (to avoid clutter)
                if total_changes > 0 and differences["unchanged"]:
                    f.write(f"UNCHANGED ITEMS ({len(differences['unchanged'])}):\n")
                    f.write("-" * 40 + "\n")
                    unchanged_paths = sorted(differences["unchanged"].keys())
                    for path in unchanged_paths[:10]:  # Show first 10
                        f.write(f"  = {path}\n")
                    if len(unchanged_paths) > 10:
                        f.write(f"  ... and {len(unchanged_paths) - 10} more\n")
                    f.write("\n")

        print(f"  Saved: {report_file}")

    def _write_summary_statistics(self, comparison_results: List[Dict[str, Any]]):
        """Write summary statistics."""
        stats_file = self.output_dir / "structure_comparison_stats.txt"

        with open(stats_file, "w") as f:
            f.write("Structure Comparison Statistics\n")
            f.write("=" * 80 + "\n\n")

            # Overall statistics
            total_added = sum(
                len(r["differences"]["added"]) for r in comparison_results
            )
            total_removed = sum(
                len(r["differences"]["removed"]) for r in comparison_results
            )
            total_changed = sum(
                len(r["differences"]["changed"]) for r in comparison_results
            )
            total_unchanged = sum(
                len(r["differences"]["unchanged"]) for r in comparison_results
            )

            f.write(f"Overall Statistics:\n")
            f.write(f"  Total comparisons: {len(comparison_results)}\n")
            f.write(f"  Total items added: {total_added}\n")
            f.write(f"  Total items removed: {total_removed}\n")
            f.write(f"  Total items changed: {total_changed}\n")
            f.write(f"  Total items unchanged: {total_unchanged}\n\n")

            # Most frequently changed paths
            path_changes = defaultdict(int)
            for result in comparison_results:
                for path in result["differences"]["added"]:
                    path_changes[path] += 1
                for path in result["differences"]["removed"]:
                    path_changes[path] += 1
                for path in result["differences"]["changed"]:
                    path_changes[path] += 1

            f.write(f"Most Frequently Changed Paths:\n")
            f.write("-" * 40 + "\n")
            for path, count in sorted(
                path_changes.items(), key=lambda x: x[1], reverse=True
            )[:20]:
                f.write(f"  {path}: {count} changes\n")

            # Change types analysis
            change_types = defaultdict(int)
            for result in comparison_results:
                for path, change_info in result["differences"]["changed"].items():
                    for change in change_info["changes"]:
                        change_type = change.split(":")[0] if ":" in change else change
                        change_types[change_type] += 1

            f.write(f"\nChange Types:\n")
            f.write("-" * 40 + "\n")
            for change_type, count in sorted(
                change_types.items(), key=lambda x: x[1], reverse=True
            ):
                f.write(f"  {change_type}: {count} occurrences\n")

        print(f"  Saved: {stats_file}")

    def _write_evolution_timeline(self, file_structures: Dict[str, Dict[str, Any]]):
        """Write structure evolution timeline with enhanced change highlighting."""
        timeline_file = self.output_dir / "structure_evolution_timeline.txt"

        with open(timeline_file, "w") as f:
            f.write("HDF5 Structure Evolution Timeline\n")
            f.write("=" * 80 + "\n\n")

            # Collect all unique paths across all files
            all_paths = set()
            for paths in file_structures.values():
                all_paths.update(paths.keys())

            all_paths = sorted(all_paths)

            f.write(
                f"Tracking {len(all_paths)} unique paths across {len(file_structures)} files\n\n"
            )

            # For each path, show its evolution with change highlighting
            for path in all_paths:
                f.write(f"\nPath: {path}\n")
                f.write("-" * 60 + "\n")

                # Collect all values for this path across files
                path_values = []
                for file_path, paths in file_structures.items():
                    file_name = Path(file_path).name
                    if path in paths:
                        item = paths[path]
                        if item.get("type") == "dataset":
                            shape_str = str(item.get("shape", []))
                            dtype_str = str(item.get("dtype", "unknown"))
                            value_str = f"dataset {shape_str} {dtype_str}"
                        elif item.get("type") == "group":
                            children_count = item.get("children_count", 0)
                            value_str = f"group ({children_count} children)"
                        else:
                            value_str = f"{item.get('type', 'unknown')}"

                        path_values.append((file_name, value_str))
                    else:
                        path_values.append((file_name, "<missing>"))

                # Detect changes and highlight them
                prev_value = None
                for file_name, value_str in path_values:
                    if (
                        prev_value is not None
                        and prev_value != value_str
                        and value_str != "<missing>"
                    ):
                        # Highlight changes with arrows
                        f.write(f"  {file_name}: {value_str} ← CHANGED\n")
                    else:
                        f.write(f"  {file_name}: {value_str}\n")
                    prev_value = value_str

        print(f"  Saved: {timeline_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare HDF5 file structures and identify differences"
    )
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

    comparator = HDF5StructureComparator(metadata_file)
    comparator.generate_structure_comparison_report()

    return 0


if __name__ == "__main__":
    sys.exit(main())
