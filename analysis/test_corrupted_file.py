#!/usr/bin/env python3
"""Test script to reproduce and fix the truncated HDF5 file error."""

import h5py
from pathlib import Path


def test_file_opening(file_path):
    """Test opening an HDF5 file with error handling."""
    print(f"\nTesting file: {file_path}")
    print(f"File size: {file_path.stat().st_size:,} bytes")

    try:
        with h5py.File(file_path, "r") as f:
            print(f"✅ Successfully opened: {file_path.name}")
            print(f"   Keys: {list(f.keys())}")
            return True, None
    except OSError as e:
        error_msg = str(e)
        if "truncated file" in error_msg.lower():
            print(f"❌ TRUNCATED FILE ERROR: {file_path.name}")
            print(f"   Error: {error_msg}")
            return False, "truncated"
        else:
            print(f"❌ OTHER OSError: {file_path.name}")
            print(f"   Error: {error_msg}")
            return False, "other_os_error"
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {file_path.name}")
        print(f"   Error: {type(e).__name__}: {e}")
        return False, "unexpected"


if __name__ == "__main__":
    # Test the specific file that caused the error
    problem_file = Path("das24_data/20240506/dphi/171135.hdf5")

    if problem_file.exists():
        success, error_type = test_file_opening(problem_file)
        print(f"\nResult: {'SUCCESS' if success else f'FAILED ({error_type})'}")
    else:
        print(f"File not found: {problem_file}")
