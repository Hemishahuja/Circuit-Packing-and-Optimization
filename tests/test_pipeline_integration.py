from pathlib import Path

from circuit_packing.config import RunConfig
from circuit_packing.pipeline import run_pipeline


def test_pipeline_runs_in_simulator_mode() -> None:
    config = RunConfig(
        num_qubits_circuit=4,
        requested_copies=2,
        shots=128,
        use_simulator=True,
        output_dir=Path("outputs"),
    )
    result = run_pipeline(config)

    assert result.backend_name
    assert result.job_id is None
    assert len(result.separated_counts) >= 1
    assert result.metrics.packed_total_counts == config.shots
