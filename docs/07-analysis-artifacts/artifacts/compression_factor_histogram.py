#!/usr/bin/env python3
"""
Script to create a histogram of compression factors from stats.csv
Reads compression factors, rounds them down to integers, and creates a histogram.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
    # Read the CSV file
    csv_file = "/Users/zak/src/undersea-cable/analysis/artifacts/stats.csv"

    print(f"Reading data from {csv_file}")
    df = pd.read_csv(csv_file)

    # Extract compression factors (column 6, 0-indexed)
    compression_factors = df["compression_factor"].values

    print(f"Found {len(compression_factors)} compression factor values")
    print(
        f"Compression factor range: {compression_factors.min():.2f} to {compression_factors.max():.2f}"
    )

    # Round down to integers using numpy floor
    rounded_factors = np.floor(compression_factors).astype(int)

    print(f"Rounded factors range: {rounded_factors.min()} to {rounded_factors.max()}")

    # Create histogram
    plt.figure(figsize=(12, 8))

    # Get unique values and their counts
    unique_values, counts = np.unique(rounded_factors, return_counts=True)

    # Create bar plot
    plt.bar(unique_values, counts, alpha=0.7, edgecolor="black", linewidth=0.5)

    plt.xlabel("Compression Factor (rounded down to integer)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title(
        "Histogram of Compression Factors\n(Rounded Down to Integers)",
        fontsize=14,
        fontweight="bold",
    )
    plt.grid(True, alpha=0.3)

    # Add statistics text
    mean_val = np.mean(rounded_factors)
    median_val = np.median(rounded_factors)
    std_val = np.std(rounded_factors)

    stats_text = f"Mean: {mean_val:.1f}\nMedian: {median_val:.1f}\nStd Dev: {std_val:.1f}\nTotal Samples: {len(rounded_factors)}"
    plt.text(
        0.02,
        0.98,
        stats_text,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    plt.tight_layout()

    # Save as image
    output_image = "/Users/zak/src/undersea-cable/analysis/artifacts/compression_factor_histogram.png"
    plt.savefig(output_image, dpi=300, bbox_inches="tight")
    print(f"Histogram saved as image: {output_image}")

    # Create text summary
    output_text = "/Users/zak/src/undersea-cable/analysis/artifacts/compression_factor_histogram.txt"

    with open(output_text, "w") as f:
        f.write("Compression Factor Histogram Summary\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total samples: {len(rounded_factors)}\n")
        f.write(
            f"Original range: {compression_factors.min():.2f} to {compression_factors.max():.2f}\n"
        )
        f.write(
            f"Rounded range: {rounded_factors.min()} to {rounded_factors.max()}\n\n"
        )

        f.write("Statistics:\n")
        f.write(f"  Mean: {mean_val:.2f}\n")
        f.write(f"  Median: {median_val:.2f}\n")
        f.write(f"  Standard Deviation: {std_val:.2f}\n\n")

        f.write("Histogram bins (compression_factor: count):\n")
        for val, count in zip(unique_values, counts):
            f.write(f"  {val}: {count}\n")

        f.write(f"\nPercentage distribution:\n")
        for val, count in zip(unique_values, counts):
            percentage = (count / len(rounded_factors)) * 100
            f.write(f"  {val}: {count} ({percentage:.1f}%)\n")

    print(f"Histogram summary saved as text: {output_text}")

    # Show the plot
    plt.show()

    print("\nSummary:")
    print(f"- Processed {len(compression_factors)} compression factors")
    print(
        f"- Rounded down to integers ranging from {rounded_factors.min()} to {rounded_factors.max()}"
    )
    print(f"- Created histogram with {len(unique_values)} unique integer values")
    print(f"- Files saved: {output_image} and {output_text}")


if __name__ == "__main__":
    main()
