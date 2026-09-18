# Agent Engineering Sprint — 3 Weeks + 1 Saturday

**Goal:** go from "has shipped LLM platforms on Bedrock" to "can build an agent harness from an empty file, prove it works with evals, pick and justify the production tooling, explain the economics, and defend it all to a regulator."

**Shape:** Week 1 builds the harness from scratch and instruments it. Week 2 builds production RAG with modern tools (two days), the MCP protocol by hand (two days), then memory on top of your retrieval stack. Week 3 adds evals, workflows vs agents, inference economics, security and governance, then ships a public capstone. A final Saturday turns it into an **AI-driven engineering culture playbook** for the teams you'll lead.

**Method: build it, then adopt it.** Agent mechanisms are built by hand first, because the harness is where your judgement matters. Commodity infrastructure (search engines, embedding models, parsers) is adopted directly and judged on your own data.

**Local-first:** everything runs on your Mac Studio and RTX 5090 workstation except the frontier model (Anthropic API) and a few optional managed services. AWS is optional; Azure is reference reading only. Each day marks where work runs: **[Mac]**, **[5090]**, **[API]**, **[AWS · optional]**, **[Azure · read]**.

**Throughline capstone:** a *Dispute & Ops Agent for a synthetic digital bank*. Every day adds one piece to a single repo.

