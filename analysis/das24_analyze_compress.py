#!/usr/bin/env python3
import argparse
import os
import sys
import time
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

import numpy as np
import pandas as pd
import h5py
from tqdm import tqdm
import matplotlib.pyplot as plt


def find_hdf5_files(root: Path) -> List[Path]:
    exts = {".h5", ".hdf5"}
    files: List[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            files.append(p)
    return files


def list_numeric_2d_datasets(f: h5py.File) -> List[str]:
    out: List[str] = []

    def visitor(name, obj):
        if isinstance(obj, h5py.Dataset):
            if obj.ndim == 2 and np.issubdtype(obj.dtype, np.number):
                out.append(name)

    f.visititems(visitor)
    # Prefer a dataset named "data" if present by moving it to the front
    out.sort()
    if "data" in out:
        out.remove("data")
        out.insert(0, "data")
    return out


def sample_array(a: np.ndarray, max_elems: int) -> np.ndarray:
    n = a.size
    if n <= max_elems:
        return a
    ratio = np.sqrt(max_elems / n)
    step0 = max(1, int(round(1 / ratio)))
    view = a[::step0, ::step0]
    if view.size <= max_elems:
        return view
    # fallback: random sample without replacement on flattened indices
    flat = a.ravel()
    idx = np.random.default_rng(0xA11CE).choice(
        flat.size, size=max_elems, replace=False
    )
    return flat[idx]


def compute_stats(a: np.ndarray) -> Dict[str, Any]:
    stats: Dict[str, Any] = {}
    stats["shape"] = tuple(a.shape)
    stats["dtype"] = str(a.dtype)
    stats["nbytes"] = int(a.nbytes)
    if a.size == 0:
        stats.update(
            {
                "min": np.nan,
                "max": np.nan,
                "mean": np.nan,
                "std": np.nan,
                "p0p1": np.nan,
                "p1": np.nan,
                "p50": np.nan,
                "p99": np.nan,
                "p99p9": np.nan,
                "nan_frac": np.nan,
            }
        )
        return stats

    if np.issubdtype(a.dtype, np.floating):
        nan_frac = float(np.isnan(a).mean())
        arr = a[np.isfinite(a)]
    else:
        nan_frac = 0.0
        arr = a

    if arr.size == 0:
        stats.update(
            {
                "min": np.nan,
                "max": np.nan,
                "mean": np.nan,
                "std": np.nan,
                "p0p1": np.nan,
                "p1": np.nan,
                "p50": np.nan,
                "p99": np.nan,
                "p99p9": np.nan,
                "nan_frac": nan_frac,
            }
        )
        return stats

    stats["min"] = float(np.min(arr))
    stats["max"] = float(np.max(arr))
    stats["mean"] = float(np.mean(arr))
    stats["std"] = float(np.std(arr))
    qs = np.percentile(arr, [0.1, 1, 50, 99, 99.9])
    stats["p0p1"], stats["p1"], stats["p50"], stats["p99"], stats["p99p9"] = map(
        float, qs
    )
    stats["nan_frac"] = nan_frac
    return stats


def save_histogram(a: np.ndarray, out_png: Path, title: str) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)

    if a.size == 0:
        return
    if np.issubdtype(a.dtype, np.floating):
        finite = a[np.isfinite(a)]
        if finite.size == 0:
            return
        lo, hi = np.percentile(finite, [1, 99])
        data = np.clip(finite, lo, hi)
        bins = 128
    else:
        data = a
        vmin, vmax = int(np.min(data)), int(np.max(data))
        if vmin == vmax:
            bins = 1
        else:
            bins = min(256, vmax - vmin + 1)

    plt.figure(figsize=(8, 4))
    plt.hist(data.ravel(), bins=bins, color="#1abc9c", alpha=0.8)
    plt.title(title)
    plt.xlabel("value")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()


def ensure_daspack() -> Tuple[Any, Any]:
    try:
        from daspack import DASCoder, Quantizer

        return DASCoder, Quantizer
    except Exception as e:
        raise RuntimeError(
            "daspack is not installed. Build it with 'maturin develop --release' in the daspack/ directory, "
            "or install via 'pip install daspack-dev'. Original error: %s" % (e,)
        )


def encode_one(coder, quantizer, arr: np.ndarray) -> bytes:
    return coder.encode(arr, quantizer)


