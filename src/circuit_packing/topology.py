from __future__ import annotations


def resolve_coupling_map(backend) -> list[tuple[int, int]]:
    """Return backend coupling map; synthesize a chain for unconstrained simulators."""
    coupling_map = backend.configuration().coupling_map
    if coupling_map:
        return [tuple(edge) for edge in coupling_map]

    num_qubits = backend.configuration().n_qubits
    if num_qubits < 2:
        return []
    return [(index, index + 1) for index in range(num_qubits - 1)]
