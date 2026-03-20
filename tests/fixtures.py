from __future__ import annotations

from circuit_packing.circuits import create_sample_circuit


def sample_coupling_map() -> list[tuple[int, int]]:
    return [
        (0, 1),
        (1, 2),
        (2, 3),
        (4, 5),
        (5, 6),
        (6, 7),
    ]


def measured_sample_circuit():
    return create_sample_circuit(4)
