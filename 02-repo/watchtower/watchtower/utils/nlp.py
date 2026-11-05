"""
NLP Utilities - Natural Language Parsing for Watchtower
Parses user queries into structured timeframes, filters, and intents.
"""

import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dateutil import parser as date_parser


# Timeframe patterns
TIMEFRAME_PATTERNS = [
    (r"last\s+(\d+)\s*hours?", lambda m: timedelta(hours=int(m.group(1)))),
    (r"last\s+(\d+)\s*days?", lambda m: timedelta(days=int(m.group(1)))),
    (r"last\s+(\d+)\s*weeks?", lambda m: timedelta(weeks=int(m.group(1)))),
    (r"past\s+(\d+)\s*hours?", lambda m: timedelta(hours=int(m.group(1)))),
    (r"past\s+(\d+)\s*days?", lambda m: timedelta(days=int(m.group(1)))),
    (r"yesterday", lambda m: timedelta(days=1)),
    (r"today", lambda m: timedelta(days=0)),
    (r"this\s+week", lambda m: timedelta(days=7)),
    (r"last\s+week", lambda m: timedelta(days=14)),
]

# Event type patterns
EVENT_TYPE_PATTERNS = {
    "person": [r"\bperson\b", r"\bpeople\b", r"\bhuman\b", r"\bindividual\b"],
    "vehicle": [r"\bvehicle\b", r"\bcar\b", r"\btruck\b", r"\bmotorcycle\b", r"\bvan\b"],
    "motion": [r"\bmotion\b", r"\bmovement\b", r"\bactivity\b"],
    "package": [r"\bpackage\b", r"\bdelivery\b", r"\bparcel\b"],
}

# Camera patterns
CAMERA_PATTERNS = {
    "front": [r"\bfront\s*(door|doorway|entry|entrance)?\b", r"\bentry\b", r"\bfront\b"],
    "back": [r"\bback\s*(door|yard)?\b", r"\bbackyard\b", r"\brear\b"],
    "garage": [r"\bgarage\b", r"\bdriveway\b"],
    "side": [r"\bside\s*(gate|door|yard)?\b", r"\bside\b"],
    "cam-": [r"\bcam[\s-]?(\d+)\b", r"\bcamera[\s-]?(\d+)\b"],
}

# Confidence patterns
CONFIDENCE_PATTERNS = [
    (r"confidence\s+(above|over|greater\s+than)\s*(\d+)", lambda m: ("min", int(m.group(2)))),
    (r"confidence\s+(below|under|less\s+than)\s*(\d+)", lambda m: ("max", int(m.group(2)))),
    (r"high\s+confidence", lambda m: ("min", 80)),
    (r"low\s+confidence", lambda m: ("max", 50)),
]


def parse_natural_language_query(
    query: str,
    explicit_timeframe: Optional[str] = None,
    explicit_filters: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Parse natural language query into structured parameters.
    
    Args:
        query: Natural language query string
        explicit_timeframe: Optional explicit timeframe override
        explicit_filters: Optional explicit filters override
    
    Returns:
        Dict with keys:
            - timeframe: Dict with start/end datetime
            - filters: Dict with camera_id, event_type, min_confidence
            - original_query: str
    """
    query_lower = query.lower().strip()
    now = datetime.now()
    
    # Parse timeframe
    timeframe = _parse_timeframe(query_lower, explicit_timeframe, now)
    
    # Parse filters
    filters = _parse_filters(query_lower, explicit_filters)
    
    return {
        "timeframe": timeframe,
        "filters": filters,
        "original_query": query
    }


def _parse_timeframe(query: str, explicit: Optional[str], now: datetime) -> Dict[str, datetime]:
    """Parse timeframe from query or explicit override."""
    end_time = now
    start_time = now - timedelta(hours=24)  # Default: last 24 hours
    
    # Check explicit override first
    if explicit:
        try:
            # Try parsing as relative (e.g., "24h", "7d")
            if explicit.endswith('h'):
                start_time = now - timedelta(hours=int(explicit[:-1]))
            elif explicit.endswith('d'):
                start_time = now - timedelta(days=int(explicit[:-1]))
            elif explicit.endswith('w'):
                start_time = now - timedelta(weeks=int(explicit[:-1]))
            else:
                # Try absolute date
                start_time = date_parser.parse(explicit)
        except Exception:
            pass  # Fall back to default
    
    # Check query for timeframe patterns
    for pattern, func in TIMEFRAME_PATTERNS:
        match = re.search(pattern, query)
        if match:
            delta = func(match)
            if isinstance(delta, timedelta):
                start_time = now - delta
            break
    
    return {"start": start_time, "end": end_time}


def _parse_filters(query: str, explicit: Optional[Dict] = None) -> Dict[str, Any]:
    """Parse filters from query."""
    filters = {}
    
    # Start with explicit filters
    if explicit:
        filters.update(explicit)
    
    # Event types
    event_types = []
    for etype, patterns in EVENT_TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, query):
                event_types.append(etype)
                break
    if event_types:
        filters["event_type"] = list(set(event_types))
    
    # Camera
    camera_id = None
    for cam_key, patterns in CAMERA_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                if cam_key == "cam-":
                    camera_id = f"cam-{match.group(1)}"
                else:
                    camera_id = f"cam-{cam_key}"
                break
        if camera_id:
            break
    if camera_id:
        filters["camera_id"] = camera_id
    
    # Confidence
    for pattern, func in CONFIDENCE_PATTERNS:
        match = re.search(pattern, query)
        if match:
            constraint, value = func(match)
            if constraint == "min":
                filters["min_confidence"] = value
            elif constraint == "max":
                filters["max_confidence"] = value
            break
    
    return filters


def parse_timeframe_string(timeframe_str: str) -> timedelta:
    """Parse timeframe string like '24h', '7d', '2w' into timedelta."""
    timeframe_str = timeframe_str.strip().lower()
    if timeframe_str.endswith('h'):
        return timedelta(hours=int(timeframe_str[:-1]))
    elif timeframe_str.endswith('d'):
        return timedelta(days=int(timeframe_str[:-1]))
    elif timeframe_str.endswith('w'):
        return timedelta(weeks=int(timeframe_str[:-1]))
    elif timeframe_str.endswith('m'):
        return timedelta(minutes=int(timeframe_str[:-1]))
    else:
        # Assume hours if no unit
        return timedelta(hours=int(timeframe_str))


# For testing
if __name__ == "__main__":
    test_queries = [
        "analyze last 24 hours",
        "show person detections yesterday 18:00-22:00",
        "generate briefing for front door camera last week",
        "extract clips for all vehicle detections today",
        "show high confidence person detections last 2 days",
        "cam-2 motion events this week"
    ]
    
    for q in test_queries:
        result = parse_natural_language_query(q)
        print(f"\nQuery: {q}")
        print(f"  Timeframe: {result['timeframe']['start']} to {result['timeframe']['end']}")
        print(f"  Filters: {result['filters']}")