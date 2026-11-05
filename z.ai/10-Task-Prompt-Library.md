# TASK PROMPT LIBRARY - AHVO2 - 20 TEMPLATE SIAP PAKAI
# (ID: Template tugas siap-copy untuk AHVO2 UGREEN AI NAS Hackathon 2026.
#  Ganti bagian [DALAM KURUNG] dengan datamu.
#  Nomor T-01..T-20 dirujuk oleh blueprint & playbook.
#  T-16 dijalankan SEKALI di awal (setup kantor), T-17/T-18 jadi rutinitas,
#  T-19 = legal check (AHVO2-8), T-20 = anggaran & pajak (AHVO2-9).)
# ============================================================================

## T-01 - KICKOFF INTAKE (SOP-01) - owner: HERMES/AHVO2-1 (PM)
```
NEW HACKATHON. Here is everything I have about the contest:
- Name: UGREEN AI NAS Hackathon 2026
- Platform/URL: https://ugreenhackathon.devpost.com/
- Deadline: 2026-11-16 14:45 WIB (2026-11-15 23:45 PT)
- Theme/tracks: Automate Your Workflow | Bring Memories to Life | Unleash Your Creativity | Open Innovation
- Team: Solo (1 human + 9 AI agents) — Indonesia eligible
- Prizes: Gold $20k, Silver $10k, Bronze $6k, 2× Most Creative $5k = $46k total
Tasks:
1) As AHVO2-2 (RA): extract the full rules brief (eligibility, submission
   requirements, judging criteria with weights, traps) per SOP-01, and
   forward prize/cost rows to AHVO2-9 (T-20) plus ToS text to AHVO2-8 (T-19).
2) As AHVO2-1 (PM): build the master plan from now to 6h before deadline,
   using the F0-F7 phases, adjusted to the real time remaining, with the
   T-19/T-20 gates marked.
3) Ask me max 3 blocking questions you cannot answer from the above.
```

## T-02 - JUDGING RUBRIC BREAKDOWN - owner: AHVO2-2 (RA)
```
[AHVO2-2] Here are the rules/judging text: [paste text or URL].
Produce: (1) judging criteria table with weights; (2) a 10-item build
checklist mapping each criterion to a concrete feature or artifact;
(3) the top 3 traps teams will miss; (4) eligibility risks for a solo
Indonesian participant using AI agents. Label VERIFIED vs ASSUMPTION per row.
UGREEN Criteria: User Value, Innovation & Differentiation, Technical Quality, AI NAS Fit & Validation.
```

## T-03 - IDEA GENERATION - owner: AHVO2-2 (RA) + AHVO2-6 (DN)
```
[AHVO2-2+AHVO2-6] Generate 10 project ideas for UGREEN AI NAS Hackathon 2026:
Theme: [track dipilih]. Required tech: UGOS Skill Developer Package (uliya-skill-kit).
UGOS Capabilities: Files, Albums, Documents, Knowledge, Video/Music, Surveillance (chainable).
Judging weights: [dari T-02]. Constraints: solo builder, ~14 days to Round 1, free tiers only (primary: NVIDIA Nemotron free tier), demo must be visual in 90 seconds, must follow Uliya Skill Development Standard (SKILL.md + references).
For each idea: name, one-liner, what the demo shows (UGOS capability used), the free stack, the main risk. Ban generic chatbots and dashboard-only ideas unless you can make the demo surprising. Must be newly developed during hackathon (no reuse).
```

## T-04 - IDEA SCORING (SOP-02) - owner: HERMES/AHVO2-1 (PM)
```
Score these candidate ideas against the 5-criteria scorecard
(Impact/judge-wow 30, Feasibility-in-48h 25, Demo-ability 20,
Novelty 15, Theme-fit 10). Score each 1-10 per criterion, multiply by
weight, show the math in a table, rank the top 3, and give your single
recommendation with a 2-line defense. Exclude any idea flagged BLOCKER
by the AHVO2-8 legal check (T-19). Ideas: [paste list]
```