def process_dataset(
    h5_path: Path,
    dset_name: str,
    threads: int,
    uniform_steps: List[float],
    max_sample: int,
    verify_limit: int,
    outputs_dir: Path,
    artifacts_dir: Path,
    aggregator_h5: Optional[h5py.File],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with h5py.File(h5_path, "r") as f:
        dset = f[dset_name]
        data = dset[...]

    # Stats and histogram (on sampled data)
    sample = sample_array(data, max_sample)
    stats = compute_stats(sample)

    # Create histograms subdirectory
    histograms_dir = artifacts_dir / "histograms"
    histograms_dir.mkdir(parents=True, exist_ok=True)

    hist_png = (
        histograms_dir / f"hist_{h5_path.stem}__{dset_name.replace('/', '_')}.png"
    )
    save_histogram(sample, hist_png, title=f"{h5_path.name}:{dset_name}")

    # Compression
    DASCoder, Quantizer = ensure_daspack()
    coder = DASCoder(threads=threads)

    def record(
        mode: str,
        step: Optional[float],
        stream: bytes,
        enc_s: float,
        dec_s: float,
        recon_ok: Optional[bool],
        max_err: Optional[float],
    ) -> None:
        out_name = f"{h5_path.stem}__{dset_name.replace('/', '_')}__{mode}"
        if step is not None:
            out_name += f"{step}"
        out_path = outputs_dir / f"{out_name}.dasp"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as fo:
            fo.write(stream)

        if aggregator_h5 is not None:
            grp_path = (
                f"{h5_path.stem}/{dset_name}/{mode}{'' if step is None else step}"
            )
            if grp_path in aggregator_h5:
                del aggregator_h5[grp_path]
            dset_c = aggregator_h5.create_dataset(
                grp_path + "/compressed", data=np.frombuffer(stream, dtype=np.uint8)
            )
            dset_c.attrs["lossless"] = mode == "lossless"
            dset_c.attrs["quant_step"] = float(step or 0.0)
            dset_c.attrs["shape"] = stats["shape"]
            dset_c.attrs["dtype"] = stats["dtype"]

        rows.append(
            {
                "file": str(h5_path),
                "dataset": dset_name,
                "mode": mode,
                "step": float(step) if step is not None else None,
                "orig_nbytes": int(data.nbytes),
                "compressed_bytes": len(stream),
                "compression_factor": (
                    (data.nbytes / len(stream)) if len(stream) > 0 else np.inf
                ),
                "encode_seconds": enc_s,
                "decode_seconds": dec_s,
                "verify_ok": bool(recon_ok) if recon_ok is not None else None,
                "verify_max_abs_err": float(max_err) if max_err is not None else None,
            }
        )

    # Lossless path for integer arrays
    if np.issubdtype(data.dtype, np.integer):
        arr_i32 = data.astype(np.int32, copy=False)
        q = Quantizer.Lossless()
        t0 = time.perf_counter()
        stream = encode_one(coder, q, arr_i32)
        enc_s = time.perf_counter() - t0
        # Optional decode/verify if small
        t1 = time.perf_counter()
        recon_ok = None
        dec_s = 0.0
        if arr_i32.size <= verify_limit:
            restored = coder.decode(stream)
            dec_s = time.perf_counter() - t1
            recon_ok = np.array_equal(restored, arr_i32)
        record("lossless", None, stream, enc_s, dec_s, recon_ok, None)
    else:
        # Lossy path for floats
        arr_f64 = data.astype(np.float64, copy=False)
        for step in uniform_steps:
            q = Quantizer.Uniform(step=float(step))
            t0 = time.perf_counter()
            stream = encode_one(coder, q, arr_f64)
            enc_s = time.perf_counter() - t0
            # Optional decode/verify if small
            t1 = time.perf_counter()
            max_err = None
            recon_ok = None
            dec_s = 0.0
            if arr_f64.size <= verify_limit:
                restored = coder.decode(stream)
                dec_s = time.perf_counter() - t1
                tol = step / 2 + 1e-12
                max_err = (
                    float(np.max(np.abs(restored - arr_f64))) if restored.size else 0.0
                )
                recon_ok = max_err <= tol
            record("uniform", float(step), stream, enc_s, dec_s, recon_ok, max_err)

    # Return metrics with stats columns merged
    for r in rows:
        r.update(
            {
                "shape": stats["shape"],
                "dtype": stats["dtype"],
                "min": stats.get("min"),
                "max": stats.get("max"),
                "mean": stats.get("mean"),
                "std": stats.get("std"),
                "p0p1": stats.get("p0p1"),
                "p1": stats.get("p1"),
                "p50": stats.get("p50"),
                "p99": stats.get("p99"),
                "p99p9": stats.get("p99p9"),
                "nan_frac": stats.get("nan_frac"),
            }
        )

    return rows


def append_results_md(results_md: Path, rows: List[Dict[str, Any]]) -> None:
    results_md.parent.mkdir(parents=True, exist_ok=True)
    with open(results_md, "a", encoding="utf-8") as fo:
        for r in rows:
            line = (
                f"- file={Path(r['file']).name} dset={r['dataset']} mode={r['mode']}"
                f" step={r['step']} cf={r['compression_factor']:.3f}"
                f" enc={r['encode_seconds']:.3f}s dec={r['decode_seconds']:.3f}s"
            )
            if r.get("verify_ok") is not None:
                line += f" verify_ok={r['verify_ok']}"
            if r.get("verify_max_abs_err") is not None:
                line += f" max_err={r['verify_max_abs_err']:.6g}"
            fo.write(line + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Analyze and compress DAS24 HDF5 files using daspack"
    )
    ap.add_argument(
        "--input",
        type=str,
        default="das24_data",
        help="Input directory to scan for HDF5 files",
    )
    ap.add_argument("--threads", type=int, default=4, help="Threads for DASCoder")
    ap.add_argument(
        "--uniform-steps",
        type=float,
        nargs="*",
        default=[0.5, 0.1],
        help="Uniform quantization steps for float data",
    )
    ap.add_argument(
        "--max-sample",
        type=int,
        default=2_000_000,
        help="Max elements to sample for stats/histograms",
    )
    ap.add_argument(
        "--verify-limit",
        type=int,
        default=1_200_000,
        help="Max elements allowed to fully decode for verification",
    )
    ap.add_argument(
        "--min-files",
        type=int,
        default=2,
        help="Require at least this many files to be found",
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional cap on number of files processed (0=no cap)",
    )
    args = ap.parse_args()

    root = Path(args.input).resolve()
    if not root.exists():
        print(f"Input path not found: {root}", file=sys.stderr)
        return 2

    files = find_hdf5_files(root)
    if len(files) < args.min_files:
        print(
            f"Found {len(files)} HDF5 file(s), fewer than required min-files={args.min_files}",
            file=sys.stderr,
        )
        return 3

    if args.limit and args.limit > 0:
        files = files[: args.limit]

    base_dir = Path(__file__).resolve().parent
    artifacts_dir = base_dir / "artifacts"
    outputs_dir = base_dir / "outputs"
    stats_csv = artifacts_dir / "stats.csv"
    results_md = base_dir / "RESULTS.md"
    aggregator_path = outputs_dir / "daspack_compressed.h5"

    all_rows: List[Dict[str, Any]] = []

    # Open aggregator once
    aggregator: Optional[h5py.File] = None
    outputs_dir.mkdir(parents=True, exist_ok=True)
    try:
        aggregator = h5py.File(aggregator_path, "a")
    except Exception:
        aggregator = None

    try:
        for h5_path in tqdm(files, desc="Files"):
            try:
                with h5py.File(h5_path, "r") as f:
                    dsets = list_numeric_2d_datasets(f)
            except OSError as e:
                error_msg = str(e)
                if "truncated file" in error_msg.lower():
                    print(
                        f"\n⚠️  Skipping truncated file: {h5_path.name}", file=sys.stderr
                    )
                    print(f"    Error: {error_msg}", file=sys.stderr)
                    continue
                elif "unable to open file" in error_msg.lower():
                    print(
                        f"\n⚠️  Skipping inaccessible file: {h5_path.name}",
                        file=sys.stderr,
                    )
                    print(f"    Error: {error_msg}", file=sys.stderr)
                    continue
                else:
                    print(
                        f"\n⚠️  Skipping file with OSError: {h5_path.name}",
                        file=sys.stderr,
                    )
                    print(f"    Error: {error_msg}", file=sys.stderr)
                    continue
            except Exception as e:
                print(
                    f"\n⚠️  Skipping file with unexpected error: {h5_path.name}",
                    file=sys.stderr,
                )
                print(f"    Error: {type(e).__name__}: {e}", file=sys.stderr)
                continue

            if not dsets:
                continue
            # Process only the first dataset if there are many, but always prioritize 'data'
            target_dsets = dsets[:1]
            for dname in target_dsets:
                rows = process_dataset(
                    h5_path=h5_path,
                    dset_name=dname,
                    threads=args.threads,
                    uniform_steps=args.uniform_steps,
                    max_sample=args.max_sample,
                    verify_limit=args.verify_limit,
                    outputs_dir=outputs_dir,
                    artifacts_dir=artifacts_dir,
                    aggregator_h5=aggregator,
                )
                all_rows.extend(rows)
                append_results_md(results_md, rows)
    finally:
        if aggregator is not None:
            aggregator.close()

    # Merge to CSV
    if all_rows:
        df = pd.DataFrame(all_rows)
        df.sort_values(
            ["file", "dataset", "mode", "step"], inplace=True, na_position="last"
        )
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(stats_csv, index=False)

    print(f"Done. Stats CSV: {stats_csv}")
    print(f"Results: {results_md}")
    print(f"Compressed outputs: {outputs_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
