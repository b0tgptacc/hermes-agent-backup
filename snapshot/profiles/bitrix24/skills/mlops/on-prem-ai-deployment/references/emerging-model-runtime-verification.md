# Verifying newly released local-model serving claims

Use this note when a model name or release is new enough that architecture, context, quantization, and runtime support may have changed.

## Evidence order

1. Read the official model card for parameter count, modality, native context, thinking controls, license, and recommended runtimes.
2. Read raw `config.json` for layer count, attention layout, head dimensions, dtype, maximum positions, vision components, and model type.
3. Query the official repository tree/API and sum exact weight-shard byte sizes programmatically. Do not substitute the parameter-count formula for checkpoint size.
4. Read the exact runtime recipe and quantization compatibility matrix for the model, runtime version, CUDA stack, and GPU generation.
5. Benchmark the immutable checkpoint and container digest on the actual GPU topology, context buckets, concurrency, and task corpus.

## Interpretation rules

- `parameters × bits / 8` is only a lower-bound sanity check; runtime memory also includes recurrent/KV state, activations, graphs, batching, vision components, and allocator headroom.
- Native long-context capability is not a safe production default. Start bounded and raise limits only after load and soak tests.
- Hybrid linear/full-attention models need architecture-aware state sizing; a standard full-attention KV formula may be incomplete.
- Two visible GPUs do not prove NVLink. Record `nvidia-smi topo -m`, NVLink status, and peer-to-peer bandwidth.
- A quantized checkpoint existing does not prove an efficient kernel path on the target GPU generation. Verify the runtime matrix and measure quality plus latency.
- When reasoning is on by default, disable both current-turn and preserved thinking for deterministic detector/classifier workloads, using the request shape documented by the selected runtime.
- Keep one conservative runtime as baseline and one challenger under an identical workload; do not compare vendor headline numbers from different protocols.

## Required benchmark outputs

Record p50/p95/p99 TTFT and end-to-end latency, request and token throughput, queue depth, peak VRAM, state/KV pressure, OOM/preemption, schema pass rate, per-entity privacy recall, false-block rate, and restart/overload behavior. Procurement and production GO decisions require these measured results, not model-file size alone.