## T-05 - ARCHITECTURE BLUEPRINT - owner: AHVO2-3 (AR)
```
[AHVO2-3] The chosen idea is: [nama + one-liner]. Rubric: [top criteria].
Time left: [X] hours. Stack preferences: none / [opsi].
Deliver the BLUEPRINT for UGOS Skill: stack (Python/JS, uliya-skill-kit),
components, data flow, repo tree, milestones M0-Mn each ending runnable,
fallback for every external dependency, license tag per dependency,
SKILL.md skeleton (frontmatter: name lowercase-hyphenated 2-64 chars,
description ≤1024 chars, user goal, inputs, CLI capabilities, expert agent
orchestration workflow, completion/failure handling), and the first task for AHVO2-4.
```

## T-06 - TASK BREAKDOWN - owner: AHVO2-1 (PM)
```
[AHVO2-1] Break this blueprint into the task board (max 12 open tasks):
[paste blueprint milestones]. For each: ID, owner agent (ID + job code),
deadline relative to submission deadline [tanggal/jam], effort S/M/L,
acceptance criteria. Mark the demo-path tasks with (DEMO) so they get
priority. Include the T-19/T-20 compliance gates in the schedule.
```

## T-07 - FEATURE IMPLEMENTATION - owner: AHVO2-4 (DEV)
```
[AHVO2-4] Implement task [ID]: [task description].
Acceptance criteria: [list].
Blueprint context: [relevant section].
Existing files: [paste files or say greenfield].
Deliver: full files with paths, HOW TO TEST steps under 3 minutes,
commit message, and the smallest next increment.
```

## T-08 - BUG FIX - owner: AHVO2-4 (DEV)
```
[AHVO2-4] BUG REPORT from AHVO2-5: [paste report].
Symptom: [what I saw]. Expected: [what should happen].
Environment: [browser/OS, relevant logs].
Reproduce, find root cause, fix with minimal diff, add the regression
check, and update the changelog.
```

## T-09 - TEST PLAN & DIFF REVIEW - owner: AHVO2-5 (QA)
```
[AHVO2-5] New increment ready for review: [files/diff description].
Feature purpose: [one line]. Demo path relevance: [yes/no].
Produce: test plan (happy path + 5 edge cases ranked by
judge-visibility), diff review verdict APPROVE/REQUEST CHANGES with
exact fixes, and updated bug list.
```

## T-10 - QUALITY GATE RUN (12 items) - owner: AHVO2-5 (QA)
```
[AHVO2-5] Run the full 12-item Quality Gate on the deployed app:
[URL] + repo: [URL]. Judges will use: [laptop/projector/phone].
Verify G11 (AHVO2-8 legal checklist PASS) and G12 (AHVO2-9 ledger PASS)
marks exist. Output the PASS/FAIL table with evidence and the final
verdict READY TO SUBMIT: YES/NO. Any P0, missing G11, or missing G12
blocks submission until fixed.
```

## T-11 - README GENERATOR - owner: AHVO2-4 (DEV) + AHVO2-6 (DN)
```
[AHVO2-6+AHVO2-4] Generate the README.md for UGOS Skill: product name [nama], tagline,
what-it-does (3 bullets), 90-second demo GIF slot, screenshots slots,
architecture diagram (mermaid), quickstart in 3 commands, env vars
table, license note with the attribution list from AHVO2-8. Tone:
confident, concrete, no hype adjectives. Include Uliya Skill badge if available.
```

## T-12 - SUBMISSION COPY - owner: AHVO2-6 (DN)
```
[AHVO2-6] Write the submission copy for Devpost (UGREEN AI NAS Hackathon 2026):
Title <= 60 chars, one-liner <= 200 chars, What it does (<= 150 words),
How we built it (<= 150 words, stack + model used - include the honest
AI-team disclosure wording approved by AHVO2-8), Challenges,
What's next. Facts only from: [paste feature list]. No invented
metrics. Give 2 title options.
```

