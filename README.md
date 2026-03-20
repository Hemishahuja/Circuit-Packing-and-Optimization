# QPU Spatial Multiplexing via Hardware-Aware Circuit Packing

Production-ready, simulator-first implementation of the Q-SITE Hackathon 2024 winning idea: pack multiple copies of a small circuit into disjoint QPU regions, execute in one job, and demultiplex results back per copy.

## What is in this repository now

- A real Python package under `src/circuit_packing` with separated modules for partitioning, placement, packing, execution, demultiplexing, metrics, and orchestration.
- A CLI for reproducible runs (`run`, `benchmark`, `validate`).
- Automated tests (`pytest`), linting (`ruff`), type-checking (`mypy`), and CI workflows.
- Structured output artifacts for reports (`outputs/run_report.json`, `outputs/benchmark_report.json`, `outputs/separated_counts.csv`).
- Notebook kept as a research artifact, while production logic lives in the package.

## Quickstart (Simulator-first)

### 1) Install

```bash
pip install -e ".[dev]"
```

### 2) Validate config

```bash
python -m circuit_packing validate --copies 2 --shots 128
```

### 3) Run packed execution (simulator default)

```bash
python -m circuit_packing run --copies 2 --shots 128 --output-dir outputs
```

### 4) Run baseline-vs-packed benchmark

```bash
python -m circuit_packing benchmark --copies 2 --shots 128 --output-dir outputs
```

## Hardware mode (optional)

Hardware support is available but opt-in. Never hardcode tokens in source or notebooks.

```bash
set IBM_QUANTUM_API_TOKEN=your_token_here
python -m circuit_packing run --use-hardware --backend-name ibm_sherbrooke
```

## Architecture

Pipeline stages:

1. Build coupling graph and detect zones (`partitioning.py`).
2. Score layouts and transpile per zone (`placement.py`, `packing.py`).
3. Compose packed circuit into one executable program (`packing.py`).
4. Execute and demultiplex counts per copy (`execution.py`, `demux.py`).
5. Emit run metrics and machine-readable artifacts (`metrics.py`, `io_utils.py`).

Detailed docs:

- `docs/architecture.md`
- `docs/reproducibility.md`
- `docs/validity.md`

## Development

```bash
ruff check .
mypy src
pytest
```

CI runs in GitHub Actions via:

- `.github/workflows/ci.yml`
- `.github/workflows/notebook-smoke.yml`

## Original context

This project was the first-place submission in the QPU Circuit Packing Challenge at [Q-SITE Hackathon 2024](https://qsite.ca/), hosted by Haiqu and IBM Quantum.

Original demonstration notebook: `qpu_circuit_packing.ipynb`.

Reference figure: `ibm_fez.jpg`.
