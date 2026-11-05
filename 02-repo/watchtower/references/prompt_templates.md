# Prompt Templates - Watchtower
# Few-shot prompts for 3 Expert Agents (Scanner, Analyzer, Reporter)
# Used with NVIDIA Nemotron 3 Ultra via NVIDIA NIM

---

## Scanner Agent - Natural Language Query Parsing

### System Prompt
```
You are a natural language parser for a security camera query system.
Parse user queries into structured timeframes and filters.
Output ONLY valid JSON. No explanations.
```

### Few-Shot Examples

#### Example 1: Basic timeframe
**User:** "analyze last 24 hours"
**Output:**
```json
{
  "timeframe": {"start": "2026-11-01T14:30:00+07:00", "end": "2026-11-02T14:30:00+07:00"},
  "filters": {}
}
```

#### Example 2: With event type filter
**User:** "show person detections yesterday"
**Output:**
```json
{
  "timeframe": {"start": "2026-11-01T00:00:00+07:00", "end": "2026-11-02T00:00:00+07:00"},
  "filters": {"event_type": ["person"]}
}
```

#### Example 3: Multiple filters
**User:** "high confidence vehicle detections last 2 days from garage camera"
**Output:**
```json
{
  "timeframe": {"start": "2026-10-31T14:30:00+07:00", "end": "2026-11-02T14:30:00+07:00"},
  "filters": {
    "event_type": ["vehicle"],
    "camera_id": "cam-garage",
    "min_confidence": 80
  }
}
```

#### Example 4: Complex query
**User:** "generate briefing for front door camera last week 18:00-22:00"
**Output:**
```json
{
  "timeframe": {"start": "2026-10-26T18:00:00+07:00", "end": "2026-11-02T22:00:00+07:00"},
  "filters": {
    "camera_id": "cam-front",
    "event_type": ["person", "vehicle", "package"]
  }
}
```

#### Example 5: No timeframe (default 24h)
**User:** "what happened at back door?"
**Output:**
```json
{
  "timeframe": {"start": "2026-11-01T14:30:00+07:00", "end": "2026-11-02T14:30:00+07:00"},
  "filters": {"camera_id": "cam-backyard"}
}
```

---

## Reporter Agent - AI Reasoning for Security Briefing

### System Prompt
```
You are a professional security analyst generating briefings for homeowners/SMBs.
Analyze events and clips to produce concise, actionable security briefings.
Be concise, professional, and actionable. No fluff.
```

### Template: Standard Briefing

**Input:**
```json
{
  "events": [...],
  "clips": [...],
  "template": "standard"
}
```

**Prompt:**
```
Generate a professional security briefing with these sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
   - Overall threat assessment
   - Key anomaly count
   - Time period covered

2. KEY ANOMALIES DETECTED
   - List top 3-5 most significant events
   - Include timestamp, camera, type, confidence
   - Highlight any critical/high threats

3. PER-CAMERA SUMMARY
   - Table: Camera | Events | Top Threat | Recommendation

4. RECOMMENDATIONS
   - 3-5 actionable items for user
   - Prioritize by threat level
   - Include camera positioning, sensitivity, review suggestions

Format as structured text for HTML conversion.
Tone: Professional, concise, actionable.
Length: ~300-500 words total.
```

**Expected Output Format:**
```
EXECUTIVE SUMMARY:
[2-3 sentences summarizing overall security posture]

KEY ANOMALIES:
1. [Timestamp] | [Camera] | [Type] | [Confidence] | [Why significant]
2. ...

PER-CAMERA SUMMARY:
| Camera | Events | Top Threat | Recommendation |
|--------|--------|------------|----------------|
| Front Door | 3 | Person (94%) | Review visitor log |
| Garage | 1 | Vehicle (87%) | Check delivery log |

RECOMMENDATIONS:
1. [High priority action]
2. [Medium priority action]
3. [Low priority action]
```

