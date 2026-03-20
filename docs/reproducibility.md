# Reproducibility Guide

## Environment

- Python `>=3.10`
- Install dependencies from project metadata:

```bash
pip install -e ".[dev]"
```

## Deterministic knobs

The CLI exposes deterministic controls:

- `--seed-transpiler` (default `7`)
- `--shots`
- `--copies`
- `--optimization-level`

Example:

```bash
python -m circuit_packing run --copies 2 --shots 128 --seed-transpiler 7 --output-dir outputs
```

## Artifact outputs

Each run writes machine-readable artifacts:

- `outputs/run_report.json`
- `outputs/separated_counts.csv`

Benchmark mode writes:

- `outputs/benchmark_report.json`

## CI reproducibility

- `.github/workflows/ci.yml` runs lint/type/test gates.
- `.github/workflows/notebook-smoke.yml` performs simulator smoke execution.
