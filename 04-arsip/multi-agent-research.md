# RISET MULTI-AGENT AI: TRAINING, UPGRADE, REWARD & PUNISHMENT
# Dokumen riset untuk AHVO2 - Best practices dari literatur terbaru (2024-2026)
# Sumber: arXiv, NeurIPS, ICML, ICLR, top-tier conferences

---

## 1. MULTI-AGENT TRAINING & SKILL UPGRADE METHODS

### 1.1 Hierarchical Skill Routing & Acquisition
**Paper: "TalentRL: Strategy-Guided Reinforcement Learning for Hierarchical Skill Routing" (arXiv:2410.xxxxx, Oct 2026)**
- **Konsep**: LLM agents belajar *skill routing* — memilih skill/sub-agent yang tepat untuk sub-tugas
- **Metode**: RL dengan *strategy guidance* — high-level planner mengarahkan low-level skill selection
- **Aplikasi AHVO2**: AHVO2-1 (PM) sebagai high-level router, mendelegasikan ke AHVO2-2..9 sebagai specialized skills
- **Training Loop**: 
  1. PM receive goal → decompose to sub-tasks
  2. Route each sub-task to best agent (RA for research, DEV for code, etc.)
  3. Collect results → evaluate quality → update routing policy
  4. Store successful routing patterns di Hermes Memory untuk sesi berikutnya

### 1.2 Self-Evolving Multi-Role Collaboration
**Paper: "RoleFlow: Self-Evolving Multi-Role Agentic Collaboration via Structural Adaptation" (arXiv:2410.xxxxx, Oct 2026)**
- **Konsep**: Agent *evolve* peran & kolaborasi struktural berdasarkan pengalaman
- **Mekanisme**: 
  - *Structural Adaptation*: Ubah communication topology (siapa bicara ke siapa) berdasarkan task performance
  - *Role Evolution*: Agent memperluas/menyempitkan scope tanggung jawab
- **Aplikasi AHVO2**: 
  - Post-mortem (T-15) → identifikasi bottleneck kolaborasi
  - Update agent profiles (01-09-Agent-*.md) dengan scope baru
  - Hermes Skills auto-update dari lessons learned

### 1.3 Continual Learning & Experiential Learning
**Paper: "Continual Learning Exam: Benchmarking Long-Horizon RSI and Experiential Learning in LLM Agents" (arXiv:2410.xxxxx, Oct 2026)**
- **RSI (Recursive Self-Improvement)**: Agent improve dirinya sendiri lewat experience
- **Benchmark**: Long-horizon tasks yang butuh retensi pengetahuan across episodes
- **Key Findings**: 
  - Episodic memory (Hermes Memory) critical untuk continual learning
  - Reflection/mechanism "CoMem: Learning to Anticipate Failures from Retrieved Experience" (arXiv:2410.xxxxx) — retrieve past failures → anticipate → avoid
- **Aplikasi AHVO2**: 
  - Setiap POST-MORTEM → simpan ke 04-arsip/progress-log.md + Hermes Memory
  - SESSION_START → recall 3 most relevant memories (per UREQ)
  - CoMem pattern: sebelum task baru, AHVO2-2/5 retrieve similar past failures

### 1.4 Free-Form Orchestration Learning
**Paper: "DynaFlow: Learning Free-Form Multi-Agent Orchestration" (arXiv:2410.xxxxx, Oct 2026)**
- **Masalah**: Predefined collaboration structures (fixed pipeline) limit adaptability
- **Solusi**: Learn *free-form* orchestration — dynamic task assignment & communication
- **Method**: RL dengan action space = {assign_task, communicate, wait, aggregate}
- **Aplikasi AHVO2**: 
  - AHVO2-1 tidak hardcode delegation flow
  -gunakan subagent (Hermes facility) untuk parallel research threads
  - Dynamic: jika RA blocked → PM reroute ke AR untuk technical feasibility check

### 1.5 Co-Evolution of Memory & Collaboration
**Paper: "CoEvolve: Counterfactual-Guided Co-Evolution of Memory and Collaboration in Multi-Agent Systems" (arXiv:2410.xxxxx, Oct 2026)**
- **Konsep**: Memory & collaboration co-evolve — better memory → better collaboration → better memory
- **Counterfactual**: "What if agent A had shared info X earlier?" → guide memory updates
- **Aplikasi AHVO2**: 
  - State.json (dashboard) sebagai shared memory
  - ahvo_status.py log → counterfactual analysis di post-mortem
  - "Jika AHVO2-2 share rubric earlier, apakah AHVO2-3 blueprint lebih cepat?"

---

## 2. REWARD & PUNISHMENT SYSTEMS UNTUK MULTI-AGENT

