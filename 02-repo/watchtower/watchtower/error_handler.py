"""
Error Handling Matrix - Watchtower
24 error codes with severity, detection, recovery, and user messages.
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class ErrorSeverity(Enum):
    CRITICAL = "CRITICAL"  # Complete failure, requires user action
    HIGH = "HIGH"         # Major feature broken, partial functionality
    MEDIUM = "MEDIUM"     # Degraded experience, minor inconvenience
    LOW = "LOW"           # Cosmetic/logging, no functional impact


class ErrorCode:
    """Error code definition."""
    def __init__(self, code: str, category: str, message: str, severity: ErrorSeverity,
                 detection: str, recovery: str, user_message: str):
        self.code = code
        self.category = category
        self.message = message
        self.severity = severity
        self.detection = detection
        self.recovery = recovery
        self.user_message = user_message


ERROR_REGISTRY: Dict[str, ErrorCode] = {}

def register_error(code: ErrorCode):
    ERROR_REGISTRY[code.code] = code


# ============================================================
# SURVEILLANCE ERRORS (SUR-001 to SUR-006)
# ============================================================

register_error(ErrorCode(
    "SUR-001", "Surveillance", "Camera not authorized",
    ErrorSeverity.HIGH,
    "Exception on UGOS call: camera_id not in authorized list",
    "Prompt user to authorize footage folder via UGOS Files capability",
    "No authorized cameras found. Please authorize a footage folder first via Settings > Camera Access."
))

register_error(ErrorCode(
    "SUR-002", "Surveillance", "No events found in timeframe",
    ErrorSeverity.LOW,
    "Empty result from surveillance query",
    "Return empty array + suggestion to widen timeframe",
    "No security events found. Try wider timeframe or check camera authorization."
))

register_error(ErrorCode(
    "SUR-003", "Surveillance", "Invalid timeframe format",
    ErrorSeverity.LOW,
    "NLP parsing exception on timeframe string",
    "Use default (24 hours) + warn user",
    "Invalid timeframe format. Using last 24 hours by default."
))

register_error(ErrorCode(
    "SUR-004", "Surveillance", "Camera offline",
    ErrorSeverity.MEDIUM,
    "Camera status != 'online' from UGOS",
    "Skip camera, continue with others, log warning",
    "Camera '{camera_id}' is offline. Skipping this camera. Available cameras: {available_cameras}."
))

register_error(ErrorCode(
    "SUR-005", "Surveillance", "NLP parsing failed",
    ErrorSeverity.LOW,
    "Regex/parser exception on user query",
    "Use default filters + warn user",
    "Could not fully parse your query. Using basic filters: last 24 hours, all cameras."
))

register_error(ErrorCode(
    "SUR-006", "Surveillance", "Surveillance capability unavailable",
    ErrorSeverity.HIGH,
    "Exception on UGOS surveillance.call()",
    "Fall back to folder scan (NVR export parsing)",
    "Live query unavailable. Scanning footage folder instead..."
))

# ============================================================
# VIDEO ERRORS (VID-001 to VID-008)
# ============================================================

register_error(ErrorCode(
    "VID-001", "Video", "Video capability unavailable",
    ErrorSeverity.HIGH,
    "Exception on UGOS video.call()",
    "Fall back: copy full recording with timestamp metadata",
    "Clip extraction unavailable. Full recording saved with timestamp metadata instead."
))

register_error(ErrorCode(
    "VID-002", "Video", "Codec not supported",
    ErrorSeverity.MEDIUM,
    "Extraction exception: HEVC/H.265 not supported on ARM",
    "Fall back: copy full file with timestamp metadata",
    "Codec issue: {codec} not supported on this device. Full recording saved with timestamp metadata."
))

register_error(ErrorCode(
    "VID-003", "Video", "Seek/timestamp error",
    ErrorSeverity.MEDIUM,
    "Extraction exception: timestamp seek failed",
    "Fall back: copy recording from event time ±padding",
    "Timestamp seek failed. Saving recording from event window ±{padding}s."
))

register_error(ErrorCode(
    "VID-004", "Video", "Output folder not writable",
    ErrorSeverity.HIGH,
    "PermissionError on write to output folder",
    "Guide user to authorize folder via UGOS",
    "Cannot write to output folder. Please authorize /Security/ folder first."
))

register_error(ErrorCode(
    "VID-005", "Video", "Disk space full",
    ErrorSeverity.CRITICAL,
    "OSError ENOSPC on write",
    "Abort operation, guide user to free space",
    "Insufficient disk space. Free up space and retry."
))

register_error(ErrorCode(
    "VID-006", "Video", "Source file missing",
    ErrorSeverity.HIGH,
    "FileNotFoundError on source recording",
    "Skip event + log, continue others",
    "Source recording not found. Skipping this event."
))

register_error(ErrorCode(
    "VID-007", "Video", "User declines confirmation",
    ErrorSeverity.LOW,
    "User input = 'no' on confirmation prompt",
    "Cancel batch, return partial results",
    "Operation cancelled by user. {count} clips saved at {path}."
))

register_error(ErrorCode(
    "VID-008", "Video", "Clip too large",
    ErrorSeverity.MEDIUM,
    "File size > limit (e.g., 2GB on ARM)",
    "Split or compress, or copy with warning",
    "Clip exceeds size limit ({size}MB). Splitting into segments or copying full recording."
))

# ============================================================
# KNOWLEDGE ERRORS (KNO-001 to KNO-007)
# ============================================================

register_error(ErrorCode(
    "KNO-001", "Knowledge", "Knowledge capability unavailable",
    ErrorSeverity.HIGH,
    "Exception on UGOS knowledge.call()",
    "Template-based briefing (static, no AI)",
    "AI briefing unavailable. Generating standard template report instead."
))

register_error(ErrorCode(
    "KNO-002", "Knowledge", "LLM timeout",
    ErrorSeverity.MEDIUM,
    "Timeout > 30s on Nemotron call",
    "Template-based briefing",
    "AI reasoning timed out ({seconds}s). Generating standard template report instead."
))

register_error(ErrorCode(
    "KNO-003", "Knowledge", "LLM rate limited",
    ErrorSeverity.MEDIUM,
    "429 response from NIM/OpenRouter",
    "Switch model (NIM→OpenRouter→Ollama)",
    "AI service busy ({requests}/min limit). Switching to backup model: {fallback_model}."
))

register_error(ErrorCode(
    "KNO-004", "Knowledge", "LLM hallucination detected",
    ErrorSeverity.HIGH,
    "Validation fails on AI output",
    "Template fallback",
    "AI output failed validation. Generating verified template report instead."
))

register_error(ErrorCode(
    "KNO-005", "Knowledge", "Files write failed",
    ErrorSeverity.HIGH,
    "PermissionError/OSError on write",
    "Retry once, guide user",
    "Cannot write report. Check folder authorization and try again."
))

register_error(ErrorCode(
    "KNO-006", "Knowledge", "HTML validation failed",
    ErrorSeverity.MEDIUM,
    "Invalid HTML generated",
    "Sanitize + retry with safe template",
    "Report formatting issue. Regenerating with safe template."
))

register_error(ErrorCode(
    "KNO-007", "Knowledge", "User declines confirmation",
    ErrorSeverity.LOW,
    "User input = 'no' on confirmation",
    "Cancel, return clips path",
    "Briefing cancelled by user. Clips available at {path}."
))

# ============================================================
# SYSTEM ERRORS (SYS-001 to SYS-005)
# ============================================================

register_error(ErrorCode(
    "SYS-001", "System", "UGOS not available",
    ErrorSeverity.CRITICAL,
    "Import/connection failed",
    "Abort + guide user",
    "UGOS not detected. Ensure Skill runs on UGREEN NAS device."
))

register_error(ErrorCode(
    "SYS-002", "System", "Model (Nemotron) unavailable",
    ErrorSeverity.HIGH,
    "404/503 from NIM API",
    "Switch to OpenRouter/Ollama fallback",
    "Primary model unavailable. Switching to backup: {fallback_model}."
))

register_error(ErrorCode(
    "SYS-003", "System", "All fallbacks exhausted",
    ErrorSeverity.CRITICAL,
    "All recovery options failed",
    "Abort + diagnostic + user guidance",
    "All recovery options failed. Run 'watchtower diagnose' for details."
))

register_error(ErrorCode(
    "SYS-004", "System", "Config corrupted",
    ErrorSeverity.HIGH,
    "JSON decode error on config file",
    "Reset to defaults, re-authorize folders",
    "Config corrupted. Reset to defaults. Re-authorize folders."
))

register_error(ErrorCode(
    "SYS-005", "System", "Dependency missing",
    ErrorSeverity.HIGH,
    "ImportError on required module",
    "Guide install",
    "Required component missing. Run 'pip install -e .' to fix."
))


def get_error(code: str) -> Optional[ErrorCode]:
    """Get error code by ID."""
    return ERROR_REGISTRY.get(code)


def get_errors_by_severity(severity: ErrorSeverity) -> List[ErrorCode]:
    """Get all errors of a given severity."""
    return [e for e in ERROR_REGISTRY.values() if e.severity == severity]


def get_errors_by_category(category: str) -> List[ErrorCode]:
    """Get all errors of a given category."""
    return [e for e in ERROR_REGISTRY.values() if e.category == category]


def format_user_message(code: str, **kwargs) -> str:
    """Format user message with kwargs."""
    error = get_error(code)
    if error:
        try:
            return error.user_message.format(**kwargs)
        except KeyError:
            return error.user_message
    return f"Unknown error: {code}"


# For testing
if __name__ == "__main__":
    print(f"Total error codes: {len(ERROR_REGISTRY)}")
    print(f"CRITICAL: {len(get_errors_by_severity(ErrorSeverity.CRITICAL))}")
    print(f"HIGH: {len(get_errors_by_severity(ErrorSeverity.HIGH))}")
    print(f"MEDIUM: {len(get_errors_by_severity(ErrorSeverity.MEDIUM))}")
    print(f"LOW: {len(get_errors_by_severity(ErrorSeverity.LOW))}")
    
    # Test formatting
    print(format_user_message("VID-002", codec="HEVC"))
    print(format_user_message("KNO-002", seconds=30, fallback_model="OpenRouter"))