> **Link note:** links point to the canonical page as of September 2026. Docs sites move; if a deep link 404s, search the exact title on that site. Where an Anthropic engineering post has no stable deep link here, the link goes to the [Engineering blog index](https://www.anthropic.com/engineering), where it's listed by title.

---

## Daily rhythm

| Time | Block | Purpose |
|---|---|---|
| 08:30–09:00 | **Quiz** | Answer 5 questions from yesterday's journal without looking. Anything you miss goes to the top of today. |
| 09:00–11:30 | **Read A** | Concept-first primary sources for today's mechanism. |
| 11:30–12:15 | Lunch, walk | Away from the screen. |
| 12:15–14:30 | **Build** | Hand-build the mechanism, plus one experiment that produces a *number*. |
| 14:30–15:30 | **Adopt** | Swap in the production tool and rerun the experiment. On days with no adopt slot, this hour is **code-reading** a reference repo. |
| 15:30–15:45 | Break | |
| 15:45–17:00 | **Read B** | One paper or deep post explaining *why* the mechanism works or fails. |
| 17:00–17:45 | **Journal** | Concept → one diagram → annotated code → the number → tool verdict. Nothing is done until it's in the journal. |
| Optional | Evening | Videos and optional chapters. Never at the expense of sleep. |

**Annotation convention:** `[SDK]` vendor SDK built-ins · `[H]` your harness logic · `[P]` protocol-defined behaviour (MCP, OTel) · `[T]` adopted third-party tools.

**Journal tool verdict** (after every adopt slot): Can it self-host, and where does data physically live? Does it work without its parent framework? What latency does it add per turn? Can its decisions be audited? Did it move *your* eval?

**Weekends:** Saturday = buffer, weekly quiz, blog draft. Sunday = off.

---

## Environment — who does what

| Machine / service | Role | Runs |
|---|---|---|
| **Mac Studio** [Mac] | Primary dev box | Your code, the harness, Claude Code, Docker containers (Postgres + pgvector, OpenSearch, Qdrant, Langfuse, Neo4j/FalkorDB for Graphiti), Docling parsing, open models via [LM Studio](https://lmstudio.ai) (MLX engine, OpenAI-compatible server on `:1234`), and the [LiteLLM](https://github.com/BerriAI/litellm) proxy on `:4000` that fronts Claude, vLLM and LM Studio |
| **RTX 5090 workstation** [5090] | Local inference server | [vLLM](https://github.com/vllm-project/vllm) serving an open chat model, [Qwen3-Embedding](https://huggingface.co/Qwen/Qwen3-Embedding-8B) and a reranker ([bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) or [Qwen3-Reranker](https://huggingface.co/Qwen/Qwen3-Reranker-4B)), Llama Guard / Prompt Guard for guardrails, red-team runs against local models |
| **Anthropic API** [API] | Frontier agent model | `claude-sonnet-5` agent, `claude-haiku-4-5-20251001` judges and bulk work, `claude-opus-5` for hard comparisons |
| **Managed APIs (no cloud account needed)** [API] | Managed comparisons | [Voyage](https://docs.voyageai.com/docs/embeddings) or [Cohere](https://docs.cohere.com/docs/embeddings) embeddings, Cohere Rerank, [LangSmith](https://docs.smith.langchain.com) free tier |
| **AWS** [AWS · optional] | Build-vs-buy comparisons only | Bedrock Guardrails (Day 3), Bedrock Knowledge Bases (Day 7). Skip entirely if you don't open an account; the local equivalents cover the learning. |
| **Azure** [Azure · read] | Reference architecture | Reading only; see the mapping table below |

**Connecting them:** run vLLM's OpenAI-compatible server on the 5090 and reach it from the Mac over [Tailscale](https://tailscale.com). Your harness then treats "local model" and "Claude" as two endpoints behind one interface, which Day 13's gateway formalises.

**Workstation setup:** follow the companion guide **`workstation/vllm-workstation-setup.md`** (with `docker-compose.yml`, `.env.example` and `litellm-config.yaml`). It covers the driver, the NVIDIA Container Toolkit, sizing models for 32 GB, binding to Tailscale safely, and testing from the Mac. If vLLM fights you on a given day, use LM Studio for that day rather than losing hours; don't let driver work eat the sprint.

### Local ↔ AWS ↔ Azure mapping (for Day 7 build-vs-buy and Day 14 governance)

| Capability | Local / open (what you build with) | AWS equivalent | Azure equivalent |
|---|---|---|---|
| Document parsing | [Docling](https://github.com/docling-project/docling) | [Textract](https://aws.amazon.com/textract/) | [Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview) |
| Hybrid search | [OpenSearch](https://opensearch.org/docs/latest/search-plugins/hybrid-search/) in Docker, or [Qdrant](https://qdrant.tech/documentation/concepts/hybrid-queries/), or [pgvector](https://github.com/pgvector/pgvector) + [ParadeDB](https://github.com/paradedb/paradedb) | Amazon OpenSearch Service | [Azure AI Search hybrid](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview) + [semantic ranker](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview) |
| Managed RAG | Your Day 6–7 pipeline | [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) | [Azure AI Search agentic retrieval](https://learn.microsoft.com/en-us/azure/search/search-agentic-retrieval-concept) |
| Guardrails | [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) + [Llama Guard / Prompt Guard](https://github.com/meta-llama/PurpleLlama) | [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) | [Content Safety Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection) + [groundedness detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness) |
| Agent runtime | Your harness, [LangGraph](https://github.com/langchain-ai/langgraph) | Bedrock AgentCore / Bedrock Agents | [Foundry Agent Service](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview) + [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) |
| LLM gateway | [LiteLLM](https://github.com/BerriAI/litellm) | Bedrock cross-region inference + API Gateway | [API Management AI gateway](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities) |
| Tracing | [Langfuse](https://langfuse.com/self-hosting) / [Phoenix](https://github.com/Arize-ai/phoenix) | CloudWatch + X-Ray | Application Insights (Foundry tracing) |

---

## Weekend 0 — Setup (≈4h)

- **Mac Studio [Mac]**
  - Python via [uv](https://docs.astral.sh/uv/); container runtime via [OrbStack](https://orbstack.dev) or Docker Desktop.
  - Repo `agent-sprint/` with `harness/`, `mcp_bank/`, `rag/`, `evals/`, `adapters/`, `journal/`.
  - `docker compose` for Postgres + pgvector, OpenSearch, Qdrant, and [self-hosted Langfuse](https://langfuse.com/self-hosting).
  - [LM Studio](https://lmstudio.ai) server running with one small model for quick local tests.
  - [LiteLLM](https://github.com/BerriAI/litellm) proxy with `litellm-config.yaml` from the workstation guide.
- **5090 workstation [5090]**
  - Linux, current NVIDIA driver, CUDA 12.8+, Docker + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
  - vLLM chat, embedding and reranker servers via the companion guide (`workstation/vllm-workstation-setup.md`); confirm the Mac can reach all three and that tool calls come back as structured `tool_calls`.
  - [Tailscale](https://tailscale.com) on both machines.
- **Accounts [API]:** Anthropic API key with a hard spend limit; [LangSmith](https://smith.langchain.com) free account; Voyage and Cohere API keys (trial tiers are enough). AWS only if you want the optional comparisons.
- **Clone the reference repos:**
  - [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) (root `s01`–`s17` track)
  - [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) · [huggingface/smolagents](https://github.com/huggingface/smolagents) · [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks)
  - [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) · [openai/openai-agents-python](https://github.com/openai/openai-agents-python) · [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)
  - [openai/codex](https://github.com/openai/codex) · [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- **Synthetic bank** in SQLite: `customers`, `accounts`, `transactions` (with a free-text `merchant_memo` you'll weaponise on Day 3), `disputes`, `policies`.
- **Dogfood from day zero:** create `CLAUDE.md` and [`AGENTS.md`](https://agents.md) in the repo. Every time you correct your coding agent twice for the same thing, add a line. By Day 16 that file is first-hand evidence of what a team context file needs.
- **Bookmark:** [Picrew/awesome-agent-harness](https://github.com/Picrew/awesome-agent-harness) and [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) for lookups.
- **Optional primer:** [A Visual Guide to LLM Agents](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-llm-agents) (Alammar & Grootendorst).

---

## At a glance

| Day | Focus | By evening you have |
|---|---|---|
| 1 | [The loop, from tokens up](#day-01) | A working agent loop in under 80 lines, and the chat template that makes tool calls possible |
| 2 | [Tools as the agent–computer interface](#day-02) | Five tools, parallel calls, and a table showing how much tool descriptions matter |
| 3 | [Boundaries: permissions, hooks, guardrails, injection](#day-03) | Permission engine, audit log, and measured guardrail results against injection |
| 4 | [Planning, subagents, and the multi-agent debate](#day-04) | Single-agent vs multi-agent numbers on the same task |
| 5 | [Context engineering + tracing](#day-05) | Skills, compaction, prompt caching, and tracing into Langfuse |
| 6 | [Production RAG I: ingestion, structured extraction, hybrid indexing](#day-06) | Parsed, extracted, hybrid-indexed MAS corpus and a hand-labelled golden set |
| 7 | [Production RAG II: reranking, citations, guardrails, lifecycle](#day-07) | Reranked, cited, entitlement-filtered answers with supersession and deletion proven |
| 8 | [MCP I: the protocol by hand](#day-08) | An MCP server and client written by hand, passing the Inspector |
| 9 | [MCP II: remote, secured, production-shaped](#day-09) | MCP over HTTP with scopes and a tool-poisoning defence |
| 10 | [Memory and persistent tasks](#day-10) | A MemoryStore interface over two memory backends, with a PDPA deletion test |
| 11 | [Evals (the most important day)](#day-11) | `make eval` prints a pass^k scorecard |
| 12 | [Workflows vs agents; the framework landscape](#day-12) | The dispute flow built as a workflow and as an agent, plus a decision memo |
| 13 | [Inference internals & unit economics (on your own 5090)](#day-13) | Your own throughput and cost-per-token numbers, local vs API |
| 14 | [Security, red-teaming, governance](#day-14) | Red-team results and a two-page governance mapping |
| 15 | [Integrate, ship, narrate](#day-15) | A published repo, README, demo and blog post |
| 16 | [Building an AI-driven engineering culture (EM track)](#day-16) | A team plugin, an SDD trial, and a two-page culture playbook |

---

## Week 1 — The loop and the harness

<a id="day-01"></a>
### Day 1 — The loop, from tokens up

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic; workflow vs agent taxonomy, the five workflow patterns<br>• [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Lilian Weng; planning, memory, tool use<br>• [Agents](https://huyenchip.com/2025/01/07/agents.html) — Chip Huyen<br>• learn-claude-code: [root README](https://github.com/shareAI-lab/learn-claude-code) + [`s01_agent_loop`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s01_agent_loop) |
| 12:15 | **Build**<br>`API` `Mac` | • Call the [Messages API](https://docs.claude.com/en/api/messages) with tools using raw `httpx`, no SDK. Print `tool_use`, `stop_reason` and `tool_result` with `tool_use_id`. Reference: [tool use overview](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview).<br>• **nanochat bridge:** load the [Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) tokenizer and call `apply_chat_template(messages, tools=...)` ([chat templating docs](https://huggingface.co/docs/transformers/main/en/chat_templating)). Print the rendered string and token IDs, then hand-write the tool-call parser.<br>• Rewrite the `s01` loop from memory in under 80 lines. |
| 14:30 | **Code-read** | • [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) — an agent of about 100 lines. List what it omits compared with learn-claude-code. |
| 15:45 | **Read B** | • [ReAct](https://arxiv.org/abs/2210.03629) (Yao et al., 2022), §1–3<br>• [Toolformer](https://arxiv.org/abs/2302.04761) (Schick et al., 2023), intro and method — the *model* half of "model + harness" |
| — | **Optional evening** | • [Building Applications with AI Agents](https://www.oreilly.com/library/view/building-applications-with/9781098176495/) (Albada, O'Reilly) — opening chapters on agents vs workflows |

> **Leader lens:** when a vendor says "we built an agent," which half did they build?


<a id="day-02"></a>
### Day 2 — Tools as the agent–computer interface

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — Anthropic<br>• [SWE-agent](https://arxiv.org/abs/2405.15793) — the Agent-Computer Interface section<br>• learn-claude-code [`s02_tool_use`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s02_tool_use)<br>• Albada, the chapter on tools |
| 12:15 | **Build**<br>`API` `Mac` | • Dispatch map with 5 tools: `read_file`, `write_file`, `grep`, `run_sql`, `http_get`. Parallel calls; errors returned as observations.<br>• **Experiment:** 10 tasks × 3 tool-description variants (terse / good / misleading) → success rate and tokens. |
| 14:30 | **Adopt** | • Structured outputs: [Claude structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs) with [Pydantic](https://docs.pydantic.dev) models, or [Instructor](https://python.useinstructor.com). Measure schema-violation rate against your hand-parsed JSON. |
| 15:45 | **Read B** | • [CodeAct: Executable Code Actions Elicit Better LLM Agents](https://arxiv.org/abs/2402.01030) (Wang et al., 2024)<br>• [Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) docs |
| — | **Optional evening** | • [smolagents](https://github.com/huggingface/smolagents) source · [claude-cookbooks](https://github.com/anthropics/claude-cookbooks) tool-use notebooks |

> **Leader lens:** tool design is API design for a new kind of consumer. Who owns tool quality in your org?


<a id="day-03"></a>
### Day 3 — Boundaries: permissions, hooks, guardrails, injection

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • learn-claude-code [`s03_permission`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s03_permission) and [`s04_hooks`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s04_hooks)<br>• [The Lethal Trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) — Simon Willison<br>• [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) — LLM01 (Prompt Injection), LLM06 (Excessive Agency)<br>• *Beyond Permission Prompts* and *Claude Code Auto Mode* — both on the [Anthropic Engineering blog](https://www.anthropic.com/engineering) |
| 12:15 | **Build**<br>`API` `Mac` | • Permission engine (allow / deny / ask); `PreToolUse` / `PostToolUse` hooks writing an append-only JSONL audit log.<br>• **Attack:** plant instructions in a `merchant_memo`. Defend with prompt hardening, then hook filtering, then architectural separation. Record which actually holds. |
| 14:30 | **Adopt**<br>`5090` | • [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) ([docs](https://docs.nvidia.com/nemo/guardrails/)) with Llama Guard and Prompt Guard from [PurpleLlama](https://github.com/meta-llama/PurpleLlama) served on the 5090. Rerun the attack suite: attack success rate *and* added latency per turn.<br>• Cloud reference: [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) [AWS · optional] · [Azure Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection) [Azure · read] |
| 15:45 | **Read B** | • [CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) (Google DeepMind, 2025)<br>• [Design Patterns for Securing LLM Agents against Prompt Injections](https://arxiv.org/abs/2506.08837) (Beurer-Kellner et al., 2025) |
| — | **Optional evening** | • [Not What You've Signed Up For](https://arxiv.org/abs/2302.12173) (Greshake et al., 2023) — the founding indirect-injection paper<br>• [luisalima/agentic-security](https://github.com/luisalima/agentic-security) — notebooks: vulnerability first, then the defence |

> **Leader lens:** which actions are irreversible? Those need a hard gate or a human, never just a prompt or a rail.


<a id="day-04"></a>
### Day 4 — Planning, subagents, and the multi-agent debate

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • learn-claude-code [`s05_todo_write`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s05_todo_write) and [`s06_subagent`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s06_subagent)<br>• [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) — Anthropic<br>• [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) — Cognition (read back-to-back with the Anthropic post; they disagree on purpose) |
| 12:15 | **Build**<br>`API` `Mac` | • TodoWrite tool; subagent with a fresh `messages[]`.<br>• **Experiment:** single agent vs orchestrator + 3 subagents on one investigation task — tokens, wall time, and quality on a rubric you write first. |
| 14:30 | **Code-read** | • Compare the context boundary in `s06` with Albada's orchestration chapter. |
| 15:45 | **Read B** | • [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) (Cemri et al., 2025) — the MAST failure taxonomy; keep it for Day 11<br>• [Reflexion](https://arxiv.org/abs/2303.11366) (Shinn et al., 2023) |

> **Leader lens:** multi-agent buys parallelism and isolation for roughly N× tokens. When is that worth it?


<a id="day-05"></a>
### Day 5 — Context engineering + tracing

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic<br>• [Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Anthropic<br>• learn-claude-code [`s07_skill_loading`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s07_skill_loading) and [`s08_context_compact`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s08_context_compact) |
| 12:15 | **Build**<br>`API` `Mac` | • Skill loader (catalog → on demand); four-stage compaction.<br>• **Experiment:** a 40-turn task at 3 context budgets, logging prompt-cache hit rate.<br>• **nanochat bridge:** KV bytes per token = `2 × n_layers × n_kv_heads × head_dim × bytes`. |
| 14:30 | **Adopt**<br>`Mac`<br>*tracing, from today onward* | • Instrument with [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) → [self-hosted Langfuse](https://langfuse.com/self-hosting) (or [Phoenix](https://github.com/Arize-ai/phoenix)); dual-export to [LangSmith](https://docs.smith.langchain.com). Every run from now on leaves traces you'll mine on Day 11. |
| 15:45 | **Read B** | • [Lost in the Middle](https://arxiv.org/abs/2307.03172) (Liu et al., 2023)<br>• Microsoft's *Context Engineering for Reliable AI Agents: Lessons from Building Azure SRE Agent* — files + `grep` beat 100+ bespoke tools. Link via the [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) list. |
| — | **Optional evening** | • [claude-cookbooks](https://github.com/anthropics/claude-cookbooks) prompt-caching notebooks |

> **Leader lens:** cost per task is set more by context policy than by model choice. Where may traces containing customer data legally live?


<a id="saturday-buffer"></a>
### Saturday — Buffer

| Time | Block | What to do |
|---|---|---|
| — | **Catch-up** | • finish overruns. Optional: [E2B](https://github.com/e2b-dev/E2B) or a local Docker + [gVisor](https://gvisor.dev) sandbox for shell tools; try escaping your allow-list inside and outside it. |
| — | **Quiz** | • Week 1, from the journal. |
| — | **Prep for Monday** | • re-read your *Hands-On LLMs* Ch 8 notes; download ~50 public MAS notices and guidelines as PDFs from [mas.gov.sg](https://www.mas.gov.sg/regulation). |
| — | **Read** | • [What We Learned from a Year of Building with LLMs](https://applied-llms.org) — all three parts. |
| — | **Write** | • blog draft #1, *"The loop is 30 lines. The harness is everything else."* |
| — | **Optional** | • a lecture from the [Berkeley LLM Agents MOOC](https://llmagents-learning.org) · [decodingai-magazine/building-a-coding-agent-from-scratch-course](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course) as a second from-scratch take. |

---

## Week 2 — Retrieval, protocols, memory

RAG gets two production-focused days with modern tools; the only thing built by hand is the evaluation harness (golden set and retrieval metrics), because it encodes what "correct" means for your documents. MCP gets two days built by hand first, then the SDK. Memory comes last, because it's retrieval over the agent's own history.

<a id="day-06"></a>
### Day 6 — Production RAG I: ingestion, structured extraction, hybrid indexing

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A**<br>*concepts, 1.5h* | • [AI Engineering](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) (Chip Huyen), **Ch 6**, the RAG half — what BM25's `k1` and `b` do, why dense and sparse retrieval fail differently, how Reciprocal Rank Fusion combines them<br>• [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — Anthropic |
| 10:30 | **Read A**<br>*tools, 1h* | • [Docling docs](https://docling-project.github.io/docling/) — layout-aware parsing: tables, reading order, section hierarchy<br>• [OpenSearch hybrid search](https://opensearch.org/docs/latest/search-plugins/hybrid-search/) — BM25 + k-NN with a normalisation pipeline<br>• Alternatives: [Qdrant hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) · [pgvector](https://github.com/pgvector/pgvector) + [ParadeDB `pg_search`](https://github.com/paradedb/paradedb) |
| 12:15 | **Build**<br>`Mac` `5090` `API` | • **Parse** the MAS corpus with Docling [Mac]; compare one table-heavy PDF against [Claude's native PDF support](https://docs.claude.com/en/docs/build-with-claude/pdf-support) [API].<br>• **Structured extraction:** a Pydantic schema per document (issuer, notice number, effective date, applicability, superseded-by, obligations), filled via [structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs) and validated. Failures go to a review queue, not the index.<br>• **Structure-aware chunks:** split on parsed sections; each chunk carries `doc_id`, version, section path, page, character offsets, effective date and access level.<br>• **Index** into OpenSearch (Docker on the Mac) with metadata as filterable fields.<br>• **Golden set, by hand:** 30 questions with the correct chunk IDs, plus a ~30-line script for recall@5 and MRR. |
| 14:30 | **Adopt**<br>*embedding shoot-out on your golden set* | • Local [5090]: [Qwen3-Embedding](https://huggingface.co/Qwen/Qwen3-Embedding-8B) or [BGE-M3](https://huggingface.co/BAAI/bge-m3), served via vLLM or [text-embeddings-inference](https://github.com/huggingface/text-embeddings-inference)<br>• Managed [API]: [Voyage](https://docs.voyageai.com/docs/embeddings) or [Cohere Embed](https://docs.cohere.com/docs/embeddings)<br>• Run BM25-only, dense-only and hybrid; nudge `k1`/`b` in OpenSearch to feel what they do. |
| 15:45 | **Read B** | • Examine every golden-set miss: parsing, chunk boundary, vocabulary mismatch, or a bad question?<br>• Skim [BEIR](https://arxiv.org/abs/2104.08663) (Thakur et al., 2021) on why BM25 remains a strong baseline. |
| — | **Optional evening** | • [Stop Saying RAG Is Dead](https://hamel.dev/blog/) — Hamel Husain<br>• Parser alternatives: [Unstructured](https://github.com/Unstructured-IO/unstructured) · [Azure Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview) [Azure · read] · [Textract](https://aws.amazon.com/textract/) [AWS · optional] |

> **Leader lens:** most "the LLM hallucinated" incidents are really parsing or retrieval failures. Measure retrieval separately from generation.


<a id="day-07"></a>
### Day 7 — Production RAG II: reranking, citations, guardrails, lifecycle

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • [Citations](https://docs.claude.com/en/docs/build-with-claude/citations) — Anthropic docs<br>• NeMo Guardrails [docs](https://docs.nvidia.com/nemo/guardrails/) — retrieval rails<br>• [Microsoft Presidio](https://github.com/microsoft/presidio) — PII detection and redaction<br>• [Ragas](https://docs.ragas.io) — faithfulness, context precision and recall<br>• Cloud reference: [Bedrock contextual grounding check](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html) [AWS · optional] · [Azure groundedness detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness) [Azure · read] |
| 12:15 | **Build**<br>`Mac` `5090` `API` | • **Rerank** hybrid top 50 → top 5 with [bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) or [Qwen3-Reranker](https://huggingface.co/Qwen/Qwen3-Reranker-4B) on the 5090; compare with [Cohere Rerank](https://docs.cohere.com/docs/rerank-overview) [API]. Measure recall *and* latency.<br>• **Contextual retrieval:** LLM-written chunk context vs Voyage's contextual chunk embeddings; compare on the golden set.<br>• **Citations:** pass chunks as documents with the Citations API; map each citation to document, page and section.<br>• **Guardrails:** entitlement filter *in the query* (prove a restricted chunk never reaches the prompt); Presidio redaction at ingestion; injection scanning of retrieved chunks; a grounding check; an explicit "not found in policy" answer below an evidence threshold.<br>• **Agentic RAG:** expose `search_policy(query, filters)` as a harness tool with effective-date and issuer filters. |
| 14:30 | **Adopt** | • **Lifecycle:** re-ingest an updated notice and prove the superseded version stops being cited; delete a document and prove it's gone from index and caches (PDPA).<br>• Score end to end with [Ragas](https://docs.ragas.io).<br>• **Build vs buy:** [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) on the same corpus [AWS · optional], *or* read [Azure AI Search agentic retrieval](https://learn.microsoft.com/en-us/azure/search/search-agentic-retrieval-concept) [Azure · read] and fill in the mapping table. |
| 15:45 | **Read B** | • *AI Engineering*, **Ch 6**, the agents half<br>• [Self-RAG](https://arxiv.org/abs/2310.11511) (Asai et al., 2023), intro |

> **Leader lens:** RAG vs long context vs fine-tuning, with your own numbers. Entitlements, supersession and deletion are what auditors test first.


<a id="day-08"></a>
### Day 8 — MCP I: the protocol by hand

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • [JSON-RPC 2.0 specification](https://www.jsonrpc.org/specification) — short; requests, responses, notifications, errors<br>• [MCP specification](https://modelcontextprotocol.io/specification/latest) — base protocol, [lifecycle](https://modelcontextprotocol.io/specification/latest/basic/lifecycle), server features (tools, resources, prompts), stdio in [transports](https://modelcontextprotocol.io/specification/latest/basic/transports)<br>• learn-claude-code [`s14_mcp_plugin`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s14_mcp_plugin) |
| 12:15 | **Build**<br>`Mac`<br>*no SDK* | • **Server over stdio** (~150 lines): newline-delimited JSON on stdin; handle `initialize`, `notifications/initialized`, `tools/list` (JSON Schema `inputSchema`), `tools/call` (content blocks, `isError`). Log to **stderr only**. Tools: `get_customer`, `list_transactions`.<br>• **Resources:** `resources/list` and `resources/read` over your policy corpus.<br>• **Client by hand:** spawn the server, handshake, translate MCP tool schemas into Anthropic tool definitions, route `tool_use` → `tools/call`. Your harness is now an MCP host.<br>• **Wire-tap:** log every message; draw the sequence diagram in the journal. |
| 14:30 | **Build (cont.)**<br>*conformance check* | • Point the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) at your server. If it can list and call your tools, you've implemented the protocol correctly. |
| 15:45 | **Read B** | • learn-claude-code [`s15_integrated_harness`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s15_integrated_harness)<br>• [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) and [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) — Anthropic |

> **Leader lens:** capability negotiation and protocol versioning are what let a bank run a catalogue of servers owned by different teams.


<a id="day-09"></a>
### Day 9 — MCP II: remote, secured, production-shaped

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • MCP spec: [Streamable HTTP transport](https://modelcontextprotocol.io/specification/latest/basic/transports), [Authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization), [Security Best Practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices)<br>• [MCP tool poisoning attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) — Invariant Labs |
| 12:15 | **Build**<br>`Mac` | • **Streamable HTTP by hand** (Starlette or FastAPI): POST for JSON-RPC, streamed responses, session header handling.<br>• **Gated write tool:** `open_dispute`, requiring human approval in your harness.<br>• **Scopes:** bearer tokens with `disputes:read` / `disputes:write` checked server-side; walk through the OAuth 2.1 flow on paper.<br>• **Attack:** a malicious second server with instructions hidden in a tool description, and one that changes its description after approval (rug-pull). Defend by pinning a hash of each approved tool definition. |
| 14:30 | **Adopt** | • Rewrite with [FastMCP](https://github.com/jlowin/fastmcp) or the [official Python SDK](https://github.com/modelcontextprotocol/python-sdk); count lines against yours.<br>• Connect to Claude Desktop or Claude Code. Browse [reference servers](https://github.com/modelcontextprotocol/servers). |
| 15:45 | **Read B** | • [A2A protocol](https://a2a-protocol.org) — agent-to-agent vs agent-to-tool<br>• [MCP Registry](https://github.com/modelcontextprotocol/registry) — how server catalogues are governed |
| — | **Optional evening** | • [AI Agents with MCP](https://www.oreilly.com/library/view/ai-agents-with/9798341639546/) (O'Reilly) — server design and security chapters |

> **Leader lens:** who approves a new MCP server, pins its version, and owns its scopes? That's your agent platform's governance model in one question.


<a id="day-10"></a>
### Day 10 — Memory and persistent tasks

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • learn-claude-code [`s09_memory`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s09_memory) and [`s10_task_system`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s10_task_system)<br>• [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Anthropic<br>• [MemGPT](https://arxiv.org/abs/2310.08560) (Packer et al., 2023), §1–3 |
| 12:15 | **Build**<br>`Mac` `5090` | • Memory: selection → extraction → consolidation, reusing your Day 6 embedding and index setup.<br>• File-backed task DAG with `blockedBy`; kill mid-task and prove it resumes.<br>• Define a `MemoryStore` interface. |
| 14:30 | **Adopt**<br>`Mac`<br>*two of these behind `MemoryStore`, all self-hostable* | • [Mem0](https://github.com/mem0ai/mem0) · [Graphiti](https://github.com/getzep/graphiti) (Zep's temporal knowledge graph; needs Neo4j or FalkorDB in Docker) · [Letta](https://github.com/letta-ai/letta) · [LangMem](https://github.com/langchain-ai/langmem)<br>• Test a temporal query ("customer changed address last month — which one is current?") and a PDPA "forget this customer" deletion. |
| 15:45 | **Read B** | • [Generative Agents](https://arxiv.org/abs/2304.03442) (Park et al., 2023) — retrieval by recency, importance, relevance<br>• [Mem0 paper](https://arxiv.org/abs/2504.19413) — read critically; vendor benchmarks are contested |
| — | **Optional evening** | • *Harness Design for Long-Running Application Development* — [Anthropic Engineering](https://www.anthropic.com/engineering)<br>• [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) — the agent memory lesson |

> **Leader lens:** memory is data retention. What may the agent remember about a customer under PDPA, and how do you prove deletion?


<a id="saturday-buffer-eval-prep"></a>
### Saturday — Buffer + eval prep

| Time | Block | What to do |
|---|---|---|
| — | **Catch-up** | • RAG and MCP overruns first; they matter more than anything optional. |
| — | **Quiz** | • Week 2 — the JSON-RPC handshake from memory; BM25's `k1` and `b` in plain words. |
| — | **Prep for Monday** | • [τ-bench paper](https://arxiv.org/abs/2406.12045) on pass^k, and code-read [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) for scenario format and end-state checks. |
| — | **Write** | • blog draft #2, *"Production RAG in a bank: citations, entitlements, and the documents that change under you."* |
| — | **Optional** | • learn-claude-code [`s11`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s11_background_tasks), [`s12`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s12_cron_scheduler), [`s13`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s13_agent_teams) · [walkinglabs/learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) — *Frontier Harness Design Breakdowns* |

---

## Week 3 — Evals, workflows, economics, governance, capstone

<a id="day-11"></a>
### Day 11 — Evals (the most important day)

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • Hamel Husain: [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) · [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/) · [LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)<br>• *Demystifying Evals for AI Agents* — [Anthropic Engineering](https://www.anthropic.com/engineering)<br>• *AI Engineering* (Chip Huyen), **Ch 3–4** |
| 12:15 | **Build**<br>`Mac` `API` | • Pull 50 traces from Langfuse (collected since Day 5) → open coding → failure taxonomy, seeded with MAST from Day 4.<br>• 20 τ-bench-style scenarios with expected DB end-state, including RAG questions (reuse the Day 6 golden set) and MCP tool flows.<br>• Code assertions first, then one LLM judge validated against your labels (TPR/TNR). pass^k with k=4.<br>• **Done when `make eval` prints a scorecard.** |
| 14:30 | **Adopt** | • [LangSmith evaluation](https://docs.smith.langchain.com/evaluation) experiments · [Inspect](https://inspect.aisi.org.uk) (UK AISI) as a local alternative<br>• [hamelsmu/evals-skills](https://github.com/hamelsmu/evals-skills) in Claude Code — run its eval-audit against your pipeline |
| 15:45 | **Read B** | • [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) (Zheng et al., 2023)<br>• [Who Validates the Validators?](https://arxiv.org/abs/2404.12272) (Shankar et al., 2024)<br>• *Quantifying Infrastructure Noise in Agentic Coding Evals* — [Anthropic Engineering](https://www.anthropic.com/engineering) |
| — | **Optional evening** | • *Evals for AI Engineers* (Husain et al., O'Reilly) — see [hamel.dev](https://hamel.dev)<br>• [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/) — Eugene Yan, evals section |

> **Leader lens:** no eval, no launch. The eval set *is* the spec.


<a id="day-12"></a>
### Day 12 — Workflows vs agents; the framework landscape

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • learn-claude-code [`s16_workflow_runtime`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s16_workflow_runtime) and [`s17_goal_loop`](https://github.com/shareAI-lab/learn-claude-code/tree/main/s17_goal_loop)<br>• [LangGraph](https://github.com/langchain-ai/langgraph) docs — the persistence, durable execution and interrupts pages<br>• [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/) [Azure · read] + skim the framework and design-pattern lessons of [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) |
| 12:15 | **Build**<br>`Mac` `API` | • Card-dispute flow twice: (a) LangGraph workflow with LLM nodes + an interrupt for approval, (b) your free agent. Run the Day 11 suite on both: pass^k, cost, latency, auditability. |
| 14:30 | **Adopt**<br>*30-minute ports of one tool and one flow to two of:* | • [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview) ([Python repo](https://github.com/anthropics/claude-agent-sdk-python)) · [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) · [Pydantic AI](https://ai.pydantic.dev) · [Google ADK](https://google.github.io/adk-docs/)<br>• Read [Temporal](https://docs.temporal.io)'s durable-execution concepts for bank workflows. |
| 15:45 | **Read B** | • [Agentless](https://arxiv.org/abs/2407.01489) (Xia et al., 2024) — strongest evidence for the workflow side<br>• [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) — HumanLayer<br>• [A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — OpenAI (PDF) |
| — | **Optional evening — production harnesses** | • [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) architecture docs · [openai/codex](https://github.com/openai/codex) sandboxing and approval-policy code (Rust)<br>• Field reports (Anthropic *Scaling Managed Agents*; Cognition *What We Learned Building Cloud Agents*; OpenAI *Harness Engineering*) — linked from the [awesome-agent-harness wiki](https://github.com/Picrew/awesome-agent-harness/wiki)<br>• [LangChain Academy](https://academy.langchain.com) — *Introduction to LangGraph*, persistence and HITL modules |

> **Leader lens:** one-page memo — when is a regulated flow a workflow, and when is it an agent?


<a id="day-13"></a>
### Day 13 — Inference internals & unit economics (on your own 5090)

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • [Transformer Inference Arithmetic](https://kipp.ly/transformer-inference-arithmetic/) — kipply<br>• [Making Deep Learning Go Brrrr](https://horace.io/brrr_intro.html) — Horace He<br>• [vLLM and PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html) — vLLM blog<br>• [LLM Inference Economics from First Principles](https://www.tensoreconomics.com/p/llm-inference-economics-from-first)<br>• (These are weeks 1, 2 and 9 of [time-to-first-token](https://github.com/patchy631/time-to-first-token), compressed.) |
| 12:15 | **Build**<br>`5090`<br>*no GPU rental needed* | • Serve an 8B–14B model with vLLM, tool calling on. Run [`vllm bench serve`](https://docs.vllm.ai/en/latest/benchmarking/cli/) at a few concurrency levels; watch TTFT, inter-token latency and KV-cache use.<br>• **Cost per million tokens** two ways: your hardware (power draw × your electricity tariff + card amortised over ~3 years) vs the current hourly price of a cloud H100 at the same measured throughput.<br>• Rerun the Day 11 suite against the local model. That quality gap is the real self-host question.<br>• **LM Studio vs vLLM:** load the same model in LM Studio on the Mac and run the same concurrency sweep through LiteLLM. LM Studio is excellent for one user; watch where vLLM's continuous batching pulls ahead as concurrency rises, and what unified memory lets the Mac hold that 32 GB of VRAM can't. |
| 14:30 | **Adopt**<br>`Mac` | • [LiteLLM](https://github.com/BerriAI/litellm) (or [Portkey](https://github.com/Portkey-AI/gateway)) in front of Claude *and* your 5090: routing, fallback, per-task token budgets, per-key spend.<br>• Cloud reference: [Azure API Management AI gateway](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities) [Azure · read] |
| 15:45 | **Read B** | • [Optimizing AI Inference at Character.AI](https://blog.character.ai/optimizing-ai-inference-at-character-ai-2/)<br>• [A Postmortem of Three Recent Issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) — Anthropic<br>• *AI Engineering*, **Ch 9** |
| — | **Optional evening** | • [How to Scale Your Model](https://jax-ml.github.io/scaling-book/) — inference chapters · [Stanford CS336](https://cs336.stanford.edu) Lecture 10 · [PagedAttention paper](https://arxiv.org/abs/2309.06180) |

> **Leader lens:** self-host vs API — data residency, cost crossover by utilisation, and the quality gap *on your own eval*.


<a id="day-14"></a>
### Day 14 — Security, red-teaming, governance

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A** | • IMDA [Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2026/new-model-ai-governance-framework-for-agentic-ai) (Jan 2026; updated May 2026)<br>• CSA [Securing Agentic AI: A Discussion Paper](https://www.csa.gov.sg/resources/publications/securing-agentic-ai-a-discussion-paper/) + the finalised *Addendum on Securing Agentic AI* (June 2026) in [CSA publications](https://www.csa.gov.sg/resources/publications/)<br>• MAS [Guidelines on AI Risk Management — consultation](https://www.mas.gov.sg/publications/consultations/2025/consultation-paper-on-guidelines-on-artificial-intelligence-risk-management) (check the same page for the final version)<br>• MAS [Project MindForge](https://www.mas.gov.sg/schemes-and-initiatives/project-mindforge) — AI risk management handbook<br>• MAS [Technology Risk Management Guidelines](https://www.mas.gov.sg/regulation/guidelines/technology-risk-management-guidelines) — SDLC controls that AI-built systems still sit inside |
| 12:15 | **Build**<br>`Mac` | • Two-page governance mapping: each harness control → IMDA framework dimension → MAS materiality lens (impact, complexity, reliance). Include the RAG entitlement filter and MCP scopes and pinning. |
| 14:30 | **Adopt**<br>`Mac` `5090`<br>*red-team, all runnable locally* | • [garak](https://github.com/NVIDIA/garak) · [promptfoo red team](https://www.promptfoo.dev/docs/red-team/) · [Moonshot](https://github.com/aiverify-foundation/moonshot) (AI Verify Foundation)<br>• Attacks: memo injection, **RAG poisoning** (a planted policy document with instructions), **MCP tool poisoning**.<br>• [AgentDojo](https://github.com/ethz-spylab/agentdojo) ([paper](https://arxiv.org/abs/2406.13352)) — its **banking suite**, with your defences at the tool-execution seam; report utility and attack success rate with and without.<br>• Optional: AgentThreatBench in [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals). |
| 15:45 | **Read B** | • OWASP *Top 10 for Agentic Applications (2026)* and *Agentic AI — Threats and Mitigations* at [genai.owasp.org](https://genai.owasp.org) — map every finding to a category |
| — | **Optional evening** | • *AI Engineering*, **Ch 10**<br>• **Day 16 primer:** Birgitta Böckeler, [Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) |

> **Leader lens:** this document is what a CRO or regulator asks for, and you can now write it from the code up.


<a id="day-15"></a>
### Day 15 — Integrate, ship, narrate

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Integrate** | • wire the capstone end to end; fix the top three failure categories; decide which adopted tools stay, using your five-question verdicts. |
| 12:15 | **Write** | • README with architecture diagram, eval scorecard, retrieval metrics, cost table (local vs API), tool verdicts, governance mapping. |
| 14:30 | **Record & publish** | • five-minute demo; publish the repo; finish one post for [arunma.com](https://arunma.com). |
| 16:30 | **Retro** | • what clicked, what didn't; write the 90-day follow-on. |
| — | **Evening primer for Day 16** | • [Claude Code: Best Practices for Agentic Coding](https://www.anthropic.com/engineering/claude-code-best-practices). |

---

## Final Saturday — Day 16: Building an AI-driven engineering culture (EM track)

A softer day (about 6h), placed last because you can lead this credibly only after building agents yourself. The output is a playbook you could take into your next role on day one.

<a id="day-16"></a>
### Day 16: Building an AI-driven engineering culture (EM track)

| Time | Block | What to do |
|---|---|---|
| 09:00 | **Read A**<br>*the evidence* | • DORA [State of AI-assisted Software Development 2025](https://dora.dev/dora-report-2025/) and the [DORA AI Capabilities Model](https://dora.dev/ai/capabilities-model/report/) — seven capabilities that amplify AI's benefits<br>• DORA [ROI of AI-assisted Software Development](https://dora.dev/ai/) (2026) — the J-curve and the early productivity dip<br>• METR, [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — perceived vs measured speed-up<br>• Anthropic, [How Anthropic Teams Use Claude Code](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code) |
| 10:30 | **Read A**<br>*the practice* | • Claude Code docs: [skills](https://docs.claude.com/en/docs/claude-code/skills) · [hooks](https://docs.claude.com/en/docs/claude-code/hooks) · [subagents](https://docs.claude.com/en/docs/claude-code/sub-agents) · [plugins](https://docs.claude.com/en/docs/claude-code/plugins) · [plugin marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)<br>• [AGENTS.md](https://agents.md) convention<br>• GitHub, [Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) + [github/spec-kit](https://github.com/github/spec-kit) |
| 12:15 | **Build**<br>`Mac`<br>*team toolkit* | • **Context file:** turn your sprint-long `CLAUDE.md` into a template for a bank engineering repo — conventions, test commands, forbidden actions (no customer data in prompts, no secrets, no direct prod access).<br>• **Two team skills** (`SKILL.md`): e.g. banking PR review (PII in logs, idempotency, audit trail, rollback) and an incident or migration runbook. Structure references: [anthropics/skills](https://github.com/anthropics/skills), [hamelsmu/evals-skills](https://github.com/hamelsmu/evals-skills).<br>• **Package a plugin:** the skills + a hook blocking commits with secrets or failing tests + a slash command + your Day 9 MCP server, published to a private marketplace repo. Install it on the 5090 box as a "clean machine" to prove the rollout path. |
| 14:30 | **Build**<br>*SDD trial* | • Run [Spec Kit](https://github.com/github/spec-kit) end to end on one small capstone feature: constitution → specify → plan → tasks → implement, with EARS-style acceptance criteria. Build a comparable feature without a spec; record time, review effort, rework.<br>• Optional: [Kiro](https://kiro.dev) if your future stack is AWS-native. |
| 15:45 | **Write**<br>*the playbook (two pages)* | • **Adoption path:** pilot team → champions → paved road (shared plugin marketplace, templates) → org default.<br>• **Guardrails:** which repos and data classes may touch which models and where they're hosted; "you commit it, you own it"; mandatory human review of AI-authored PRs; AI-generated code stays inside [MAS TRM](https://www.mas.gov.sg/regulation/guidelines/technology-risk-management-guidelines) SDLC controls.<br>• **Metrics:** DORA four keys segmented by AI-assisted vs not; change-failure rate and rework on AI PRs; review latency. Explicitly *not* lines of code or suggestion acceptance rate.<br>• **People:** protecting how juniors learn; office hours and pairing; recognising contributors to the shared marketplace.<br>• **Expectation-setting:** the J-curve conversation with executives. |
| 17:00 | **Retro** | • what surprised you in DORA and METR versus your own 16 days. |
| — | **Optional evening** | • [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar) — SDD and AI-coding entries<br>• SDD alternatives: [OpenSpec](https://github.com/Fission-AI/OpenSpec) · [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) · comparison: [LLM-Coding/Spec-Driven](https://github.com/LLM-Coding/Spec-Driven) |

> **Leader lens:** AI amplifies whatever system it lands in. Fix the platform, CI, tests and review culture first; the tooling rollout is the easy part.


---

## Capstone spec — Dispute & Ops Agent

| Component | Day | Built with | Runs on |
|---|---|---|---|
| Loop, tools, structured output | 1–2 | Hand-built · Pydantic / Instructor | Mac + API |
| Permissions, hooks, guardrails | 3 | Hand-built · NeMo Guardrails, Llama Guard | Mac + 5090 |
| Planning, subagents | 4 | Hand-built | Mac + API |
| Context policy, tracing | 5 | Hand-built · Langfuse, LangSmith | Mac |
| Ingestion, extraction, hybrid index, golden set | 6 | Docling, OpenSearch, Qwen3-Embedding / Voyage / Cohere | Mac + 5090 |
| Reranking, citations, guardrails, lifecycle, agentic RAG | 7 | bge-reranker / Cohere Rerank, Citations API, Presidio, Ragas | Mac + 5090 + API |
| MCP over stdio: server, client, resources | 8 | Hand-built · MCP Inspector | Mac |
| MCP over HTTP: sessions, scopes, poisoning defence | 9 | Hand-built · FastMCP / official SDK | Mac |
| Memory, persistent tasks | 10 | Hand-built · Mem0, Graphiti, Letta, LangMem | Mac |
| Evals with pass^k | 11 | Hand-built · LangSmith, Inspect, evals-skills | Mac + API |
| Workflow variant | 12 | LangGraph, Claude Agent SDK, OpenAI Agents SDK | Mac + API |
| Self-hosted model + gateway | 13 | vLLM, LiteLLM | 5090 + Mac |
| Red-team + governance | 14 | garak, promptfoo, Moonshot, AgentDojo | Mac + 5090 |
| Team toolkit: context file, skills, plugin, SDD | 16 | Claude Code plugins, Spec Kit | Mac |

A public repo and writeup showing hands-on agent engineering in a regulated setting is direct evidence of depth, not just infrastructure leadership.

---

## Verdicts on your four original resources

| Resource | Verdict | Where it appears |
|---|---|---|
| [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | **Core.** Backbone of Weeks 1–2. Read its "agents are trained, not coded" stance critically; Day 12 tests it. | s01–s10 and s14–s17 across Days 1–12; s11–s13 optional |
| [time-to-first-token](https://github.com/patchy631/time-to-first-token) | **Good content, wrong scope for now.** | Compressed into Day 13 on your 5090; resume at 30 min/day afterwards |
| [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) | **Low marginal value for you**, but useful for the Azure reference view. | Optional on Day 10, skim on Day 12 |
| [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | **Read, don't build on.** | Optional evening on Day 12 |

---

## Budget (rough)

- **Anthropic API:** set a hard limit. Evals and multi-agent experiments dominate spend; route bulk runs and judges to Haiku, and to your 5090 where quality allows.
- **Managed APIs:** Voyage, Cohere and LangSmith trial or free tiers should cover the sprint.
- **GPU:** none to rent — the 5090 covers Day 13 and local embeddings, rerankers and guardrail models.
- **AWS:** optional, only for the Day 3 and Day 7 comparisons.

## 90-day follow-on library

- Sebastian Raschka, *Build a Reasoning Model (From Scratch)* (Manning) — the RL post-training behind agentic behaviour; a natural sequel to nanochat, and your 5090 can run its experiments.
- The rest of [time-to-first-token](https://github.com/patchy631/time-to-first-token) at 30 min/day.
- [How to Scale Your Model](https://jax-ml.github.io/scaling-book/) — full book.
- [Berkeley LLM Agents MOOC](https://llmagents-learning.org).
- Manning's 2026 agent titles ([catalogue](https://www.manning.com/catalog/ai/ai-agents)) — browse tables of contents first.
- Deliberately deferred: fine-tuning and RL for agents, computer-use and voice agents, cross-organisation A2A systems.
