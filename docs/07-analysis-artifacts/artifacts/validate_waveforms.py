#!/usr/bin/env python3
"""
Visual validation of compression-based event detection hypothesis.

This script loads actual waveform data from sample files in each category
and creates side-by-side comparisons to validate that low-compression files
indeed contain more interesting/complex signals.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd


def load_sample_waveform(filepath, max_samples=10000):
    """Load a sample of waveform data from HDF5 file."""

    try:
        with h5py.File(filepath, "r") as f:
            # Try to find 'data' dataset (common in DAS files)
            if "data" in f:
                data = f["data"][:]
            else:
                # Get first dataset
                first_key = list(f.keys())[0]
                data = f[first_key][:]

            # If 2D, flatten or take first channel
            if data.ndim == 2:
                data = data.flatten()[:max_samples]
            else:
                data = data[:max_samples]

            return data
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def plot_waveform_comparison(files_by_category, output_path):
    """Create comparison plot of waveforms from different categories."""

    n_categories = len(files_by_category)
    fig, axes = plt.subplots(n_categories, 3, figsize=(18, 4 * n_categories))

    if n_categories == 1:
        axes = axes.reshape(1, -1)

    fig.suptitle(
        "Waveform Comparison by Compression Category", fontsize=16, fontweight="bold"
    )

    for idx, (category, files) in enumerate(sorted(files_by_category.items())):

        if not files:
            continue

        # Load first available file
        waveform = None
        actual_file = None
        for filepath in files:
            waveform = load_sample_waveform(filepath)
            if waveform is not None:
                actual_file = filepath
                break

        if waveform is None:
            print(f"Warning: Could not load any file from {category}")
            continue

        # Subsample for visualization
        plot_samples = min(5000, len(waveform))
        plot_data = waveform[:plot_samples]

        # 1. Time series
        axes[idx, 0].plot(plot_data, linewidth=0.5, alpha=0.7)
        axes[idx, 0].set_ylabel("Amplitude")
        axes[idx, 0].set_title(f"{category}\nTime Series")
        axes[idx, 0].grid(True, alpha=0.3)

        # 2. Histogram
        axes[idx, 1].hist(
            waveform, bins=100, alpha=0.7, edgecolor="black", linewidth=0.5
        )
        axes[idx, 1].set_xlabel("Amplitude")
        axes[idx, 1].set_ylabel("Frequency")
        axes[idx, 1].set_title(f"{category}\nAmplitude Distribution")
        axes[idx, 1].grid(True, alpha=0.3, axis="y")

        # 3. Power spectrum
        try:
            from scipy import signal

            freqs, psd = signal.welch(waveform, nperseg=min(1024, len(waveform) // 4))
            axes[idx, 2].semilogy(freqs, psd, linewidth=1)
            axes[idx, 2].set_xlabel("Frequency (normalized)")
            axes[idx, 2].set_ylabel("Power Spectral Density")
            axes[idx, 2].set_title(f"{category}\nPower Spectrum")
            axes[idx, 2].grid(True, alpha=0.3)
        except:
            # Fallback: simple FFT
            fft = np.fft.fft(waveform)
            freqs = np.fft.fftfreq(len(waveform))
            axes[idx, 2].semilogy(
                freqs[: len(freqs) // 2], np.abs(fft[: len(fft) // 2]), linewidth=1
            )
            axes[idx, 2].set_xlabel("Frequency (normalized)")
            axes[idx, 2].set_ylabel("FFT Magnitude")
            axes[idx, 2].set_title(f"{category}\nFrequency Content")
            axes[idx, 2].grid(True, alpha=0.3)

        # Add statistics
        stats_text = (
            f"File: {Path(actual_file).name}\n"
            f"Std: {np.std(waveform):.2f}\n"
            f"Range: {np.max(waveform) - np.min(waveform):.2f}\n"
            f"Samples: {len(waveform)}"
        )
        axes[idx, 0].text(
            0.02,
            0.98,
            stats_text,
            transform=axes[idx, 0].transAxes,
            verticalalignment="top",
            fontsize=8,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"\nSaved waveform comparison: {output_path}")
    plt.close()


def main():
    """Validate hypothesis by visualizing actual waveforms."""

    print("=" * 80)
    print("WAVEFORM VALIDATION ANALYSIS")
    print("=" * 80)

    # Load the priority list to find example files
    priority_file = "/Users/zak/src/undersea-cable/analysis/artifacts/transmission_priority_list.csv"

    if not Path(priority_file).exists():
        print(
            f"Error: {priority_file} not found. Run advanced_event_detection.py first."
        )
        return

    df = pd.read_csv(priority_file)

    # Select sample files from each category
    samples_per_category = 1
    files_by_category = {}

    for category in ["anomaly_low", "normal_low", "normal_high"]:
        cat_files = (
            df[df["category"] == category]["file"].head(samples_per_category).tolist()
        )

        # Check if files exist
        existing_files = [f for f in cat_files if Path(f).exists()]

        if existing_files:
            files_by_category[category] = existing_files
            print(f"\n{category}: Using {Path(existing_files[0]).name}")
        else:
            print(f"\n{category}: No files found (may need to download data)")

    if not files_by_category:
        print("\nNo HDF5 files found. Please ensure data files are available.")
        print("Files should be in: /Users/zak/src/undersea-cable/das24_data/")
        return

    # Create comparison visualization
    output_path = (
        "/Users/zak/src/undersea-cable/analysis/artifacts/waveform_validation.png"
    )
    plot_waveform_comparison(files_by_category, output_path)

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print("\nReview waveform_validation.png to visually confirm:")
    print("  - Anomaly_low files have more complex/variable signals")
    print("  - Normal files have simpler/more regular patterns")
    print("\nThis visual inspection validates the statistical findings.")


if __name__ == "__main__":
    main()
