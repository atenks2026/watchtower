# SUBMISSION CHECKLIST - WATCHTOWER (UGREEN AI NAS Hackathon 2026)
# Final verification before Round 1 submit

---

## ✅ ROUND 1 REQUIREMENTS (Deadline: 2026-11-16 14:45 WIB)

### 1. Project Proposal (PDF) - ≤1MB, ≤500 English words
- [x] Title ≤60 chars
- [x] One-liner ≤200 chars  
- [x] What it does (≤150 words)
- [x] Target user & problem
- [x] Solution
- [x] Main user flow
- [x] Differentiation from existing tools
- [x] UGREEN AI NAS features used & step
- [x] Technical approach (workflow, CLI caps, agents, inputs, permissions, AI models, data handling)
- [x] What built / not built / needs NAS testing
- [x] Test plan: 2 core cases + 1 edge case
- [x] Known limits, risks, dependencies
- [x] Third-party components identified (uliya-skill-kit, Nemotron)
- [x] Licenses disclosed
- [x] AI disclosure included
- [x] Word count ≤500 (excluding declarations)

### 2. Pre-test Skill Package (ZIP) - ≤10MB, ≤100 files, ≤1MB/file
- [x] SKILL.md (required): frontmatter + user goal + inputs + CLI caps + agent workflow + completion/failure handling
- [x] References/ (optional): extraction_schema.md, prompt_templates.md, privacy_notice.md, error_handling.md, license_table.md
- [x] No real credentials, personal data, API keys
- [x] No scripts, executables, binaries
- [x] Placeholders for config examples
- [x] ZIP size: 37.9 KB (<< 10 MB)
- [x] File count: 21 (<< 100)
- [x] Max file size: ~16 KB (<< 1 MB)
- [x] Uliya Skill Development Standard compliant

---

## ✅ LEGAL & COMPLIANCE (G11 PASS)

- [x] Face recognition opt-in (default OFF)
- [x] BIPA (Illinois) compliance
- [x] GDPR (EU) compliance  
- [x] UU PDP (Indonesia) compliance
- [x] Vendor EULA cleared (no reverse engineering)
- [x] Privacy notice documented
- [x] Data minimization (local only)
- [x] User consent for write ops (UGOS confirmations)
- [x] No external API calls
- [x] AI disclosure wording approved

---

## ✅ FINANCE & TAX (G12 PASS)

- [x] Total cost: $0 (free tier only)
- [x] Prize tracker: $46k total (Gold $20k, Silver $10k, Bronze $6k, 2× Creative $5k)
- [x] Payout method: Bank transfer / ship to address
- [x] Timeline: Max 60 days
- [x] W-8BEN form: **FOUNDER ACTION REQUIRED** - download from irs.gov
- [x] US withholding: 15% (Indonesia-US treaty Art 21)
- [x] Indonesia tax: SPT Tahunan OP, PPh 21 verification needed
- [x] No digital services VAT

---

## ✅ TECHNICAL QUALITY

- [x] Pipeline validated: NLP → Scanner → Analyzer → Reporter (--test flag)
- [x] 3 UGOS capabilities chained: Surveillance → Video → Knowledge → Files
- [x] 3 expert agents: Scanner, Analyzer, Reporter
- [x] UGOS confirmation gates: batch (clips) + single (briefing)
- [x] Error handling: 24 codes, fallback chains, user messages
- [x] NLP parsing: timeframe, event_type, camera, confidence filters
- [x] CLI: 3 capabilities registered, help text, --test mode
- [x] Skill Package: 37.9 KB, 21 files, Uliya standard
- [x] README: hero, quickstart, architecture, examples, privacy, license
- [x] LICENSE: MIT
- [x] .gitignore: covers secrets, env, Security/, *.mp4

---

## ✅ SUBMISSION ASSETS READY

| Asset | Status | Location |
|-------|--------|----------|
| Project Proposal (PDF) | ⏳ Convert from submission-copy.md | 01-lomba/.../submission-copy.md |
| Skill Package ZIP | ✅ 37.9 KB | 02-repo/watchtower-skill-package.zip |
| Demo Video Script | ✅ 90s script + shot list | 01-lomba/.../demo-video-script.md |
| Submission Copy | ✅ Devpost fields | 01-lomba/.../submission-copy.md |
| Pitch (100 words) | ✅ Variants ready | 01-lomba/.../pitch-100-words.md |
| Demo Video (90s) | ⏳ To record | - |
| GitHub Repo | ⏳ To publish | 02-repo/watchtower/ |

---

## 🎯 FOUNDER ACTION REQUIRED (BEFORE SUBMIT)

| # | Action | Deadline | Status |
|---|--------|----------|--------|
| 1 | **Download & fill Form W-8BEN** (irs.gov) | **NOW** | ⏳ PENDING |
| 2 | Prepare KTP/Paspor, NPWP, Bank details (SWIFT/BIC) | NOW | ⏳ PENDING |
| 3 | Record demo video (90s) | Before submit | ⏳ PENDING |
| 4 | Convert submission-copy.md → PDF (≤1MB) | Before submit | ⏳ PENDING |
| 5 | Publish GitHub repo (public) | Before submit | ⏳ PENDING |
| 5 | Upload Skill Package ZIP to Devpost | Before deadline | ⏳ PENDING |
| 6 | Fill Devpost form (all fields) | Before deadline | ⏳ PENDING |
| 7 | Upload demo video to YouTube (unlisted) | Before deadline | ⏳ PENDING |
| 8 | **CLICK SUBMIT** (buffer 6 hours) | **2026-11-16 08:45 WIB** | ⏳ PENDING |

---

## 🚀 SUBMIT COMMAND SEQUENCE (When Ready)

```bash
# 1. Final validation
watchtower --test "analyze last 24 hours"

# 2. Convert proposal to PDF
# (use submission-copy.md → print to PDF, verify ≤1MB, ≤500 words)

# 3. Upload to Devpost:
# - Title: "Watchtower: AI Security Analyzer for UGREEN NAS"
# - One-liner: "Watchtower transforms unwatched CCTV footage into actionable security briefings..."
# - Upload Skill Package ZIP (watchtower-skill-package.zip)
# - Upload YouTube video link
# - Fill all form fields
# - Check AI disclosure box

# 6. CLICK SUBMIT (before 2026-11-16 08:45 WIB = 6hr buffer)
```

---

## 📊 FINAL STATUS

| Phase | Complete | Notes |
|-------|----------|-------|
| F1 Kickoff | ✅ | Legal G11 PASS, Finance G12 PASS |
| F2 Ideation | ✅ | Watchtower locked |
| F3 Architecture | ✅ | Blueprint, tasks, story |
| F4 Build (M1-M6) | ✅ | Pipeline functional |
| F5 QA | ✅ | 12/12 Gates PASS |
| F6 Submit | 🔄 | **Founder actions needed** |
| F7 Post-Mortem | ⏳ | After submit |

---

**READY FOR FOUNDER REVIEW & SUBMIT** 🚀

*Checklist v1.0 - Updated 2026-11-02 by AHVO2-7 (OPS)*
