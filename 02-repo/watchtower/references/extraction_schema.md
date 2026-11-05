# Extraction Schema - Watchtower
# JSON Schema definitions for event, clip, and briefing data structures

## Event Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SecurityEvent",
  "type": "object",
  "required": ["id", "timestamp", "camera_id", "event_type", "confidence"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^evt_\\d{4}$",
      "description": "Unique event identifier"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Event timestamp in ISO 8601 format"
    },
    "camera_id": {
      "type": "string",
      "pattern": "^cam-[a-z0-9-]+$",
      "description": "Camera identifier"
    },
    "camera_name": {
      "type": "string",
      "description": "Human-readable camera name"
    },
    "camera_location": {
      "type": "string",
      "enum": ["entry", "driveway", "rear", "side", "indoor", "other"],
      "description": "Camera location category"
    },
    "event_type": {
      "type": "string",
      "enum": ["person", "vehicle", "motion", "package", "unknown"],
      "description": "Type of detected event"
    },
    "confidence": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Detection confidence percentage"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "zone": {"type": "string", "description": "Detection zone identifier"},
        "bbox": {
          "type": "array",
          "items": {"type": "integer"},
          "minItems": 4,
          "maxItems": 4,
          "description": "Bounding box [x1, y1, x2, y2]"
        },
        "duration_seconds": {
          "type": "integer",
          "minimum": 0,
          "description": "Event duration in seconds"
        }
      },
      "additionalProperties": true
    }
  }
}
```

## Clip Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VideoClip",
  "type": "object",
  "required": ["clip_path", "event_ref", "camera_id", "start_time", "end_time", "duration"],
  "properties": {
    "clip_path": {
      "type": "string",
      "description": "Absolute path to clip file"
    },
    "event_ref": {
      "type": "string",
      "description": "Reference to source event ID"
    },
    "camera_id": {
      "type": "string",
      "description": "Source camera identifier"
    },
    "start_time": {
      "type": "string",
      "format": "date-time",
      "description": "Clip start timestamp"
    },
    "end_time": {
      "type": "string",
      "format": "date-time",
      "description": "Clip end timestamp"
    },
    "duration": {
      "type": "number",
      "minimum": 0,
      "description": "Clip duration in seconds"
    },
    "file_size": {
      "type": "integer",
      "minimum": 0,
      "description": "File size in bytes"
    },
    "event_type": {
      "type": "string",
      "enum": ["person", "vehicle", "motion", "package", "unknown"]
    },
    "confidence": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
    },
    "fallback": {
      "type": "boolean",
      "default": false,
      "description": "True if full recording copied instead of extracted clip"
    },
    "reason": {
      "type": "string",
      "description": "Reason for fallback if applicable"
    }
  }
}
```

## Briefing Report Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SecurityBriefing",
  "type": "object",
  "required": ["report_path", "generated_at", "event_count", "clip_count", "cameras_involved"],
  "properties": {
    "report_path": {
      "type": "string",
      "description": "Path to generated HTML report"
    },
    "generated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Report generation timestamp"
    },
    "event_count": {
      "type": "integer",
      "minimum": 0
    },
    "clip_count": {
      "type": "integer",
      "minimum": 0
    },
    "cameras_involved": {
      "type": "array",
      "items": {"type": "string"}
    },
    "event_counts": {
      "type": "object",
      "additionalProperties": {"type": "integer"}
    },
    "threat_levels": {
      "type": "object",
      "properties": {
        "Critical": {"type": "integer"},
        "High": {"type": "integer"},
        "Medium": {"type": "integer"},
        "Low": {"type": "integer"},
        "Info": {"type": "integer"}
      }
    },
    "template": {
      "type": "string",
      "enum": ["standard", "executive", "detailed"]
    }
  }
}
```

## UGOS Capability Input/Output Schemas

### watchtower.query_events
**Input:**
```json
{
  "query": {"type": "string", "required": true},
  "timeframe": {"type": "string"},
  "filters": {
    "type": "object",
    "properties": {
      "camera_id": {"type": "string"},
      "event_type": {"type": "array", "items": {"type": "string"}},
      "min_confidence": {"type": "integer", "minimum": 0, "maximum": 100},
      "max_confidence": {"type": "integer", "minimum": 0, "maximum": 100}
    }
  }
}
```

**Output:** Array of Event objects (see Event Schema)

### watchtower.extract_clips
**Input:**
```json
{
  "events": {"type": "array", "items": {"$ref": "#/definitions/Event"}},
  "padding_seconds": {"type": "integer", "default": 30, "minimum": 0},
  "output_folder": {"type": "string", "default": "/Security/YYYY-MM-DD/"}
}
```

**Output:** Array of Clip objects (see Clip Schema)

### watchtower.generate_briefing
**Input:**
```json
{
  "events": {"type": "array", "items": {"$ref": "#/definitions/Event"}},
  "clips": {"type": "array", "items": {"$ref": "#/definitions/Clip"}},
  "template": {"type": "string", "enum": ["standard", "executive", "detailed"], "default": "standard"}
}
```

**Output:** BriefingReport object (see Briefing Report Schema)

---

## Validation Rules

1. **Event ID Format**: Must match `^evt_\d{4}$`
2. **Camera ID Format**: Must match `^cam-[a-z0-9-]+$`
3. **Timestamp Format**: ISO 8601 with timezone (e.g., `2026-11-02T14:32:15+07:00`)
4. **Confidence Range**: 0-100 inclusive
5. **Clip Path**: Must be under `/Security/` base path
6. **Event Types**: Must be one of: person, vehicle, motion, package, unknown
7. **Template Types**: Must be one of: standard, executive, detailed

---

*Schema version: 1.0.0*
*Compatible with: Uliya Skill Development Standard v1.0*