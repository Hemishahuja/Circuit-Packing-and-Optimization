from circuit_packing.demux import demultiplex_counts


def test_demultiplex_counts_conserves_shots_per_copy() -> None:
    counts = {"00000000": 5, "11110000": 3, "10101010": 2}
    separated = demultiplex_counts(
        counts=counts,
        num_copies=2,
        num_qubits_circuit=4,
        backend_num_qubits=8,
    )

    total_shots = sum(counts.values())
    assert len(separated) == 2
    for copy_counts in separated:
        assert sum(copy_counts.values()) == total_shots
