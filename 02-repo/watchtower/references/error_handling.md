# Error Handling - Watchtower
# Failure Modes, Recovery Strategies, and User Messages

---

## Error Classification

| Severity | Definition | User Impact | Recovery |
|----------|------------|-------------|----------|
| **CRITICAL** | Skill cannot function | Complete failure | Requires user action |
| **HIGH** | Major feature broken | Partial functionality | Auto-recovery or user action |
| **MEDIUM** | Degraded experience | Minor inconvenience | Auto-recovery |
| **LOW** | Cosmetic/logging | No functional impact | Auto-recovery |

---

## Error Matrix by Capability

### 1. `watchtower.query_events` (Scanner Agent)

| Error Code | Scenario | Severity | Detection | Recovery | User Message |
|------------|----------|----------|-----------|----------|--------------|
| **SUR-001** | Surveillance capability unavailable | HIGH | Exception on UGOS call | Fallback to folder scan | "Live query unavailable. Scanning footage folder instead..." |
| **SUR-002** | No authorized cameras | MEDIUM | Empty camera list | Guide user to authorize folder | "No authorized cameras found. Please authorize a footage folder first." |
| **SUR-003** | Invalid timeframe format | LOW | Parsing exception | Use default (24h) + warn | "Invalid timeframe. Using last 24 hours." |
| **SUR-004** | No events found | LOW | Empty result | Return empty + suggestion | "No security events found. Try wider timeframe or check camera status." |
| **SUR-005** | NLP parsing failed | LOW | Regex/parser exception | Use default filters | "Could not parse query fully. Using basic filters." |
| **SUR-006** | Camera not authorized | MEDIUM | Camera ID not in authorized list | List authorized cameras | "Camera 'X' not authorized. Available: [list]." |

### 2. `watchtower.extract_clips` (Analyzer Agent)

| Error Code | Scenario | Severity | Detection | Recovery | User Message |
|------------|----------|----------|-----------|----------|--------------|
| **VID-001** | Video capability unavailable | HIGH | Exception on UGOS call | Fallback: copy full recording | "Clip extraction unavailable. Copying full recording with timestamp." |
| **VID-002** | Codec not supported | MEDIUM | Extraction exception | Fallback: copy full file | "Codec issue. Full recording saved with timestamp metadata." |
| **VID-003** | Seek/timestamp error | MEDIUM | Extraction exception | Fallback: copy from event time ±padding | "Timestamp seek failed. Saving recording from event window." |
| **VID-004** | Output folder not writable | HIGH | PermissionError on write | Guide user to authorize folder | "Cannot write to output folder. Please authorize /Security/ folder." |
| **VID-005** | Disk space full | CRITICAL | OSError ENOSPC | Abort + guide user | "Insufficient disk space. Free up space and retry." |
| **VID-006** | Source file missing | HIGH | FileNotFoundError | Skip event + log | "Source recording not found. Skipping this event." |
| **VID-007** | User declines confirmation | LOW | User input = no | Cancel batch, return partial | "Operation cancelled. [X] clips saved at [path]." |
| **VID-008** | Clip too large | MEDIUM | File size > limit | Split or compress | "Clip exceeds size limit. Splitting into segments." |

### 3. `watchtower.generate_briefing` (Reporter Agent)

| Error Code | Scenario | Severity | Detection | Recovery | User Message |
|------------|----------|----------|-----------|----------|--------------|
| **KNO-001** | Knowledge capability unavailable | HIGH | Exception on UGOS call | Template-based briefing | "AI briefing unavailable. Generating standard template report." |
| **KNO-002** | LLM timeout | MEDIUM | Timeout > 30s | Template-based briefing | "AI reasoning timed out. Generating standard template report." |
| **KNO-003** | LLM rate limited | MEDIUM | 429 response | Switch model/template | "AI service busy. Generating template report instead." |
| **KNO-004** | LLM hallucination detected | HIGH | Validation fails | Template fallback | "AI output invalid. Generating verified template report." |
| **KNO-005** | Files write failed | HIGH | PermissionError/OSError | Retry + guide user | "Cannot write report. Check folder authorization." |
| **KNO-006** | HTML validation failed | MEDIUM | Invalid HTML generated | Sanitize + retry | "Report formatting issue. Regenerating with safe template." |
| **KNO-007** | User declines confirmation | LOW | User input = no | Cancel, return clips path | "Briefing cancelled. Clips available at [path]." |

### 4. Cross-Cutting / System Errors

