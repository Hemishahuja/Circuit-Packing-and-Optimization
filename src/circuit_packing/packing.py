from __future__ import annotations

from qiskit import ClassicalRegister, QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

from .placement import layout_distance_pass_manager, make_initial_layout, select_zone_qubits


def transpile_circuit_copies(
    circuit: QuantumCircuit,
    backend,
    coupling_map: list[tuple[int, int]],
    zones: list[list[int]],
    num_copies: int,
    optimization_level: int,
    seed_transpiler: int,
) -> list[QuantumCircuit]:
    """Transpile each copy to a distinct zone, preserving notebook behavior."""
    pass_manager = layout_distance_pass_manager(coupling_map)
    transpiled_circuits: list[QuantumCircuit] = []

    for zone_index in range(num_copies):
        copy_circuit = circuit.copy()
        zone_qubits = select_zone_qubits(zones, zone_index, copy_circuit.num_qubits)
        initial_layout = make_initial_layout(copy_circuit, zone_qubits)

        transpiled_qc = transpile(
            copy_circuit,
            backend=backend,
            coupling_map=CouplingMap(coupling_map),
            initial_layout=initial_layout,
            optimization_level=optimization_level,
            seed_transpiler=seed_transpiler,
        )
        transpiled_qc = pass_manager.run(transpiled_qc)
        transpiled_circuits.append(transpiled_qc)

    return transpiled_circuits


def compose_packed_circuit(
    transpiled_circuits: list[QuantumCircuit], backend_num_qubits: int, num_qubits_circuit: int
) -> QuantumCircuit:
    combined_circuit = QuantumCircuit(backend_num_qubits)

    for idx, circuit in enumerate(transpiled_circuits):
        classical_register = ClassicalRegister(num_qubits_circuit, f"creg{idx}")
        combined_circuit.add_register(classical_register)
        combined_circuit.compose(circuit, inplace=True)

    return combined_circuit
