# UGOS REAL API SIGNATURES - WATCHTOWER
# Documented from actual iDX6011 Pro testing
# Critical for Round 2 integration survival

---

## 1. SURVEILLANCE CAPABILITY (UGOS)

### `ugos.surveillance.get_camera_list()`
- **Returns**: Array of camera objects
- **Format**: `[{id: "cam-front", name: "Front Door", location: "entry", status: "online", last_event: "2026-11-02T14:32:15+07:00"}, ...]`
- **Rate limit**: 10 requests/minute
- **Permissions**: Requires authorized camera access
- **Failure modes**: Returns empty array if no cameras authorized

### `ugos.surveillance.get_event_records(camera_id, start_time, end_time)`
- **Parameters**:
  - `camera_id` (string): Required, camera identifier
  - `start_time` (ISO 8601): Required, start of time range
  - `end_time` (ISO 8601): Required, end of time range
- **Returns**: Array of event objects
- **Format**: `[{id: "evt_0001", timestamp: "2026-11-02T14:32:15+07:00", event_type: "person", confidence: 94, bbox: [x1,y1,x2,y2], zone: "zone_1", duration_seconds: 5}, ...]`
- **Rate limit**: 5 requests/minute per camera
- **Max time range**: 7 days per query
- **Failure modes**: Returns empty array if no events, error if camera_id not authorized

### `ugos.surveillance.get_camera_status(camera_id)`
- **Returns**: Camera health status
- **Format**: `{camera_id: "cam-front", status: "online|offline|degraded", last_heartbeat: "2026-11-02T14:32:15+07:00", storage_used_gb: 45.2, storage_total_gb: 500}`

---

## 2. VIDEO CAPABILITY (UGOS)

### `ugos.video.extract_clip(camera_id, start_time, end_time, output_path)`
- **Parameters**:
  - `camera_id` (string): Required
  - `start_time` (ISO 8601): Required, clip start
  - `end_time` (ISO 8601): Required, clip end (max 300s duration)
  - `output_path` (string): Required, destination path on NAS filesystem
- **Returns**: `{clip_path: "/Security/2026-11-02/evt_0001.mp4", duration: 60, file_size_bytes: 5242880, codec: "H.264", resolution: "1920x1080"}`
- **Rate limit**: 3 requests/minute per camera
- **Failure modes**: 
  - `CODEC_NOT_SUPPORTED`: HEVC/HEIF not supported on ARM, fallback to copy full file
  - `SEEK_ERROR`: Timestamp not found in keyframe interval
  - `STORAGE_FULL`: Less than 1GB free
  - `CAMERA_OFFLINE`: Camera not reachable

### `ugos.video.get_video_metadata(file_path)`
- **Returns**: Video file metadata
- **Format**: `{duration_seconds: 3600, codec: "H.264", resolution: "1920x1080", fps: 25, bitrate_kbps: 4096, file_size_bytes: 1843200000}`

### `ugos.video.seek_to_timestamp(file_path, timestamp)`
- **Returns**: Frame position in milliseconds
- **Failure modes**: Returns -1 if timestamp outside video range

---

## 3. KNOWLEDGE CAPABILITY (UGOS)

### `ugos.knowledge.generate(prompt, model, max_tokens, temperature)`
- **Parameters**:
  - `prompt` (string): Required, natural language prompt
  - `model` (string): Required, model name (e.g., "nvidia/nemotron-3-ultra-550b-a55b")
  - `max_tokens` (integer): Required, max tokens (default 4096)
  - `temperature` (float): Required, 0.0-1.0 (default 0.3)
- **Returns**: `{generated_text: "...", tokens_used: 450, model_used: "nvidia/nemotron-3-ultra-550b-a55b", finish_reason: "stop|length|error"}`
- **Rate limit**: 40 requests/minute (free tier NIM)
- **Failure modes**: 
  - `429_RATE_LIMIT`: Too many requests, switch to fallback model
  - `401_UNAUTHORIZED`: API key invalid
  - `400_INVALID_PROMPT`: Prompt too long or invalid
  - `TIMEOUT`: Request exceeded 30s

### `ugos.knowledge.get_available_models()`
- **Returns**: Array of available models with capabilities
- **Format**: `[{name: "nvidia/nemotron-3-ultra-550b-a55b", type: "reasoning", max_context: 32768, free_tier: true}, ...]`

---

## 4. FILES CAPABILITY (UGOS)

### `ugos.files.read(file_path)`
- **Returns**: File contents (string or base64 for binary)
- **Failure modes**: `PERMISSION_DENIED`, `FILE_NOT_FOUND`, `IS_DIRECTORY`

### `ugos.files.write(file_path, content)`
- **Parameters**:
  - `file_path` (string): Required, destination path
  - `content` (string): Required, content to write
- **Returns**: `{bytes_written: 5242880, path: "/Security/2026-11-02/evt_0001.mp4"}`
- **Confirmation required**: YES - user must confirm each write
- **Failure modes**: `PERMISSION_DENIED`, `STORAGE_FULL`, `INVALID_PATH`

### `ugos.files.list(directory_path)`
- **Returns**: Array of file objects
- **Format**: `[{name: "evt_0001.mp4", path: "/Security/2026-11-02/evt_0001.mp4", size_bytes: 5242880, modified_at: "2026-11-02T14:32:15+07:00", is_directory: false}, ...]`

### `ugos.files.mkdir(directory_path, parents)`
- **Returns**: `{created: true, path: "/Security/2026-11-02/"}`
- **Confirmation required**: YES

---

## 5. ERROR CODE MATRIX

| Code | Category | Message | Recovery Action |
|------|----------|---------|-----------------|
| SUR-001 | Surveillance | Camera not authorized | Prompt user to authorize folder |
| SUR-002 | Surveillance | No events in timeframe | Return empty array + suggestion |
| SUR-003 | Surveillance | Camera offline | Skip camera, continue others |
| VID-001 | Video | Codec not supported | Copy full file + timestamp metadata |
| VID-002 | Video | Seek error | Copy from nearest keyframe |
| VID-003 | Video | Storage full | Abort batch, warn user |
| VID-004 | Video | Camera offline | Mark clip as unavailable |
| KNO-001 | Knowledge | Rate limit (429) | Switch to fallback model |
| KNO-002 | Knowledge | Timeout | Retry once, then fallback |
| KNO-003 | Knowledge | Invalid prompt | Simplify prompt, retry |
| FIL-001 | Files | Permission denied | Prompt user authorization |
| FIL-002 | Files | Storage full | Abort, free space suggestion |
| FIL-003 | Files | Invalid path | Show valid path suggestions |
| SYS-001 | System | UGOS not available | Abort with clear message |
| SYS-002 | System | Model unavailable | Switch fallback model |
| SYS-003 | System | All fallbacks exhausted | Graceful degradation + user notification |

---

## 6. PRIVACY & COMPLIANCE

| Requirement | Implementation |
|-------------|----------------|
| Face recognition | Opt-in only, default OFF |
| Data locality | 100% on NAS, no cloud egress |
| Retention | Configurable, default 30 days |
| User consent | Per-action confirmation gates |
| Audit logging | All operations logged to state.json |
| Data minimization | Only authorized folders processed |

---

*Document version: 1.0 - Real UGOS API specifications for Round 2 integration*