| Error Code | Scenario | Severity | Detection | Recovery | User Message |
|------------|----------|----------|-----------|----------|--------------|
| **SYS-001** | UGOS not available | CRITICAL | Import/connection failed | Abort + guide | "UGOS not detected. Ensure skill runs on UGREEN NAS." |
| **SYS-002** | Model (Nemotron) unavailable | HIGH | 404/503 from NIM | Switch to OpenRouter/Ollama | "Primary model unavailable. Switching to backup." |
| **SYS-003** | All fallbacks exhausted | CRITICAL | All recovery failed | Abort + diagnostic | "All recovery options failed. Run `watchtower diagnose` for details." |
| **SYS-004** | Config corrupted | HIGH | JSON decode error | Reset to defaults | "Config corrupted. Reset to defaults. Re-authorize folders." |
| **SYS-005** | Dependency missing | HIGH | ImportError | Guide install | "Required component missing. Run `pip install -e .`" |

---

## Recovery Strategies

### Fallback Chain (Per Capability)
```
Primary UGOS Capability
        ↓ (fails)
Fallback 1: Alternative UGOS capability
        ↓ (fails)
Fallback 2: Local file system operations
        ↓ (fails)
Fallback 3: Template/static response
        ↓ (fails)
Fallback 4: Graceful degradation + user guidance
```

### Model Fallback Chain (LLM)
```
NVIDIA Nemotron 3 Ultra (NIM)
        ↓ (429/timeout/error)
NVIDIA Nemotron 3.5 Super VL (NIM)
        ↓ (429/timeout/error)
OpenRouter: Llama 3.1 70B / Gemini Flash
        ↓ (429/timeout/error)
Ollama Local: Nemotron 3 Ultra quantized
        ↓ (fails)
Template-only mode (no AI)
```

---

## User-Facing Message Guidelines

### Tone Principles
1. **Honest**: Admit failure clearly
2. **Actionable**: Tell user what they can do
3. **Non-technical**: Avoid jargon
4. **Reassuring**: Emphasize data safety
5. **Specific**: Reference actual paths, counts

### Message Template
```
[SEVERITY ICON] [SHORT TITLE]

What happened: [1 sentence, plain language]
What we're doing: [Automatic recovery action]
What you can do: [Specific user action]
Where to find results: [Actual path/location]

Example:
⚠️ CLIP EXTRACTION PARTIAL
What happened: 3 of 10 clips failed due to codec issues.
What we're doing: Full recordings copied with timestamp metadata.
What you can do: Check /Security/2026-11-02/ for all clips.
```

### Severity Icons
- 🔴 **CRITICAL** - Immediate action needed
- 🟠 **HIGH** - Feature broken, workaround exists
- 🟡 **MEDIUM** - Degraded, auto-recovering
- 🟢 **LOW** - Minor, auto-recovered
- 🔵 **INFO** - Status update

---

## Logging & Diagnostics

### Structured Log Format (JSON Lines)
```json
{
  "timestamp": "2026-11-02T14:32:15+07:00",
  "level": "ERROR",
  "code": "VID-002",
  "capability": "watchtower.extract_clips",
  "event_ref": "evt_0003",
  "message": "Codec not supported: HEVC",
  "recovery": "fallback_full_copy",
  "user_message_shown": true,
  "context": {"camera_id": "cam-front", "codec": "hevc"}
}
```

### Diagnostic Command
```bash
watchtower diagnose
```
Outputs:
- System status (UGOS, model, disk, memory)
- Capability health checks
- Recent errors (last 50)
- Config validation
- Authorization status

---

## Testing Error Scenarios

### Unit Test Coverage Targets
| Component | Error Scenarios | Target Coverage |
|-----------|----------------|-----------------|
| Scanner Agent | 6 | 100% |
| Analyzer Agent | 8 | 100% |
| Reporter Agent | 7 | 100% |
| Confirmation Gates | 4 | 100% |
| NLP Parser | 10 | 90% |
| Fallback Chain | 5 | 100% |

### Integration Test Scenarios
1. **Full pipeline with all failures**: Each capability fails once
2. **Model fallback chain**: Primary → backup → local → template
3. **Confirmation flow**: User accepts, declines, cancels mid-batch
4. **Disk full simulation**: Write failures at various stages
5. **Network partition**: UGOS unavailable, model unavailable

---

*Error Handling v1.0 - Watchtower Skill*
*Compatible with: Uliya Skill Development Standard v1.0*
*Last updated: 2026-11-02*