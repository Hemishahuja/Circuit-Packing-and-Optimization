from __future__ import annotations

from qiskit import QuantumCircuit


def create_sample_circuit(num_qubits: int) -> QuantumCircuit:
    """Create the sample circuit used in the original notebook."""
    if num_qubits < 4:
        raise ValueError("Sample circuit expects at least 4 qubits.")

    circuit = QuantumCircuit(num_qubits)
    circuit.h(range(num_qubits))
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.cx(2, 3)
    circuit.barrier()
    circuit.measure_all()
    return circuit
