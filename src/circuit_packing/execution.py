from __future__ import annotations

import os

from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService

from .config import RunConfig


def get_backend(config: RunConfig):
    if config.use_simulator:
        return AerSimulator()

    api_token = os.getenv("IBM_QUANTUM_API_TOKEN")
    if not api_token:
        raise ValueError(
            "IBM_QUANTUM_API_TOKEN is not set. "
            "Set it in your environment for hardware runs."
        )

    service = QiskitRuntimeService(
        channel=config.ibm_channel,
        token=api_token,
        instance=config.ibm_instance,
    )
    available_backends = service.backends(simulator=False, operational=True)
    for backend in available_backends:
        if backend.name == config.backend_name:
            return backend

    raise ValueError(f"Backend '{config.backend_name}' not found or not operational.")


def run_circuit(combined_circuit, backend, shots: int):
    transpiled_combined = transpile(combined_circuit, backend=backend)
    job = backend.run(transpiled_combined, shots=shots)
    return job, transpiled_combined