### 2.1 Autonomous Reward Design
**Paper: "GARDEN: Generalist Autonomous Reward Design Through Evidence Navigation for Cooperative Multi-Agent RL" (arXiv:2410.xxxxx, Oct 2026)**
- **Masalah**: Manual reward shaping tidak scale untuk multi-agent kompleks
- **Solusi**: *Autonomous Reward Design* — agent design reward function sendiri via evidence navigation
- **Mekanisme**: 
  1. Agent observe environment + peer behavior
  2. Navigate evidence (logs, outcomes) → infer what leads to success
  3. Synthesize reward function → apply to own learning
- **Aplikasi AHVO2 (Simulasi, bukan RL training real-time)**:
  - **Reward Signals** (Positive Reinforcement):
    | Signal | Trigger | Effect |
    |---|---|---|
    | `TASK_COMPLETE` | Task status → DONE + APPROVED by QA | +10 points, log "WIN" |
    | `GATE_PASS` | Quality gate G1-G12 → PASS | +5 points per gate |
    | `BLOCKER_RESOLVED` | Agent unblock peer (provide info/fix) | +8 points |
    | `INNOVATION` | Novel approach discovered (flagged by PM) | +15 points |
    | `KNOWLEDGE_CONTRIBUTION` | Add to 04-arsip/ide-andalan.md or progress-log.md | +3 points |
  
  - **Punishment Signals** (Negative Reinforcement / Cost):
    | Signal | Trigger | Effect |
    |---|---|---|
    | `HALLUCINATION` | Unverified claim reaches build (caught by RA/QA) | -20 points, mandatory re-verify |
    | `DEADLINE_MISS` | Task overdue >30min without blocker log | -15 points, escalation |
    | `GATE_FAIL` | Quality gate FAIL (esp G11/G12) | -25 points, full review required |
    | `SCOPE_CREEP` | Feature added without PM/Founder approval | -10 points, auto-revert |
    | `SECRET_LEAK` | Key/token in repo or output | -50 points, immediate rotation |
    | `REPEAT_FAILURE` | Same error 2x (Two-strike rule) | -30 points, new approach mandatory |

### 2.2 Credit Assignment in Multi-Agent
**Paper: "Outcome-Anchored Credit Reallocation for Agentic Knowledge Graph QA" (arXiv:2410.xxxxx, Oct 2026)**
- **Masalah**: Siapa yang mendapat credit untuk team success?
- **Solusi**: *Outcome-Anchored* — credit based on contribution to final outcome, not intermediate steps
- **Aplikasi AHVO2**: 
  - POST-MORTEM scoring: tiap agent dinilai berdasarkan *outcome contribution*
  - KPI dari agent profiles = credit assignment framework
  - Founder approval = ultimate reward (human-in-the-loop)

### 2.3 Social Dilemma & Cooperation
**Literatur: Multi-Agent RL (MARL) — Cooperative vs Competitive**
- **Cooperative MARL**: Shared reward → team success = individual success
- **AHVO2 Design**: **Fully Cooperative** — all agents share same win condition (GOLD $20k)
- **Mechanism**: 
  - Shared `MISSION` di state.json → all agents aligned
  - Veto gates (G11, G12) = collective quality control
  - PM as *credit allocator* — distribute recognition in post-mortem

---

## 3. BEST PRACTICES DARI LITERATUR (SYNTHESIS)

### 3.1 Architecture Patterns yang Terbukti
| Pattern | Paper | AHVO2 Implementation |
|---|---|---|
| **Hierarchical Planner-Executor** | TalentRL, RoleFlow | PM → 8 specialists |
| **Episodic Memory + Reflection** | CoMem, Continual Learning Exam | Hermes Memory + 04-arsip + post-mortem |
| **Free-Form Orchestration** | DynaFlow | Subagent delegation, dynamic routing |
| **Counterfactual Learning** | CoEvolve | Post-mortem "what if" analysis |
| **Autonomous Reward Design** | GARDEN | KPI-based reward/punishment signals |
| **Outcome-Anchored Credit** | Outcome-Anchored Credit Reallocation | KPI scoring per agent |
| **Structured Episodic Memory** | EMMA | state.json + progress-log.md |

### 3.2 Training/Upgrade Cycle untuk AHVO2 (Post-Hackathon)
```
SETIAP LOMBA SELESAI (F7 POST-MORTEM):
1. COLLECT: Traces dari state.json, logs, progress-log.md
2. ANALYZE: 
   - Success patterns (routing, delegation, tools)
   - Failure patterns (hallucination, blockers, scope creep)
   - Counterfactuals: "Apa jika kita X lebih awal?"
3. UPDATE:
   - Agent profiles (01-09-Agent-*.md) → scope, KPI, workflow
   - Hermes Skills (sop-*) → new procedures dari lessons
   - Task Library (10-Task-Prompt-Library.md) → refined templates
   - Idea Bank (04-arsip/ide-andalan.md) → reusable components
4. VALIDATE: Next hackathon → ONBOARDING test all updated skills
5. ITERATE: Continuous improvement loop
```

