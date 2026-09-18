# vLLM on the RTX 5090 workstation, served to your Mac over Tailscale

**What you end up with:** three OpenAI-compatible servers on the workstation, reachable from the Mac Studio over Tailscale by name, protected by an API key *and* by binding only to the Tailscale interface, plus one LiteLLM endpoint on the Mac that fronts Claude, vLLM and LM Studio together.

```
Mac Studio                                   RTX 5090 workstation
─────────────────────────────                ─────────────────────────────────
harness / evals / Claude Code                vllm-chat    :8000  Qwen3-8B-FP8 (tools on)
LiteLLM proxy      :4000  ── Tailscale ──▶  vllm-embed   :8001  Qwen3-Embedding-0.6B
LM Studio (MLX)    :1234                     vllm-rerank  :8002  bge-reranker-v2-m3
Docker: OpenSearch, Postgres, Langfuse
```

Files in this folder: `docker-compose.yml`, `.env.example`, `litellm-config.yaml`.

**Time budget:** about an hour on Weekend 0, since you've run vLLM before; longer only if the driver needs upgrading.

---

## 1. Your setup

Two machines only: the **Mac Studio** (LM Studio, harness, LiteLLM, Docker services) and the **Ubuntu workstation** (vLLM on the 5090), joined by **Tailscale**. Everything below assumes that; no LAN port exposure, no router changes.

---

## 2. Check the workstation (you've run vLLM before, so this is mostly verification)

**2.1 Driver new enough for current images.** The current `vllm/vllm-openai` image is built on CUDA 13 with Blackwell kernels included. Your earlier vLLM setup may have used a CUDA 12.8-era driver, which is too old for it.

```bash
nvidia-smi          # header must show "CUDA Version: 13.x" (driver R580 or newer)
```

If it shows 12.x, upgrade to the newest `-open` driver (RTX 50-series needs NVIDIA's open kernel modules) and reboot:

```bash
ubuntu-drivers list
sudo apt install nvidia-driver-580-open     # or the newest -open offered
sudo reboot
```

**2.2 Docker can see the GPU.** If you ran vLLM in a Python venv before rather than Docker, install the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):

```bash
docker run --rm --gpus all ubuntu nvidia-smi    # if this works, skip the rest of 2.2

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

**2.3 Clear out the old setup.** Stop any old vLLM process or container (`nvidia-smi` should show no processes holding VRAM). Reuse your existing Hugging Face cache by pointing `HF_CACHE` in `.env` at it, so weights you already downloaded aren't fetched again.

**2.4 Tailscale on both machines.**

```bash
# Ubuntu workstation
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale ip -4          # e.g. 100.x.y.z  -> this is BIND_IP in .env
tailscale status         # note the machine name, e.g. "workstation"
```

On the Mac, install Tailscale from [tailscale.com/download](https://tailscale.com/download) and sign in to the same tailnet. With **MagicDNS** on (the default for new tailnets), the Mac reaches the workstation as `http://<machine-name>:8000`. This guide assumes the name is `workstation`; rename it in the Tailscale admin console or substitute your name everywhere.

**2.5 Make the binding survive reboots.** The containers bind to the Tailscale IP, which only exists once `tailscaled` is up. If Docker starts first after a reboot, the containers fail with "cannot assign requested address". Two small fixes:

```bash
# Let services bind to an address that isn't up yet
echo 'net.ipv4.ip_nonlocal_bind=1' | sudo tee /etc/sysctl.d/99-nonlocal-bind.conf
sudo sysctl --system

# Start Docker after Tailscale
sudo systemctl edit docker
#   add:
#   [Unit]
#   After=tailscaled.service
#   Wants=tailscaled.service
```

Test once with a reboot and `docker compose ps` before relying on it.

---

## 3. Size the models for 32 GB (your Day 5 formula, applied)

vLLM grabs a fixed fraction of VRAM per server (`--gpu-memory-utilization`). Inside that slice it loads weights, reserves room for activations and CUDA graphs, and gives **everything left to the KV cache**. So the question "how many tokens can I serve at once?" is exactly the KV arithmetic from Day 5.

Qwen3-8B: 36 layers, 8 KV heads, head dim 128. With a BF16 KV cache:

```
KV bytes per token = 2 (K and V) × 36 layers × 8 heads × 128 dim × 2 bytes
                   = 147,456 bytes ≈ 144 KiB per token
One full 32K-token context ≈ 32,768 × 144 KiB ≈ 4.5 GiB
```

