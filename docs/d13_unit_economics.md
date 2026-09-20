# Day 13 — Inference internals and unit economics

> Measured on the 5090, not estimated. No cloud GPU rental needed.

## Setup

- Model, quantisation, vLLM version, `--max-model-len`, tool calling on
- Mac side: same model in LM Studio, reached through LiteLLM

## Benchmark sweep

`vllm bench serve` at several concurrency levels.

| Concurrency | TTFT p50 | TTFT p95 | Inter-token latency | Output tok/s | KV cache used |
|---|---|---|---|---|---|
| 1 | | | | | |
| 4 | | | | | |
| 16 | | | | | |
| 64 | | | | | |

Where does throughput stop scaling, and what ran out first — KV cache,
compute, or memory bandwidth?

## KV cache arithmetic

`2 × n_layers × n_kv_heads × head_dim × bytes` = bytes per token.

- Per token:
- At your max context:
- How many concurrent sequences fit in 32 GB, and does that match what vLLM
  reported?

## LM Studio vs vLLM

Same model, same sweep, through LiteLLM.

| Concurrency | LM Studio tok/s | vLLM tok/s |
|---|---|---|
| 1 | | |
| 8 | | |
| 32 | | |

Where does continuous batching pull ahead? What does the Mac's unified memory
hold that 32 GB of VRAM cannot?

## Cost per million tokens

**Self-hosted:** measured throughput, power draw × your tariff, card amortised
over ~3 years, at some assumed utilisation.

| | Value |
|---|---|
| Sustained output tok/s | |
| Power draw under load (W) | |
| Electricity tariff (S$/kWh) | |
| Hardware amortised (S$/hour) | |
| Assumed utilisation | |
| **Cost per 1M output tokens** | |

**Cloud H100** at today's hourly price and the same measured throughput:

| | Value |
|---|---|
| Hourly price | |
| Throughput assumption | |
| **Cost per 1M output tokens** | |

**Claude** at list price, for the same work.

## The crossover

At what utilisation does self-hosting win? Plot it if that is clearer.

## The quality gap

Day 11 suite against the local model vs Claude. This is the real self-host
question, and the cost table is meaningless without it.

| | Claude | Local 8B–14B |
|---|---|---|
| pass^k (k=4) | | |
| Cost per task | | |
| p95 latency | | |

## Leader lens

Self-host vs API: data residency, cost crossover by utilisation, and the
quality gap on your own eval.