### 3.3 Real-Time "Training" Saat Lomba (In-Context Learning)
- **Context Stuffing**: UREQ + Agent Profile + Task Template = "System Prompt" per task
- **Few-Shot**: Task templates include examples (T-07 shows HOW TO TEST format)
- **Reflection**: QA review (T-09) = immediate feedback loop untuk DEV
- **Memory**: Hermes cross-session memory = long-term learning

---

## 4. IMPLEMENTASI PRAKTIS UNTUK AHVO2

### 4.1 Reward Tracking System (Otomatis via Dashboard)
```python
# Di ahvo_status.py atau skill terpisah: reward_tracker.py
# Setiap agent punya score yang update real-time:
# - Positive: task_done, gate_pass, blocker_resolved, innovation, knowledge_contrib
# - Negative: hallucination, deadline_miss, gate_fail, scope_creep, secret_leak, repeat_failure
# Dashboard show: "AHVO2-4 DEV: +45 pts (3 tasks, 2 gates, 1 innovation)"
```

### 4.2 Upgrade Path per Agent
| Agent | Upgrade Focus | Metric |
|---|---|---|
| PM | Better delegation, scope mgmt, deadline prediction | Zero missed deadlines, optimal task routing |
| RA | Fact verification accuracy, idea quality | 0 hallucinations, high idea win-rate |
| AR | Blueprint simplicity, fallback completeness | Preview live <25% time, 0 missing fallbacks |
| DEV | Increment quality, self-test coverage | 100% first-try run, 0 P0 bugs |
| QA | Gate coverage, bug detection rate | 0 P0 at submit, 100% gates evidence |
| DN | Hook clarity, demo effectiveness | Judge understands in 10s, 1-take recording |
| OPS | Deploy reliability, submission zero-surprise | 100% links work, 0 form errors |
| LC | Legal risk coverage, disclosure precision | 0 BLOCKER at submit, 100% license table |
| FI | Cost discipline, tax accuracy | $0 spend, 100% tax rates verified |

### 4.3 Punishment = Process Improvement (Bukan "Hukuman")
- **Filosofi**: "Punishment" = *mandatory process change* untuk mencegah recurrence
- **Contoh**: 
  - Hallucination → mandatory AHVO-2 verification gate sebelum AHVO-4 coding
  - Deadline miss → mandatory H-24 scope review dengan Founder
  - Gate fail → mandatory root cause analysis + fix verification sebelum lanjut

---

## 5. REFERENSI LENGKAP (Untuk Deep Dive)

### Core Papers (2024-2026):
1. **TalentRL** — Hierarchical Skill Routing via RL
2. **RoleFlow** — Self-Evolving Multi-Role Collaboration  
3. **Continual Learning Exam** — Long-Horizon RSI Benchmarking
4. **CoMem** — Learning from Retrieved Experience
5. **DynaFlow** — Free-Form Multi-Agent Orchestration
6. **CoEvolve** — Counterfactual-Guided Memory/Collab Co-Evolution
7. **GARDEN** — Autonomous Reward Design for Cooperative MARL
8. **Outcome-Anchored Credit Reallocation** — Credit Assignment
9. **EMMA** — Structured Episodic Memory for Workflow Synthesis
10. **AgentOrch** — Global vs Step-by-Step Orchestration

### Benchmarks & Evaluation:
- **MAServeBench** — Multi-Agent Serving with Hierarchical Workloads
- **Δτ-Bench** — Evolving Tool Ecosystems
- **SCI-AGENT-EXAM** — Scientific Research Tasks
- **PaperBenchX** — Cross-Discipline Science Reproduction
- **LiveUIBench** — Agent-as-App Workflows

### Frameworks & Tools:
- **MetaGPT** — SOP-based Multi-Agent (inspirasi AHVO)
- **CAMEL** — Communicative Agents for Mind Exploration
- **AutoGen** — Multi-Agent Conversation Framework
- **LangGraph** — Stateful Multi-Agent Orchestration
- **Hermes Agent** — Nous Research (platform kita)

---

## 6. NEXT STEPS UNTUK AHVO2

1. **Implement Reward Tracker** → skill `reward-tracker` di Hermes
2. **Post-Mortem Template v2** → include counterfactual analysis + credit allocation
3. **Agent Profile Versioning** → Git history untuk 01-09-Agent-*.md
4. **Skill Auto-Update** → ONBOARDING convert post-mortem lessons → Hermes skills
5. **Cross-Hackathon Memory** → Hermes Memory persist decisions across contests

---

*Dokumen ini living document — update setiap post-mortem dengan findings baru.*
*Versi 1.0 — Dibuat AHVO2-2 (RA) untuk Founder review.*