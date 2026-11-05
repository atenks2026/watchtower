---
name: watchtower
description: "AI Security Analyzer: Natural language query → cross-camera anomaly detection → HTML security briefing with video clips. Turns unwatched footage into actionable security intelligence."
version: "1.0.0"
author: "AHVO2 Team"
license: "MIT"
tags: [surveillance, security, video-analysis, home-automation]
ugos_capabilities: [surveillance, video, knowledge, files]
---

# Watchtower — AI Security Analyzer

## User Goal
Help homeowners and SMBs understand what their security cameras actually recorded without watching hours of footage. Transform passive CCTV recording into actionable security intelligence through natural language queries, automated clip extraction, and AI-generated briefings.

## Required Inputs
- **Authorized footage folder**: Path to camera recordings (e.g., `/mnt/cameras/` or NVR export folder)
- **Timeframe**: Natural language (e.g., "last 24 hours", "yesterday 18:00-22:00", "last 7 days")
- **Optional filters**: Camera ID, event type (person/vehicle/motion), confidence threshold

## Supported CLI Capabilities

### 1. `watchtower.query_events`
**Description**: Query security events using natural language.
**Inputs**:
- `query` (string, required): Natural language query (e.g., "person detections last 24h")
- `timeframe` (string, optional): Explicit timeframe override
- `filters` (object, optional): `{camera_id, event_type, min_confidence}`
**Output**: Structured event list `[{timestamp, camera_id, event_type, confidence, metadata}]`
**Confirmation**: No (read-only)

### 2. `watchtower.extract_clips`
**Description**: Extract video clips around detected events.
**Inputs**:
- `events` (array, required): Event list from `query_events`
- `padding_seconds` (integer, default: 30): Seconds before/after event
- `output_folder` (string, default: `/Security/YYYY-MM-DD/`): Destination
**Output**: Clip files + metadata `[{clip_path, event_ref, start_time, end_time, camera_id}]`
**Confirmation**: **YES** — Batch approval for multiple clips

### 3. `watchtower.generate_briefing`
**Description**: Generate HTML security briefing with embedded clips.
**Inputs**:
- `events` (array, required): Event list
- `clips` (array, required): Clip metadata from `extract_clips`
- `template` (string, optional): `standard` | `executive` | `detailed`
**Output**: `security_briefing_YYYYMMDD_HHMM.html` with executive summary, timeline, embedded video clips, per-camera summary, recommendations
**Confirmation**: **YES** — Single approval for HTML report

## Expert Agent Orchestration Workflow

```
User Query (Natural Language)
        │
        ▼
┌───────────────────┐
│   SCANNER AGENT   │  ← UGOS Surveillance: query camera events
│  (Query Events)   │
└───────────────────┘
        │
        ▼ (Event List)
┌───────────────────┐
│   ANALYZER AGENT  │  ← UGOS Video: extract clips ±30s
│  (Extract Clips)  │  ← UGOS Files: save to /Security/
└───────────────────┘
        │
        ▼ (Clips + Metadata)
┌───────────────────┐
│   REPORTER AGENT  │  ← UGOS Knowledge: AI reasoning (Nemotron)
│ (Generate Brief)  │  ← UGOS Files: write HTML report
└───────────────────┘
        │
        ▼
HTML Security Briefing + Clip Folder
```

**Sequential Execution**: Each agent uses the actual output of the previous agent. No vague references.

## Completion/Failure Handling

### Success
- **Query Events**: Returns event list (empty array if none found)
- **Extract Clips**: Returns clip metadata + folder path
- **Generate Briefing**: Returns HTML report path + clip folder path

### No Events Found
> "No security events found in timeframe. Try wider range or check camera authorization."

### Partial Failure (Clips extracted, Briefing failed)
> "Clips extracted successfully at [path]. Briefing generation failed: [reason]. Template briefing available at [fallback_path]."

### User Declines Confirmation
> "Operation cancelled by user. [X] clips saved at [path]."

### Capability Unavailable
> "Live query unavailable. Falling back to footage folder scan..."

## Privacy & Security
- **100% Local Processing**: No external API calls. Footage never leaves NAS.
- **Face Recognition**: Opt-in only (default OFF). BIPA/GDPR/UU PDP compliant.
- **UGOS Confirmation Gates**: All write operations require explicit user approval.
- **No External Dependencies**: Python stdlib + uliya-skill-kit only. No binaries, no external APIs.
- **Data Minimization**: Only processes authorized folders. User controls scope.