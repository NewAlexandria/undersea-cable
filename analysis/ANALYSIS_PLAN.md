## DAS24 data analysis and compression plan

Scope

- Analyze HDF5 datasets in `das24_data/` (2D numeric arrays typical of DAS)
- Produce dataset-level stats and histograms
- Compress ≥2 datasets using `daspack` (lossless for int32, uniform-quant lossy for float)
- Save artifacts (CSV stats, PNG histograms, compressed outputs) and a concise results report

Environment

- Python 3.9+
- Dependencies: numpy, h5py, pandas, matplotlib, tqdm
- Build/install local `daspack` Python module via `maturin develop --release` or fallback `pip install daspack-dev`

Data discovery

- Recursively find `*.h5`, `*.hdf5` under `das24_data/`
- For each file, probe for 2D numeric datasets. If unknown layout, traverse all datasets and infer by dtype and ndim
- Prefer dataset named `data` if present (common for DAS examples)

Sampling strategy

- For large arrays, sample rows/columns with stride to cap sample size (e.g., ≤ 2e6 elements) for quick stats/histograms
- Full stats for smaller arrays

Computed metrics per dataset

- Shape, dtype, nbytes (in-memory)
- Min, max, mean, std
- Percentiles: 0.1, 1, 50, 99, 99.9
- Optional: fraction of NaNs (if float)

Histograms

- For float: 128 bins over [p1, p99] clipped; for ints: min..max with at most 256 bins
- Save to `analysis/artifacts/hist_{file}_{dataset}.png`

Compression plan

- Lossless: if dtype is integer → cast to int32 and encode with `Quantizer.Lossless()`
- Lossy: if dtype is float → encode with `Quantizer.Uniform(step)` for steps in {0.5, 0.1} (configurable)
- Use `DASCoder(threads=4)` and blocksize default (1000, 1000) unless dataset is tiny
- Save outputs per source file to `analysis/outputs/`:
  - `{stem}__{dset}__lossless.dasp` or `__uniform{step}.dasp`
  - Also aggregate HDF5 `analysis/outputs/daspack_compressed.h5` with one group per dataset and an attribute table

Evaluation

- Compression factor = original_nbytes / compressed_bytes
- Report time to encode/decode (wall clock)
- For lossy: verify max abs error ≤ step/2 + 1e-12 on a sample; record max error

Deliverables

- `analysis/artifacts/stats.csv` (per dataset row)
- Histogram PNGs
- Compressed files in `analysis/outputs/`
- Results summary in `analysis/RESULTS.md`

Runbook

1. Set up venv and install deps
2. Build/install `daspack`
3. Run `python das24_analyze_compress.py --input das24_data --min-files 2 --uniform-steps 0.5 0.1 --threads 4`
4. Review `analysis/RESULTS.md` and artifacts