Rough budget for the chat server at `0.70` of ~32 GB:

| Item | Approx. |
|---|---|
| Slice for the chat server (0.70 × ~32 GB) | ~22 GB |
| Qwen3-8B **FP8** weights | ~9 GB |
| Activations, CUDA graphs, overhead | ~2–3 GB |
| **Left for KV cache** | **~10 GB ≈ 70K tokens** |

That's two full 32K contexts, or dozens of short agent turns in parallel. With BF16 weights (~16 GB) the KV budget would collapse to a few thousand tokens, which is why the compose file starts with the FP8 checkpoint.

**Check your arithmetic against reality:** on startup vLLM logs the KV cache size in tokens and the maximum concurrency for your `--max-model-len`. Put both numbers, and your prediction, in the journal.

**Other options on 32 GB:**
- **Qwen3-14B-FP8:** fits only if the chat server gets most of the card (stop the embed and rerank servers, raise to ~0.90).
- **Larger MoE or 30B-class models:** need 4-bit (AWQ/GPTQ) checkpoints and a short `--max-model-len`. Try them after the basics work, not before.

---

## 4. Configure and start

On the workstation:

```bash
mkdir -p ~/vllm && cd ~/vllm
# copy docker-compose.yml and .env.example here, then:
cp .env.example .env
openssl rand -hex 32        # paste as VLLM_API_KEY in .env
nano .env                   # set BIND_IP to the output of: tailscale ip -4

docker compose pull
docker compose up -d
docker compose logs -f chat     # first start downloads weights and compiles; allow several minutes
```

**What the key chat flags do:**

| Flag | Why |
|---|---|
| `--enable-auto-tool-choice --tool-call-parser hermes` | Turns Qwen's tool-call tokens into OpenAI-style `tool_calls` (Qwen models use the Hermes format). Without these, tool calls come back as plain text. |
| `--reasoning-parser qwen3` | Separates Qwen3's thinking tokens from the answer. |
| `--default-chat-template-kwargs '{"enable_thinking": false}'` | Thinking is on by default for Qwen3; off gives faster, cheaper agent turns. Per-request you can turn it back on for comparisons. |
| `--max-model-len 32768` | Caps context so the KV cache isn't sized for a context you'll never use. |
| `--served-model-name qwen3-8b` | The short name clients use in the `model` field. |

---

## 5. Why this is safe