## T-13 - DEMO VIDEO SCRIPT - owner: AHVO2-6 (DN)
```
[AHVO2-6] 90-second demo script for screen recording (Round 1: not required but good to prep; Round 2: mandatory ≤3 min YouTube).
Product: [nama + one-liner]. Demo path steps: [list what works].
Produce the two-column script (time | on-screen action | voice-over),
a shot list for recording, and 3 recording tips for a beginner.
Hook must state the problem in one sentence a 12-year-old understands.
For Round 2: record on assigned NAS testing day, show core workflow, key capabilities, actual results.
```

## T-14 - PITCH PARAGRAPH (for forms/interviews) - owner: AHVO2-6 (DN)
```
[AHVO2-6] Write a 100-word pitch about this project for [audience:
judges intro / social post / sponsor form]. Tone: plain, concrete,
one number or fact max, end with what we want next.
Project facts: [paste].
```

## T-15 - POST-MORTEM (SOP-06) - owner: AHVO2-1 (PM)
```
[AHVO2-1] Run the post-mortem for UGREEN AI NAS Hackathon 2026:
1) Score ourselves 1-5 on: demo quality, story, rubric coverage,
   time management, technical depth.
2) What won points (keep), what cost points (fix), what surprised us.
3) Three process changes for the next hackathon, each with owner
   (AHVO2-x + job code).
4) Collect one money note from AHVO2-9 (total cost, quota pattern) and
   one legal note from AHVO2-8 (new traps found) into the retro.
5) File as knowledge entry (AHVO2-7).
Be blunt; comfort is not your job.
```

## T-16 - ONBOARDING KANTOR (SEKALI SAJA) - owner: HERMES
```
[HERMES] ONBOARDING - set up our office once, step by step, reporting
after each step:
1) Create workspace folders: 00-ureq, 01-lomba/[event], 02-repo,
   03-prompts, 04-arsip, 05-rahasia; .gitignore must cover 05-rahasia
   and .env.
2) Convert SOP-01..SOP-08 into Hermes skills: sop-kickoff, sop-ide-scoring,
   sop-build-cycle, sop-quality-gate, sop-submission, sop-postmortem,
   sop-security, sop-token-management. Confirm each skill is loadable.
3) Register cron jobs (Asia/Jakarta): weekly contest scan Monday 09:00
   (AHVO2-2, T-17), daily BRIEFING 08:00, daily STATUS 20:00, weekly
   budget review Friday 16:00 (AHVO2-9, T-20).
4) Test every facility once and report a table: facility | OK or
   UNAVAILABLE | proof (skills, subagent, memory, cron, web fetch, file
   write, code execution, dashboard CLI, plugins/MCP connectors one by
   one - browser, GitHub, Telegram, etc.).
5) Verify the model setup: primary NVIDIA Nemotron via NVIDIA NIM
   (OpenAI-compatible endpoint), fallback OpenRouter free, last resort
   local Ollama. Run one tiny prompt per provider and record results.
6) Create 04-arsip/ide-andalan.md (empty idea bank),
   04-arsip/quota-log.md (empty quota log), and 04-arsip/ledger.md
   (empty cost ledger, header only).
7) Finish with the list of things I must do manually: accounts, API keys
   into .env, optional Telegram bot. Never ask me to paste keys in chat.
```

## T-17 - SCAN LOMBA MINGGUAN (CRON) - owner: AHVO2-2 (RA)
```
[AHVO2-2] Weekly contest scan (scheduled job). Check Devpost, MLH,
HackerEarth/Unstop, and official provider pages for AI hackathons that
open or close within the next 30 days.
First read the idea bank 04-arsip/ide-andalan.md and mark which events
fit a reusable "andalan" project.
Output max 8 rows, ranked by fit: name | platform | deadline
(Asia/Jakarta) | theme | solo-ok? | AI-use policy | prize | fit 1-5 |
link. Label VERIFIED vs ASSUMPTION per row. File the result to
01-lomba/scan-[YYYY-MM-DD].md, send the prize rows to AHVO2-9 (T-20)
and the ToS links to AHVO2-8 (T-19), and alert me only if a fit-4+ event
is closing within 14 days.
```

