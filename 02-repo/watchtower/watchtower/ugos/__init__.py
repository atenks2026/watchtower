"""
UGOS Capability Wrappers
Interfaces to UGREEN NAS capabilities (Surveillance, Video, Knowledge, Files)
"""

# Capability availability flags (set at runtime)
CAPABILITIES = {
    "surveillance": False,
    "video": False,
    "knowledge": False,
    "files": False,
}

def check_capabilities() -> dict:
    """Check which UGOS capabilities are available."""
    # In real implementation, query UGOS for capability availability
    # For now, return mock status
    return CAPABILITIES.copy()

def set_capability(name: str, available: bool):
    """Set capability availability (for testing/mock)."""
    if name in CAPABILITIES:
        CAPABILITIES[name] = available

__all__ = [
    "CAPABILITIES",
    "check_capabilities",
    "set_capability",
]