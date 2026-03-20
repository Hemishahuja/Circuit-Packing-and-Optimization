from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RunMetrics:
    packed_utilization: float
    qubits_used: int
    backend_qubits: int
    effective_copies: int
    shots: int
    packed_total_counts: int

    def to_dict(self) -> dict:
        return asdict(self)


def build_metrics(
    backend_qubits: int,
    num_qubits_circuit: int,
    effective_copies: int,
    shots: int,
    counts: dict[str, int],
) -> RunMetrics:
    qubits_used = num_qubits_circuit * effective_copies
    packed_utilization = qubits_used / backend_qubits if backend_qubits else 0.0
    packed_total_counts = sum(counts.values())
    return RunMetrics(
        packed_utilization=packed_utilization,
        qubits_used=qubits_used,
        backend_qubits=backend_qubits,
        effective_copies=effective_copies,
        shots=shots,
        packed_total_counts=packed_total_counts,
    )
