from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    """Runtime configuration for a single packing execution."""

    num_qubits_circuit: int = 4
    requested_copies: int = 9
    shots: int = 1024
    optimization_level: int = 3
    use_simulator: bool = True
    backend_name: str = "ibm_sherbrooke"
    ibm_channel: str = "ibm_quantum"
    ibm_instance: str | None = None
    output_dir: Path = Path("outputs")
    seed_transpiler: int = 7

    def validate(self) -> None:
        if self.num_qubits_circuit < 2:
            raise ValueError("num_qubits_circuit must be >= 2.")
        if self.requested_copies < 1:
            raise ValueError("requested_copies must be >= 1.")
        if self.shots < 1:
            raise ValueError("shots must be >= 1.")
        if not 0 <= self.optimization_level <= 3:
            raise ValueError("optimization_level must be in [0, 3].")
        if self.seed_transpiler < 0:
            raise ValueError("seed_transpiler must be >= 0.")
