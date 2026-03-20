from pathlib import Path

from circuit_packing.benchmark import run_benchmark
from circuit_packing.config import RunConfig


def test_benchmark_returns_runtime_summary() -> None:
    config = RunConfig(
        num_qubits_circuit=4,
        requested_copies=2,
        shots=64,
        use_simulator=True,
        output_dir=Path("outputs"),
    )
    benchmark = run_benchmark(config)
    assert "packed" in benchmark
    assert "baseline" in benchmark
    assert benchmark["runtime_speedup"] >= 0.0
