from __future__ import annotations

import time

from qiskit import transpile

from .circuits import create_sample_circuit
from .config import RunConfig
from .execution import get_backend
from .pipeline import run_pipeline


def run_baseline(config: RunConfig) -> dict:
    """Run non-packed baseline: independent executions per copy."""
    backend = get_backend(config)
    circuit = create_sample_circuit(config.num_qubits_circuit)

    started = time.time()
    total_counts = 0
    for _ in range(config.requested_copies):
        transpiled = transpile(
            circuit,
            backend=backend,
            optimization_level=config.optimization_level,
            seed_transpiler=config.seed_transpiler,
        )
        job = backend.run(transpiled, shots=config.shots)
        counts = job.result().get_counts()
        total_counts += sum(counts.values())

    elapsed = time.time() - started
    return {
        "requested_copies": config.requested_copies,
        "shots_per_copy": config.shots,
        "elapsed_seconds": elapsed,
        "total_counts": total_counts,
    }


def run_benchmark(config: RunConfig) -> dict:
    packed_result = run_pipeline(config)
    baseline_result = run_baseline(config)

    packed_elapsed = packed_result.elapsed_seconds
    baseline_elapsed = baseline_result["elapsed_seconds"]
    speedup = baseline_elapsed / packed_elapsed if packed_elapsed > 0 else 0.0

    return {
        "packed": packed_result.to_dict(),
        "baseline": baseline_result,
        "runtime_speedup": speedup,
    }
