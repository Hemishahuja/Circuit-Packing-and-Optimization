from __future__ import annotations

import time
from dataclasses import asdict, dataclass

from .circuits import create_sample_circuit
from .config import RunConfig
from .demux import demultiplex_counts
from .execution import get_backend, run_circuit
from .metrics import RunMetrics, build_metrics
from .packing import compose_packed_circuit, transpile_circuit_copies
from .partitioning import cap_copies_by_zone_count, detect_zones
from .topology import resolve_coupling_map


@dataclass(frozen=True)
class RunArtifacts:
    backend_name: str
    job_id: str | None
    raw_counts: dict[str, int]
    separated_counts: list[dict[str, int]]
    metrics: RunMetrics
    elapsed_seconds: float

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["metrics"] = self.metrics.to_dict()
        return payload


def run_pipeline(config: RunConfig) -> RunArtifacts:
    config.validate()

    started = time.time()
    backend = get_backend(config)

    sample_circuit = create_sample_circuit(config.num_qubits_circuit)
    coupling_map = resolve_coupling_map(backend)
    zones = detect_zones(coupling_map)
    effective_copies = cap_copies_by_zone_count(config.requested_copies, zones)
    if effective_copies < 1:
        raise ValueError("No valid zones available for packing on this backend.")

    transpiled_circuits = transpile_circuit_copies(
        circuit=sample_circuit,
        backend=backend,
        coupling_map=coupling_map,
        zones=zones,
        num_copies=effective_copies,
        optimization_level=config.optimization_level,
        seed_transpiler=config.seed_transpiler,
    )

    backend_num_qubits = backend.configuration().n_qubits
    combined_circuit = compose_packed_circuit(
        transpiled_circuits=transpiled_circuits,
        backend_num_qubits=backend_num_qubits,
        num_qubits_circuit=config.num_qubits_circuit,
    )

    job, _transpiled_combined = run_circuit(combined_circuit, backend, config.shots)
    result = job.result()
    counts = result.get_counts()
    separated_counts = demultiplex_counts(
        counts=counts,
        num_copies=effective_copies,
        num_qubits_circuit=config.num_qubits_circuit,
        backend_num_qubits=backend_num_qubits,
    )

    metrics = build_metrics(
        backend_qubits=backend_num_qubits,
        num_qubits_circuit=config.num_qubits_circuit,
        effective_copies=effective_copies,
        shots=config.shots,
        counts=counts,
    )
    elapsed_seconds = time.time() - started
    job_id = None if config.use_simulator else job.job_id()

    return RunArtifacts(
        backend_name=backend.name,
        job_id=job_id,
        raw_counts=counts,
        separated_counts=separated_counts,
        metrics=metrics,
        elapsed_seconds=elapsed_seconds,
    )
