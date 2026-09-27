# Dual-GPU local model evaluation

Use this procedure when comparing open-weight models for a two-GPU workstation or server.

## Required discovery

Capture exact memory per GPU, PCIe/SXM form factor, NVLink/P2P topology (`nvidia-smi topo -m`), system RAM, target context, concurrency, modalities, and latency objective. Do not treat two GPUs as one undifferentiated memory pool.

## Capacity model

Separate:

- checkpoint weights and quantization metadata;
- modality projectors/encoders;
- KV cache at the actual context and parallel-slot count;
- recurrent/SSM state for hybrid models;
- activations, CUDA graphs, workspaces, allocator reserve, and speculative drafter.

`parameters × bytes/weight` is only a lower bound. Sparse active parameters reduce compute but do not remove stored expert weights.

## TP versus independent replicas

- If the checkpoint cannot fit one card, use tensor parallelism.
- If it fits one card and requests are independent, benchmark one replica per GPU; this usually improves throughput and fault isolation.
- Use TP for higher precision, long context, or large batches.
- Without NVLink/P2P, prefer single-GPU quantized replicas where practical because TP collectives cross PCIe.
- Compare TP=2 against 2×TP1 on completed tasks per hour, not only token throughput.

## Hardware-aware quantization

Verify the serving framework's current hardware matrix. A checkpoint labeled FP8/FP4 does not guarantee native acceleration on every GPU generation; a backend may fall back to weight-only kernels. Record whether the format saves memory, improves throughput, or merely enables fit.

## Comparison table

For each model record total/active parameters, dense/MoE/hybrid architecture, exact checkpoint precision and size, modalities, context, license, language coverage, framework/parser requirements, per-card fit, TP fit, and evidence class (vendor, independent, or target-host measurement).

Reject candidates whose idealized weight size leaves no safe runtime headroom. Keep separate recommendations for each GPU-memory variant.

## Verification

Benchmark cold/warm TTFT, prefill/decode speed, peak memory at relevant contexts, concurrency 1/4/8, tool-call validity, domain-language quality, and OOM behavior. Use identical prompts, quantization class, reasoning budget, tools, timeout, and repeated trials. Prefer verified task completion and quality over raw tokens/s.
