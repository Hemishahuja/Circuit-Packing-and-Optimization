from __future__ import annotations

import argparse
from pathlib import Path

from .benchmark import run_benchmark
from .config import RunConfig
from .io_utils import ensure_output_dir, write_counts_csv, write_json
from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="circuit-packing")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_flags(target_parser: argparse.ArgumentParser) -> None:
        target_parser.add_argument("--num-qubits-circuit", type=int, default=4)
        target_parser.add_argument("--copies", type=int, default=9)
        target_parser.add_argument("--shots", type=int, default=1024)
        target_parser.add_argument("--optimization-level", type=int, default=3)
        target_parser.add_argument("--seed-transpiler", type=int, default=7)
        target_parser.add_argument("--backend-name", default="ibm_sherbrooke")
        target_parser.add_argument("--use-hardware", action="store_true")
        target_parser.add_argument("--ibm-instance", default=None)
        target_parser.add_argument("--output-dir", default="outputs")

    run_parser = subparsers.add_parser("run", help="Execute packed circuit workflow.")
    add_common_flags(run_parser)

    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Compare packed vs baseline runtime.",
    )
    add_common_flags(benchmark_parser)

    validate_parser = subparsers.add_parser("validate", help="Validate configuration values only.")
    add_common_flags(validate_parser)

    return parser


def to_config(args: argparse.Namespace) -> RunConfig:
    return RunConfig(
        num_qubits_circuit=args.num_qubits_circuit,
        requested_copies=args.copies,
        shots=args.shots,
        optimization_level=args.optimization_level,
        use_simulator=not args.use_hardware,
        backend_name=args.backend_name,
        ibm_instance=args.ibm_instance,
        output_dir=Path(args.output_dir),
        seed_transpiler=args.seed_transpiler,
    )


def _write_run_outputs(
    config: RunConfig, artifacts: dict, separated_counts: list[dict[str, int]]
) -> None:
    output_dir = ensure_output_dir(config.output_dir)
    write_json(output_dir / "run_report.json", artifacts)
    write_counts_csv(output_dir / "separated_counts.csv", separated_counts)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = to_config(args)
    config.validate()

    if args.command == "validate":
        print("Configuration is valid.")
        return 0

    if args.command == "run":
        artifacts = run_pipeline(config)
        payload = artifacts.to_dict()
        _write_run_outputs(config, payload, artifacts.separated_counts)
        print(f"Backend: {artifacts.backend_name}")
        if artifacts.job_id:
            print(f"Job ID: {artifacts.job_id}")
        print(f"Elapsed seconds: {artifacts.elapsed_seconds:.3f}")
        print(f"Packed utilization: {artifacts.metrics.packed_utilization:.3f}")
        return 0

    if args.command == "benchmark":
        benchmark_result = run_benchmark(config)
        output_dir = ensure_output_dir(config.output_dir)
        write_json(output_dir / "benchmark_report.json", benchmark_result)
        print(f"Runtime speedup: {benchmark_result['runtime_speedup']:.3f}x")
        return 0

    raise ValueError(f"Unknown command '{args.command}'.")
