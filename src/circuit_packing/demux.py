from __future__ import annotations


def demultiplex_counts(
    counts: dict[str, int],
    num_copies: int,
    num_qubits_circuit: int,
    backend_num_qubits: int,
) -> list[dict[str, int]]:
    if num_copies < 1:
        raise ValueError("num_copies must be >= 1.")
    if num_qubits_circuit < 1:
        raise ValueError("num_qubits_circuit must be >= 1.")

    separated_counts: list[dict[str, int]] = []
    for copy_index in range(num_copies):
        start_clbit = copy_index * num_qubits_circuit
        counts_per_copy: dict[str, int] = {}
        for outcome, count in counts.items():
            bits = outcome.zfill(backend_num_qubits)
            outcome_copy = bits[start_clbit : start_clbit + num_qubits_circuit]
            counts_per_copy[outcome_copy] = counts_per_copy.get(outcome_copy, 0) + count
        separated_counts.append(counts_per_copy)
    return separated_counts