1. **Ports are published only on the Tailscale IP** (`${BIND_IP}:8000:8000`), so nothing is reachable from your home LAN, let alone the internet. Only devices signed in to your tailnet can connect.
2. **Don't rely on `ufw` for Docker ports.** Docker writes its own iptables rules that bypass `ufw`; the interface binding above is the control that actually works.
3. **The API key is a second layer, not the only one.** vLLM's `--api-key` / `VLLM_API_KEY` only authenticates the `/v1`, `/v2` and `/inference` paths; others such as `/invocations` are not authenticated ([vLLM security note](https://docs.vllm.ai/en/latest/usage/security.html)). That's fine behind Tailscale, but never port-forward these ports on your router.
4. **Optional:** tighten further with a [Tailscale ACL](https://tailscale.com/kb/1018/acls) that allows only the Mac to reach ports 8000–8002 on the workstation.

---

## 6. Test from the Mac

```bash
export VLLM_API_KEY=...   # same value as on the workstation

# Health (unauthenticated) and model list (authenticated)
curl http://workstation:8000/health
curl -H "Authorization: Bearer $VLLM_API_KEY" http://workstation:8000/v1/models

# Chat
curl http://workstation:8000/v1/chat/completions \
  -H "Authorization: Bearer $VLLM_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3-8b","messages":[{"role":"user","content":"Say hello in five words."}]}'

# Embeddings
curl http://workstation:8001/v1/embeddings \
  -H "Authorization: Bearer $VLLM_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3-embed","input":["MAS notice on technology risk"]}'

# Rerank
curl http://workstation:8002/v1/rerank \
  -H "Authorization: Bearer $VLLM_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"bge-rerank","query":"card dispute timelines","documents":["Disputes must be raised within 60 days.","Branch opening hours are 9 to 5."]}'
```

**Tool-calling check** (the one that matters for your harness):

```python
from openai import OpenAI
import os, json

client = OpenAI(base_url="http://workstation:8000/v1", api_key=os.environ["VLLM_API_KEY"])
tools = [{
    "type": "function",
    "function": {
        "name": "get_customer",
        "description": "Look up a bank customer by ID",
        "parameters": {"type": "object",
                       "properties": {"customer_id": {"type": "string"}},
                       "required": ["customer_id"]},
    },
}]
r = client.chat.completions.create(
    model="qwen3-8b",
    messages=[{"role": "user", "content": "Find customer C-1042"}],
    tools=tools,
)
print(json.dumps(r.choices[0].message.model_dump(), indent=2))
# Expect a populated tool_calls list, not the call written out as text.
```

---

## 7. One endpoint for everything: LiteLLM on the Mac

`litellm-config.yaml` puts Claude, the 5090 and LM Studio behind `http://localhost:4000`, so the harness only ever switches a model *name*. This is also the Day 13 gateway, set up early.

```bash
mise install         # pins litellm[proxy] in .mise.toml, project root
mise run litellm      # loads ANTHROPIC_API_KEY / VLLM_API_KEY from .env, no manual export
```

In the harness, point any OpenAI-compatible client at `http://localhost:4000` and use `model="local-qwen"`, `"claude-sonnet"` or `"lmstudio"`.

**LM Studio on the Mac:** start its server from the Developer tab (or `lms server start`); it listens on `http://localhost:1234/v1`. Copy the model id from `/v1/models` into `litellm-config.yaml`. LM Studio is ideal for trying models quickly and for MLX on Apple Silicon. vLLM is what you use when you need concurrency, which is exactly the Day 13 comparison: run the same load test against both and watch throughput diverge as concurrency rises.

---

## 8. Keep it stable

- **Pin the image** once everything works: replace `latest` in `.env` with the version tag you pulled (visible in the startup log). The workshop shouldn't break because `latest` moved mid-sprint.
- `restart: unless-stopped` brings servers back after a reboot.
- `/metrics` on each port exposes Prometheus metrics (queue depth, TTFT, KV-cache use). You'll scrape them on Day 13.

---

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `no kernel image is available for execution on the device` or "sm_120 is not compatible" | Old image or old driver | `docker compose pull` for a current image; confirm `nvidia-smi` shows CUDA 13.x. Earlier 2026 builds had this problem; it was [fixed upstream](https://github.com/vllm-project/vllm/issues/35432). |
| CUDA out of memory at startup | Fractions too high, or something else holds VRAM (LM Studio, a notebook) | Check `nvidia-smi`; lower `--gpu-memory-utilization` or `--max-model-len`; stop the embed/rerank servers to test the chat server alone. |
| Tool calls come back as plain text | Tool flags missing or wrong parser | Keep `--enable-auto-tool-choice --tool-call-parser hermes` for Qwen; other model families need their own parser ([tool calling docs](https://docs.vllm.ai/en/latest/features/tool_calling.html)). |
| `<think>` text in answers | Reasoning parser not set | Keep `--reasoning-parser qwen3`; disable thinking per request or server-wide. |
| Embed server rejects `--convert embed` | Flag name changed between versions | Remove it; `--runner pooling` alone auto-detects for Qwen3-Embedding in current builds ([pooling docs](https://docs.vllm.ai/en/latest/models/pooling_models/)). |
| Mac gets "connection refused" | Wrong `BIND_IP`, Tailscale down on one side, or MagicDNS name differs | `docker compose ps` on the workstation; `tailscale status` on both; `curl http://100.x.y.z:8000/health` from the Mac to bypass DNS. |
| Containers down after a reboot | Docker started before Tailscale had an IP | Apply section 2.5, then `docker compose up -d`. |
| First request very slow | `torch.compile` and CUDA graph capture on first start | Normal; the `vllm-cache` volume makes later starts faster. |

---

## 10. Where this plugs into the sprint

| Day | Uses |
|---|---|
| 1 | Tokenizer and chat template work stays on the Mac (Hugging Face `transformers`). |
| 3 | Llama Guard / Prompt Guard can run as a fourth vLLM service, or in LM Studio. |
| 6–7 | `vllm-embed` and `vllm-rerank` in the embedding and reranker shoot-outs. |
| 10 | Memory tools pointed at `local-embed` through LiteLLM. |
| 11 | Rerun the eval suite with `model="local-qwen"` vs `"claude-sonnet"`. |
| 13 | `vllm bench serve` against `:8000`; `/metrics`; LM Studio vs vLLM under concurrency; cost per million tokens on your own hardware. |
| 14 | garak / AgentDojo against the local model. |
