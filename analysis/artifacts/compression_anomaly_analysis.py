#!/usr/bin/env python3
"""
Analysis of compression ratio anomalies to identify interesting event data.

This script explores the hypothesis that files with unusual compression ratios
(not ~8 or ~14) may contain more interesting event data worth transmitting.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Set style
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")


def categorize_compression_ratio(ratio):
    """Categorize compression ratios into groups."""
    rounded = int(np.floor(ratio))

    if 7 <= rounded <= 9:
        return "normal_low"  # ~8
    elif 13 <= rounded <= 15:
        return "normal_high"  # ~14
    elif rounded < 7:
        return "anomaly_low"  # < 7 (harder to compress, more complex?)
    else:  # 10-12
        return "anomaly_mid"  # intermediate


def analyze_statistics_by_category(df):
    """Analyze statistical properties grouped by compression category."""

    print("\n" + "=" * 80)
    print("STATISTICAL ANALYSIS BY COMPRESSION CATEGORY")
    print("=" * 80)

    # Add category column
    df["category"] = df["compression_factor"].apply(categorize_compression_ratio)
    df["compression_rounded"] = np.floor(df["compression_factor"]).astype(int)

    # Summary counts
    print("\nCategory Distribution:")
    print(df["category"].value_counts().sort_index())
    print(f"\nTotal files: {len(df)}")

    # Statistical comparisons
    metrics = ["std", "min", "max", "p99p9", "p0p1", "mean"]

    results = {}
    for category in sorted(df["category"].unique()):
        cat_data = df[df["category"] == category]
        results[category] = {
            "count": len(cat_data),
            "compression_mean": cat_data["compression_factor"].mean(),
            "compression_std": cat_data["compression_factor"].std(),
        }

        for metric in metrics:
            if metric in df.columns:
                results[category][f"{metric}_mean"] = cat_data[metric].mean()
                results[category][f"{metric}_std"] = cat_data[metric].std()
                results[category][f"{metric}_range"] = (
                    cat_data[metric].max() - cat_data[metric].min()
                )

    # Print detailed statistics
    print("\n" + "-" * 80)
    print("Detailed Statistics by Category:")
    print("-" * 80)
    for category, stats in results.items():
        print(f"\n{category.upper()} (n={stats['count']}):")
        print(
            f"  Compression: {stats['compression_mean']:.2f} ± {stats['compression_std']:.2f}"
        )
        if "std_mean" in stats:
            print(f"  Data Std Dev: {stats['std_mean']:.3f} ± {stats['std_std']:.3f}")
            print(
                f"  Data Range (max-min): {stats.get('max_mean', 0) - stats.get('min_mean', 0):.3f}"
            )
            print(
                f"  P99.9 - P0.1 spread: {stats.get('p99p9_mean', 0) - stats.get('p0p1_mean', 0):.3f}"
            )

    return df, results


def calculate_signal_complexity(df):
    """Calculate proxy metrics for signal complexity."""

    print("\n" + "=" * 80)
    print("SIGNAL COMPLEXITY ANALYSIS")
    print("=" * 80)

    # Dynamic range: difference between extreme percentiles
    df["dynamic_range"] = df["p99p9"] - df["p0p1"]

    # Absolute dynamic range
    df["absolute_range"] = df["max"] - df["min"]

    # Coefficient of variation (normalized variability)
    df["coef_variation"] = df["std"] / (np.abs(df["mean"]) + 1e-10)

    # Signal-to-noise-like ratio
    df["signal_complexity"] = df["std"] / df["compression_factor"]

    print("\nComplexity Metrics by Category:")
    print("-" * 80)

    for category in sorted(df["category"].unique()):
        cat_data = df[df["category"] == category]
        print(f"\n{category.upper()}:")
        print(
            f"  Dynamic Range: {cat_data['dynamic_range'].mean():.3f} ± {cat_data['dynamic_range'].std():.3f}"
        )
        print(
            f"  Absolute Range: {cat_data['absolute_range'].mean():.3f} ± {cat_data['absolute_range'].std():.3f}"
        )
        print(
            f"  Coef. of Variation: {cat_data['coef_variation'].mean():.3f} ± {cat_data['coef_variation'].std():.3f}"
        )
        print(
            f"  Signal Complexity: {cat_data['signal_complexity'].mean():.3f} ± {cat_data['signal_complexity'].std():.3f}"
        )

    return df


def temporal_analysis(df):
    """Analyze temporal patterns in compression anomalies."""

    print("\n" + "=" * 80)
    print("TEMPORAL PATTERN ANALYSIS")
    print("=" * 80)

    # Extract timestamp from filename
    df["filename"] = df["file"].apply(lambda x: Path(x).stem)
    df["timestamp"] = df["filename"].astype(str)

    # Sort by timestamp
    df_sorted = df.sort_values("timestamp")

    # Identify runs of anomalies
    anomaly_mask = ~df_sorted["category"].isin(["normal_low", "normal_high"])
    df_sorted["is_anomaly"] = anomaly_mask

    # Calculate runs
    df_sorted["anomaly_change"] = df_sorted["is_anomaly"].astype(int).diff().fillna(0)

    anomaly_count = df_sorted["is_anomaly"].sum()
    total_count = len(df_sorted)

    print(f"\nAnomaly Statistics:")
    print(
        f"  Total anomalies: {anomaly_count} / {total_count} ({100*anomaly_count/total_count:.1f}%)"
    )

    # Find longest runs
    run_lengths = []
    current_run = 0
    for is_anom in df_sorted["is_anomaly"]:
        if is_anom:
            current_run += 1
        else:
            if current_run > 0:
                run_lengths.append(current_run)
            current_run = 0
    if current_run > 0:
        run_lengths.append(current_run)

    if run_lengths:
        print(f"  Anomaly runs: {len(run_lengths)} sequences")
        print(f"  Longest run: {max(run_lengths)} consecutive anomalies")
        print(f"  Mean run length: {np.mean(run_lengths):.1f}")

    return df_sorted


def create_visualizations(df, output_dir):
    """Create comprehensive visualizations."""

    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)

    output_dir = Path(output_dir)

    # 1. Compression factor vs Statistical properties
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(
        "Compression Factor vs Data Properties", fontsize=16, fontweight="bold"
    )

    properties = [
        ("std", "Standard Deviation"),
        ("dynamic_range", "Dynamic Range (P99.9-P0.1)"),
        ("absolute_range", "Absolute Range (Max-Min)"),
        ("coef_variation", "Coefficient of Variation"),
        ("signal_complexity", "Signal Complexity"),
        ("mean", "Mean Value"),
    ]

    for ax, (prop, title) in zip(axes.flat, properties):
        for category in sorted(df["category"].unique()):
            cat_data = df[df["category"] == category]
            ax.scatter(
                cat_data["compression_factor"],
                cat_data[prop],
                alpha=0.6,
                label=category,
                s=30,
            )

        ax.set_xlabel("Compression Factor")
        ax.set_ylabel(title)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        output_dir / "compression_vs_properties.png", dpi=300, bbox_inches="tight"
    )
    print(f"  Saved: compression_vs_properties.png")
    plt.close()

    # 2. Distribution comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "Statistical Distribution by Compression Category",
        fontsize=16,
        fontweight="bold",
    )

    metrics = ["std", "dynamic_range", "coef_variation", "signal_complexity"]
    titles = [
        "Standard Deviation",
        "Dynamic Range",
        "Coef. of Variation",
        "Signal Complexity",
    ]

    for ax, metric, title in zip(axes.flat, metrics, titles):
        for category in sorted(df["category"].unique()):
            cat_data = df[df["category"] == category]
            ax.hist(cat_data[metric], alpha=0.5, label=category, bins=20)

        ax.set_xlabel(title)
        ax.set_ylabel("Frequency")
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        output_dir / "distribution_comparison.png", dpi=300, bbox_inches="tight"
    )
    print(f"  Saved: distribution_comparison.png")
    plt.close()

    # 3. Box plots for key metrics
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.suptitle("Key Metrics by Compression Category", fontsize=16, fontweight="bold")

    key_metrics = [
        ("std", "Standard Deviation"),
        ("dynamic_range", "Dynamic Range"),
        ("signal_complexity", "Signal Complexity"),
    ]

    for ax, (metric, title) in zip(axes, key_metrics):
        data_to_plot = [
            df[df["category"] == cat][metric].values
            for cat in sorted(df["category"].unique())
        ]
        ax.boxplot(data_to_plot, labels=sorted(df["category"].unique()))
        ax.set_ylabel(title)
        ax.set_xlabel("Category")
        ax.grid(True, alpha=0.3, axis="y")
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(output_dir / "category_boxplots.png", dpi=300, bbox_inches="tight")
    print(f"  Saved: category_boxplots.png")
    plt.close()

    # 4. Temporal pattern
    fig, ax = plt.subplots(figsize=(16, 6))

    # Plot compression factor over time with color coding
    for category in sorted(df["category"].unique()):
        cat_data = df[df["category"] == category].sort_values("timestamp")
        ax.scatter(
            range(len(cat_data)),
            cat_data["compression_factor"],
            label=category,
            alpha=0.7,
            s=20,
        )

    ax.set_xlabel("File Index (temporal order)")
    ax.set_ylabel("Compression Factor")
    ax.set_title(
        "Compression Factor Over Time (by Category)", fontsize=14, fontweight="bold"
    )
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "temporal_pattern.png", dpi=300, bbox_inches="tight")
    print(f"  Saved: temporal_pattern.png")
    plt.close()


def identify_interesting_files(df, output_dir):
    """Identify specific files worth investigating."""

    print("\n" + "=" * 80)
    print("IDENTIFYING FILES OF INTEREST")
    print("=" * 80)

    output_dir = Path(output_dir)

    # Files with anomalous compression
    anomalies = df[~df["category"].isin(["normal_low", "normal_high"])].copy()

    # Sort by different criteria
    interesting_files = {
        "lowest_compression": df.nsmallest(10, "compression_factor")[
            ["file", "compression_factor", "std", "dynamic_range", "category"]
        ],
        "highest_std": df.nlargest(10, "std")[
            ["file", "compression_factor", "std", "dynamic_range", "category"]
        ],
        "highest_dynamic_range": df.nlargest(10, "dynamic_range")[
            ["file", "compression_factor", "std", "dynamic_range", "category"]
        ],
        "highest_complexity": df.nlargest(10, "signal_complexity")[
            ["file", "compression_factor", "std", "signal_complexity", "category"]
        ],
    }

    # Save to JSON
    files_json = {}
    for key, files_df in interesting_files.items():
        print(f"\n{key.replace('_', ' ').title()}:")
        print(files_df.to_string(index=False))

        files_json[key] = files_df.to_dict("records")

    with open(output_dir / "interesting_files.json", "w") as f:
        json.dump(files_json, f, indent=2)

    print(f"\n  Saved: interesting_files.json")

    return interesting_files


def generate_report(df, results, output_dir):
    """Generate a comprehensive markdown report."""

    output_dir = Path(output_dir)
    report_path = output_dir / "compression_anomaly_report.md"

    with open(report_path, "w") as f:
        f.write("# Compression Anomaly Analysis Report\n\n")
        f.write("## Executive Summary\n\n")

        # Summary statistics
        total = len(df)
        anomalies = df[~df["category"].isin(["normal_low", "normal_high"])]
        anomaly_pct = 100 * len(anomalies) / total

        f.write(f"**Total Files Analyzed:** {total}\n\n")
        f.write(f"**Anomalous Files:** {len(anomalies)} ({anomaly_pct:.1f}%)\n\n")

        f.write("### Key Findings\n\n")

        # Compare anomalies vs normal
        normal_low = df[df["category"] == "normal_low"]
        normal_high = df[df["category"] == "normal_high"]

        f.write("#### Hypothesis Validation\n\n")
        f.write(
            "We investigated whether files with unusual compression ratios contain more interesting event data.\n\n"
        )

        # Statistical evidence
        if len(anomalies) > 0:
            anom_std = anomalies["std"].mean()
            norm_low_std = normal_low["std"].mean() if len(normal_low) > 0 else 0
            norm_high_std = normal_high["std"].mean() if len(normal_high) > 0 else 0

            f.write(f"**Standard Deviation Comparison:**\n")
            f.write(f"- Anomalous files: {anom_std:.3f}\n")
            f.write(f"- Normal (low compression ~8): {norm_low_std:.3f}\n")
            f.write(f"- Normal (high compression ~14): {norm_high_std:.3f}\n\n")

            anom_dr = anomalies["dynamic_range"].mean()
            norm_low_dr = (
                normal_low["dynamic_range"].mean() if len(normal_low) > 0 else 0
            )
            norm_high_dr = (
                normal_high["dynamic_range"].mean() if len(normal_high) > 0 else 0
            )

            f.write(f"**Dynamic Range Comparison:**\n")
            f.write(f"- Anomalous files: {anom_dr:.3f}\n")
            f.write(f"- Normal (low compression ~8): {norm_low_dr:.3f}\n")
            f.write(f"- Normal (high compression ~14): {norm_high_dr:.3f}\n\n")

            # Interpretation
            if anom_std > max(norm_low_std, norm_high_std) * 1.1:
                f.write(
                    "✓ **HYPOTHESIS SUPPORTED:** Anomalous compression files show higher variability, suggesting more complex/interesting signals.\n\n"
                )
            elif anom_std < min(norm_low_std, norm_high_std) * 0.9:
                f.write(
                    '✗ **HYPOTHESIS PARTIALLY REFUTED:** Anomalous compression files show lower variability, possibly indicating different signal characteristics rather than "more interesting" events.\n\n'
                )
            else:
                f.write(
                    "⚠ **INCONCLUSIVE:** Anomalous files show similar statistical properties. Further analysis needed.\n\n"
                )

        f.write("## Detailed Analysis\n\n")

        f.write("### Compression Category Distribution\n\n")
        f.write("| Category | Count | Percentage |\n")
        f.write("|----------|-------|------------|\n")
        for category in sorted(df["category"].unique()):
            count = len(df[df["category"] == category])
            pct = 100 * count / total
            f.write(f"| {category} | {count} | {pct:.1f}% |\n")

        f.write("\n### Statistical Properties by Category\n\n")
        f.write(
            "| Category | Count | Avg Compression | Avg Std Dev | Avg Dynamic Range | Signal Complexity |\n"
        )
        f.write(
            "|----------|-------|-----------------|-------------|-------------------|-------------------|\n"
        )

        for category in sorted(df["category"].unique()):
            cat_data = df[df["category"] == category]
            f.write(
                f"| {category} | {len(cat_data)} | {cat_data['compression_factor'].mean():.2f} | "
                f"{cat_data['std'].mean():.3f} | {cat_data['dynamic_range'].mean():.3f} | "
                f"{cat_data['signal_complexity'].mean():.3f} |\n"
            )

        f.write("\n## Recommendations\n\n")

        if len(anomalies) > 0 and anomalies["std"].mean() > normal_low["std"].mean():
            f.write(
                "1. **PRIORITIZE TRANSMISSION** of files with compression ratios outside 7-9 and 13-15 ranges\n"
            )
            f.write(
                "2. **IMPLEMENT FILTERING**: Focus bandwidth on anomalous compression files\n"
            )
            f.write(
                "3. **REAL-TIME MONITORING**: Use compression ratio as a proxy for event detection\n"
            )
        else:
            f.write(
                "1. **FURTHER INVESTIGATION** needed to understand anomalous compression patterns\n"
            )
            f.write(
                "2. **ADDITIONAL METRICS**: Consider spectral analysis, entropy, or domain-specific features\n"
            )
            f.write(
                "3. **MANUAL INSPECTION**: Review sample files from each category\n"
            )

        f.write("\n## Visualizations\n\n")
        f.write("See accompanying PNG files:\n")
        f.write(
            "- `compression_vs_properties.png` - Scatter plots of compression vs data properties\n"
        )
        f.write("- `distribution_comparison.png` - Histograms comparing categories\n")
        f.write("- `category_boxplots.png` - Box plots of key metrics\n")
        f.write("- `temporal_pattern.png` - Time series of compression factors\n")

        f.write("\n## Files of Interest\n\n")
        f.write(
            "See `interesting_files.json` for specific file paths to investigate.\n"
        )

    print(f"\n  Generated report: {report_path}")


def main():
    """Main analysis pipeline."""

    csv_file = "/Users/zak/src/undersea-cable/analysis/artifacts/stats.csv"
    output_dir = "/Users/zak/src/undersea-cable/analysis/artifacts"

    print("=" * 80)
    print("COMPRESSION ANOMALY ANALYSIS")
    print("=" * 80)
    print(f"\nInput: {csv_file}")
    print(f"Output: {output_dir}")

    # Load data
    df = pd.read_csv(csv_file)
    print(f"\nLoaded {len(df)} records")

    # Analysis pipeline
    df, results = analyze_statistics_by_category(df)
    df = calculate_signal_complexity(df)
    df = temporal_analysis(df)

    # Visualizations
    create_visualizations(df, output_dir)

    # Identify interesting files
    interesting_files = identify_interesting_files(df, output_dir)

    # Generate report
    generate_report(df, results, output_dir)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nOutput files in: {output_dir}")
    print("  - compression_anomaly_report.md")
    print("  - interesting_files.json")
    print("  - compression_vs_properties.png")
    print("  - distribution_comparison.png")
    print("  - category_boxplots.png")
    print("  - temporal_pattern.png")


if __name__ == "__main__":
    main()
