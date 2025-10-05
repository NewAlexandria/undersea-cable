#!/usr/bin/env python3
"""
HDF5 Metadata Scanner with Persistent Index

Scans HDF5 files recursively and builds a persistent metadata index that includes:
- File structure (groups and datasets)
- Dataset shapes, dtypes, and attributes
- Group attributes
- Hierarchical tree structure

The index is stored in JSON format and can be incrementally updated.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import h5py
import numpy as np


class HDF5MetadataScanner:
    """Scans HDF5 files and builds a persistent metadata index."""

    def __init__(self, metadata_file: Path):
        self.metadata_file = metadata_file
        self.metadata: Dict[str, Any] = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load existing metadata or create new structure."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    data = json.load(f)
                print(
                    f"Loaded existing metadata with {len(data.get('files', {}))} files"
                )
                return data
            except Exception as e:
                print(f"Warning: Could not load metadata file: {e}", file=sys.stderr)
                print("Creating new metadata structure", file=sys.stderr)

        return {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "files": {},  # file_path -> metadata
            "scanned_directories": [],  # list of fully scanned directories
        }

    def save_metadata(self):
        """Save metadata to disk."""
        self.metadata["last_updated"] = datetime.now().isoformat()
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)
        print(f"Saved metadata to {self.metadata_file}")

    def _serialize_value(self, value: Any) -> Any:
        """Convert numpy/HDF5 types to JSON-serializable types."""
        if isinstance(value, (np.integer, np.floating)):
            return value.item()
        elif isinstance(value, np.ndarray):
            if value.size <= 10:  # Only store small arrays
                return value.tolist()
            else:
                return f"<array shape={value.shape} dtype={value.dtype}>"
        elif isinstance(value, bytes):
            try:
                return value.decode("utf-8")
            except:
                return f"<bytes length={len(value)}>"
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(v) for v in value]
        else:
            return str(value)

    def _extract_attributes(self, h5obj) -> Dict[str, Any]:
        """Extract attributes from an HDF5 object."""
        attrs = {}
        for key in h5obj.attrs.keys():
            try:
                attrs[key] = self._serialize_value(h5obj.attrs[key])
            except Exception as e:
                attrs[key] = f"<error reading attribute: {e}>"
        return attrs

    def _scan_item(self, name: str, obj, path_prefix: str = "") -> Dict[str, Any]:
        """Recursively scan an HDF5 item (group or dataset)."""
        full_path = f"{path_prefix}/{name}" if path_prefix else name

        if isinstance(obj, h5py.Dataset):
            return {
                "type": "dataset",
                "path": full_path,
                "shape": list(obj.shape) if obj.shape else [],
                "dtype": str(obj.dtype),
                "size": int(obj.size),
                "nbytes": int(obj.nbytes) if hasattr(obj, "nbytes") else None,
                "chunks": list(obj.chunks) if obj.chunks else None,
                "compression": obj.compression if hasattr(obj, "compression") else None,
                "attributes": self._extract_attributes(obj),
            }
        elif isinstance(obj, h5py.Group):
            children = {}
            for child_name in obj.keys():
                try:
                    children[child_name] = self._scan_item(
                        child_name, obj[child_name], full_path
                    )
                except Exception as e:
                    children[child_name] = {"type": "error", "error": str(e)}

            return {
                "type": "group",
                "path": full_path,
                "attributes": self._extract_attributes(obj),
                "children": children,
            }
        else:
            return {"type": "unknown", "path": full_path, "class": str(type(obj))}

    def scan_file(
        self, file_path: Path, force: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Scan a single HDF5 file and return its metadata.

        Args:
            file_path: Path to the HDF5 file
            force: If True, rescan even if file is already in index

        Returns:
            File metadata dictionary or None if scan failed
        """
        file_key = str(file_path.resolve())

        # Check if already scanned
        if not force and file_key in self.metadata["files"]:
            print(f"  Skipping (already scanned): {file_path.name}")
            return self.metadata["files"][file_key]

        try:
            file_stat = file_path.stat()

            with h5py.File(file_path, "r") as f:
                # Build tree structure
                structure = {}
                for key in f.keys():
                    structure[key] = self._scan_item(key, f[key])

                file_metadata = {
                    "file_path": file_key,
                    "file_name": file_path.name,
                    "file_size": file_stat.st_size,
                    "modified_time": datetime.fromtimestamp(
                        file_stat.st_mtime
                    ).isoformat(),
                    "scanned_time": datetime.now().isoformat(),
                    "root_attributes": self._extract_attributes(f),
                    "structure": structure,
                }

                self.metadata["files"][file_key] = file_metadata
                return file_metadata

        except OSError as e:
            error_msg = str(e)
            if "truncated file" in error_msg.lower():
                print(f"  ⚠️  Truncated file: {file_path.name}", file=sys.stderr)
            elif "unable to open file" in error_msg.lower():
                print(f"  ⚠️  Cannot open file: {file_path.name}", file=sys.stderr)
            else:
                print(f"  ⚠️  OSError: {file_path.name}: {error_msg}", file=sys.stderr)
            return None
        except Exception as e:
            print(
                f"  ⚠️  Error scanning {file_path.name}: {type(e).__name__}: {e}",
                file=sys.stderr,
            )
            return None

    def scan_directory(
        self,
        directory: Path,
        force: bool = False,
        extensions: Set[str] = {".h5", ".hdf5"},
    ) -> int:
        """
        Scan all HDF5 files in a directory recursively.

        Args:
            directory: Directory to scan
            force: If True, rescan all files even if directory was scanned before
            extensions: Set of file extensions to scan

        Returns:
            Number of files scanned
        """
        dir_key = str(directory.resolve())

        # Check if directory was already fully scanned
        if not force and dir_key in self.metadata["scanned_directories"]:
            print(f"Directory already scanned: {directory}")
            print("Use --force to rescan")
            return 0

        # Find all HDF5 files
        files = []
        for ext in extensions:
            files.extend(directory.rglob(f"*{ext}"))

        files = sorted(files)
        print(f"\nFound {len(files)} HDF5 files in {directory}")

        scanned_count = 0
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] Scanning: {file_path.name}")
            if self.scan_file(file_path, force=force):
                scanned_count += 1

        # Mark directory as scanned
        if dir_key not in self.metadata["scanned_directories"]:
            self.metadata["scanned_directories"].append(dir_key)

        print(f"\nSuccessfully scanned {scanned_count}/{len(files)} files")
        return scanned_count


def main():
    parser = argparse.ArgumentParser(
        description="Scan HDF5 files and build persistent metadata index"
    )
    parser.add_argument("input", type=str, help="Directory to scan for HDF5 files")
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

    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"Error: Directory not found: {input_dir}", file=sys.stderr)
        return 1

    if not input_dir.is_dir():
        print(f"Error: Not a directory: {input_dir}", file=sys.stderr)
        return 1

    # Create scanner
    metadata_file = Path(args.metadata_file)
    scanner = HDF5MetadataScanner(metadata_file)

    # Scan directory
    extensions = set(args.extensions)
    scanned_count = scanner.scan_directory(
        input_dir, force=args.force, extensions=extensions
    )

    # Save results
    scanner.save_metadata()

    print(f"\n✅ Scan complete!")
    print(f"   Total files in index: {len(scanner.metadata['files'])}")
    print(f"   Scanned directories: {len(scanner.metadata['scanned_directories'])}")
    print(f"   Metadata file: {metadata_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())



