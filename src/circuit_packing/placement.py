from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap, PassManager
from qiskit.transpiler.passes import Layout2qDistance


def select_zone_qubits(
    zones: list[list[int]], zone_index: int, num_qubits_circuit: int
) -> list[int]:
    zone_qubits = zones[zone_index]
    if len(zone_qubits) < num_qubits_circuit:
        raise ValueError(
            f"Zone {zone_index} has {len(zone_qubits)} qubits, "
            f"but circuit requires {num_qubits_circuit}."
        )
    return zone_qubits[:num_qubits_circuit]


def make_initial_layout(circuit: QuantumCircuit, zone_qubits: list[int]) -> dict:
    return {circuit.qubits[idx]: zone_qubits[idx] for idx in range(len(zone_qubits))}


def layout_distance_pass_manager(coupling_map: list[tuple[int, int]]) -> PassManager:
    manager = PassManager()
    manager.append(Layout2qDistance(CouplingMap(coupling_map)))
    return manager