### Template: Executive Briefing
```
Generate a CONDENSED executive briefing (max 150 words):
- One-sentence threat assessment
- Top 3 anomalies only
- Top 2 recommendations
Format: Bullet points only.
```

### Template: Detailed Briefing
```
Generate a COMPREHENSIVE detailed briefing:
- Full chronological timeline (all events)
- Per-event analysis with context
- Cross-camera correlation analysis
- Long-term trend observations
- 5+ prioritized recommendations
- Appendix: All events table
```

---

## Analyzer Agent - Clip Extraction Parameters

### System Prompt
```
You are a video processing specialist. Determine optimal clip extraction parameters.
Output ONLY JSON with extraction parameters.
```

### Few-Shot Examples

#### Example 1: Standard extraction
**Input:** "extract clips for 5 person events"
**Output:**
```json
{
  "padding_seconds": 30,
  "output_folder": "/Security/2026-11-02/",
  "codec": "copy",
  "fallback_on_error": true
}
```

#### Example 2: Long events
**Input:** "extract long clips for 2 hour vehicle events"
**Output:**
```json
{
  "padding_seconds": 120,
  "output_folder": "/Security/2026-11-02/",
  "codec": "h264",
  "max_clip_size_mb": 100,
  "split_long_clips": true
}
```

#### Example 3: Batch with confirmation
**Input:** "extract all clips for 15 events, ask once"
**Output:**
```json
{
  "padding_seconds": 30,
  "output_folder": "/Security/2026-11-02/",
  "batch_confirmation": true,
  "codec": "copy",
  "fallback_on_error": true
}
```

---

## UGOS Confirmation Prompts

### Single Confirmation (Briefing Generation)
```
⚠️ UGOS CONFIRMATION REQUIRED
Generate standard HTML security briefing with 5 embedded clips?
Report will be saved to /Security/2026-11-02/security_briefing_20261102_143000.html
[y/N]:
```

### Batch Confirmation (Clip Extraction)
```
⚠️ UGOS BATCH CONFIRMATION REQUIRED
Extract 8 clips to /Security/2026-11-02/?

Items (8):
  1. cam-front | Person | 14:32:15 | ±30s
  2. cam-garage | Vehicle | 16:15:30 | ±30s
  3. cam-backyard | Motion | 18:44:22 | ±30s
  4. cam-front | Person | 20:10:05 | ±30s
  5. cam-side | Package | 21:30:00 | ±30s
  5. ... and 3 more items

[y/N]:
```

### Single Confirmation (Folder Authorization)
```
⚠️ UGOS CONFIRMATION REQUIRED
Authorize access to footage folder: /mnt/cameras/?
This allows Watchtower to read camera recordings for analysis.
[y/N]:
```

---

## Error Handling Prompts

### Capability Unavailable
```
[WARNING] UGOS Surveillance capability unavailable.
Falling back to footage folder scan at /mnt/cameras/.
Proceed with folder scan? [y/N]:
```

### Clip Extraction Failed
```
[ERROR] Clip extraction failed for event evt_0003 (codec issue).
Fallback: Copy full recording with timestamp metadata?
Source: /mnt/cameras/cam-front/20261102_143000.mp4
Destination: /Security/2026-11-02/evt_0003_FULL_RECORDING.mp4
[y/N]:
```

### User Declined Confirmation
```
[CANCELLED] Operation cancelled by user.
Partial results saved: 3 clips at /Security/2026-11-02/
Generate briefing with available clips? [y/N]:
```

### LLM Timeout
```
[WARNING] AI reasoning timed out (30s).
Fallback: Generate template-based briefing without AI analysis?
[y/N]:
```

---

*Prompt Templates v1.0*
*Compatible with: NVIDIA Nemotron 3 Ultra via NVIDIA NIM*
*Temperature: 0.3 (reasoning) | 0.7 (creative)*
*Max tokens: 4096*