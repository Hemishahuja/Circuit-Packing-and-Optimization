# Scientific Validity Notes

## What this implementation measures

- Packing feasibility via graph partitioning of coupling topology.
- Runtime ratio between packed execution and baseline repeated execution.
- Per-copy measurement distributions recovered through deterministic demultiplexing.
- Qubit utilization proxy: `(num_qubits_circuit * effective_copies) / backend_qubits`.

## Assumptions

- Zone boundaries are a practical proxy for reduced crosstalk pressure.
- Community detection yields useful placement partitions for the target topology.
- The baseline method (separate repeated runs) is an appropriate control comparison.

## Known limitations

- Current benchmark reports runtime speedup only; it does not compute statistical confidence intervals.
- Simulator-first mode does not model full hardware drift or queueing conditions.
- Fidelity deltas from real hardware are not recomputed automatically in CI.

## Recommendations for publication-quality experiments

- Run multiple seeded trials and report confidence intervals.
- Persist backend calibration metadata with each hardware run.
- Separate transpilation latency from queue+execution latency.
- Track per-copy fidelity metrics (Hellinger or TV distance) against baseline distributions.