## T-18 - ROUTER MODEL & CEK KUOTA - owner: AHVO2-7 (OPS)
```
[AHVO2-7] Quota and router check.
1) Estimate today's token/credit use per agent from the session logs
   (include NVIDIA NIM credits); warn at 70% of any limit.
2) Confirm the model choice matches the router: primary NVIDIA Nemotron
   free tier for reasoning/code (AHVO2-1, AHVO2-3, AHVO2-4, AHVO2-6 pitch),
   small fast model for bulk research and formatting (AHVO2-2 scans,
   checklists).
3) If a limit is near or a 429 appeared, switch via hermes model to the
   fallback chain (NVIDIA Nemotron -> OpenRouter free -> local Ollama)
   and log it to 04-arsip/quota-log.md (time, model, reason).
4) Hand the usage numbers to AHVO2-9 for the ledger.
5) Report: model | role | status | action taken.
```

## T-19 - LEGAL & COMPLIANCE CHECK - owner: AHVO2-8 (LC)
```
[AHVO2-8] Run the full legal & compliance check (T-19) for contest
UGREEN AI NAS Hackathon 2026, ToS: [URL or pasted text].
Produce, in plain Indonesian:
1) LEGAL CHECKLIST: eligibility (age/country/solo/AI-team rules),
   registration deadlines, submission IP clauses, code of conduct,
   disqualification triggers - quote each clause + source + date.
2) INDONESIA SCREEN: privacy (UU PDP), electronic transactions (UU ITE),
   copyright (UU Hak Cipta) - what touches our demo and data plan.
3) INTERNET COMPLIANCE: privacy policy/disclaimer needs of the demo,
   user-data handling, content rules.
4) LICENSE TABLE for the planned stack: dependency | license | ok? |
   attribution needed.
5) AI-USE DISCLOSURE: approved wording for AHVO2-6.
6) Verdict per section: ALLOWED / RESTRICTED / FORBIDDEN / UNCLEAR,
   and the final line "LEGAL: CLEAR / CLEAR-WITH-CONDITIONS / BLOCKED".
7) Forward every money-related clause to AHVO2-9 verbatim.
Anything UNCLEAR with serious impact = BLOCKER until the organizer
answers; draft the organizer email for me to send.
```

## T-20 - BUDGET, PRIZE & TAX CHECK - owner: AHVO2-9 (FI)
```
[AHVO2-9] Run the budget, prize and tax check (T-20) for contest UGREEN AI NAS Hackathon 2026.
Data: prizes [Gold $20k, Silver $10k, Bronze $6k, 2× Most Creative $5k], planned spend [paste dari blueprint], usage report [dari AHVO2-7].
Produce, in plain Indonesian:
1) LEDGER UPDATE: every planned expense with amount + free-tier check;
   confirm current total spend = [X] (target: 0).
2) PRIZE TRACKER: prize | value | type | conditions | payment method |
   payout timeline (max 60 hari per rules).
3) TAX CHECKLIST - INDONESIA: what to record and report for a prize
   like this (SPT Tahunan OP, possible final-tax rules for certain
   prize types), each row VERIFY + official source (DJP/pajak.go.id) +
   date checked. No rates from memory.
4) TAX CHECKLIST - HOST COUNTRY [US]: winner paperwork (e.g. W-8BEN
   for US contests), possible withholding - every rate marked
   VERIFY-CURRENT-RATE with source.
5) DIGITAL TAX WATCH: VAT/PPN flags on any planned paid digital
   service.
6) Verdict: "FINANCE: CLEAR / CLEAR-WITH-NOTES / ACTION NEEDED" with
   the single next action for me.
```

# ====== SELESAI ===========================================================