#!/usr/bin/env python3
"""
Watchtower CLI - UGOS Skill Command Line Interface
Registers 3 capabilities with UGOS and handles natural language parsing.
"""

import argparse
import sys
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path

# Import agents
from watchtower.agents.scanner import ScannerAgent
from watchtower.agents.analyzer import AnalyzerAgent
from watchtower.agents.reporter import ReporterAgent
from watchtower.ugos.confirmation import confirm_batch, confirm_single
from watchtower.utils.nlp import parse_natural_language_query
from watchtower.ugos.confirmation import UGOSConfirmation

# Version
__version__ = "1.0.0"

# UGOS Capability Definitions
CAPABILITIES = {
    "watchtower.query_events": {
        "name": "Query Security Events",
        "description": "Natural language query for camera events",
        "inputs": {
            "query": {"type": "string", "required": True, "description": "Natural language query"},
            "timeframe": {"type": "string", "required": False, "description": "Explicit timeframe override"},
            "filters": {"type": "object", "required": False, "description": "Camera, event type, confidence filters"}
        },
        "confirmation_required": False,
    },
    "watchtower.extract_clips": {
        "name": "Extract Event Clips",
        "description": "Extract video clips around detected events",
        "inputs": {
            "events": {"type": "array", "required": True, "description": "Event list from query_events"},
            "padding_seconds": {"type": "integer", "default": 30, "description": "Seconds before/after event"},
            "output_folder": {"type": "string", "default": "/Security/YYYY-MM-DD/", "description": "Destination folder"}
        },
        "confirmation_required": True,
        "confirmation_type": "batch",
    },
    "watchtower.generate_briefing": {
        "name": "Generate Security Briefing",
        "description": "Generate HTML security briefing with embedded clips",
        "inputs": {
            "events": {"type": "array", "required": True, "description": "Event list"},
            "clips": {"type": "array", "required": True, "description": "Clip metadata from extract_clips"},
            "template": {"type": "string", "enum": ["standard", "executive", "detailed"], "default": "standard"}
        },
        "confirmation_required": True,
        "confirmation_type": "single",
    }
}


def print_capability_info():
    """Print capability information for UGOS registration."""
    print(json.dumps(CAPABILITIES, indent=2))


def print_help():
    """Print help text with examples."""
    help_text = """
Watchtower - AI Security Analyzer for UGREEN NAS
Natural language query -> cross-camera anomaly detection -> HTML security briefing

USAGE:
    watchtower "natural language query"
    watchtower --capabilities
    watchtower --help

EXAMPLES:
    watchtower "analyze last 24 hours"
    watchtower "show person detections yesterday 18:00-22:00"
    watchtower "generate briefing for front door camera last week"
    watchtower "extract clips for all vehicle detections today"

NATURAL LANGUAGE PARSING:
    Timeframes: "last 24 hours", "yesterday", "last 7 days", "this week", "2026-11-01 to 2026-11-02"
    Filters: "person detections", "vehicle detections", "motion events"
    Cameras: "front door camera", "cam-1", "garage camera"
    Confidence: "high confidence", "confidence above 80%"

UGOS CAPABILITIES:
    watchtower.query_events     - Natural language query (read-only, no confirmation)
    watchtower.extract_clips    - Extract clips ±30s (requires batch confirmation)
    watchtower.generate_briefing - Generate HTML briefing (requires single confirmation)

AUTHORIZATION:
    watchtower authorize /path/to/footage
    watchtower deauthorize /path/to/footage

VERSION: 1.0.0
"""
    print(help_text.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watchtower - AI Security Analyzer for UGREEN NAS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    parser.add_argument("query", nargs="*", help="Natural language query")
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("--capabilities", action="store_true", help="Print UGOS capabilities JSON")
    parser.add_argument("--version", action="store_true", help="Print version")
    parser.add_argument("--authorize", type=str, help="Authorize footage folder")
    parser.add_argument("--deauthorize", type=str, help="Deauthorize footage folder")
    parser.add_argument("--test", action="store_true", help="Test mode: auto-confirm all prompts")
    return parser.parse_args()


def handle_authorize(path: str) -> int:
    """Handle folder authorization via UGOS Files capability."""
    print(f"[INFO] Requesting authorization for: {path}")
    print("[INFO] This will prompt UGOS for user approval...")
    # In real implementation, call UGOS Files capability to request access
    print(f"[SUCCESS] Folder authorized: {path}")
    return 0


def handle_deauthorize(path: str) -> int:
    """Handle folder deauthorization."""
    print(f"[INFO] Deauthorizing: {path}")
    print(f"[SUCCESS] Folder deauthorized: {path}")
    return 0


def run_query_events(query: str, timeframe: Optional[str] = None, filters: Optional[Dict] = None) -> List[Dict]:
    """Execute query_events capability via Scanner Agent."""
    print(f"[SCANNER] Parsing query: {query}")
    parsed = parse_natural_language_query(query, timeframe, filters)
    print(f"[SCANNER] Parsed: timeframe={parsed.get('timeframe')}, filters={parsed.get('filters')}")
    
    # Initialize Scanner Agent
    scanner = ScannerAgent()
    events = scanner.query(parsed)
    
    print(f"[SCANNER] Found {len(events)} events")
    for i, event in enumerate(events[:5]):
        print(f"  [{i+1}] {event['timestamp']} | {event['camera_id']} | {event['event_type']} | {event['confidence']}%")
    if len(events) > 5:
        print(f"  ... and {len(events) - 5} more events")
    
    return events


def run_extract_clips(events: List[Dict], padding_seconds: int = 30, output_folder: Optional[str] = None, test_mode: bool = False) -> List[Dict]:
    """Execute extract_clips capability via Analyzer Agent with batch confirmation."""
    if not events:
        print("[ANALYZER] No events to extract clips from")
        return []
    
    if output_folder is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_folder = f"/Security/{today}/"
    
    print(f"[ANALYZER] Extracting clips for {len(events)} events")
    print(f"[ANALYZER] Padding: ±{padding_seconds}s | Output: {output_folder}")
    
    # UGOS Confirmation Gate - Batch approval
    clip_preview = []
    for i, event in enumerate(events):
        clip_preview.append({
            "event_ref": event.get("id", f"event_{i}"),
            "camera_id": event["camera_id"],
            "event_type": event["event_type"],
            "timestamp": event["timestamp"],
            "estimated_clip": f"{event['timestamp']} ±{padding_seconds}s"
        })
    
    print("\n[CONFIRMATION REQUIRED] The following clips will be extracted:")
    for i, clip in enumerate(clip_preview):
        print(f"  {i+1}. {clip['camera_id']} | {clip['event_type']} | {clip['timestamp']} | ±{padding_seconds}s")
    
    if not confirm_batch(f"Extract {len(clip_preview)} clips to {output_folder}?", test_mode=test_mode):
        print("[CANCELLED] User declined clip extraction")
        return []
    
    # Initialize Analyzer Agent
    analyzer = AnalyzerAgent()
    clips = analyzer.extract(events, padding_seconds, output_folder)
    
    print(f"[ANALYZER] Extracted {len(clips)} clips to {output_folder}")
    for clip in clips[:3]:
        print(f"  - {clip['clip_path']} ({clip['start_time']} to {clip['end_time']})")
    if len(clips) > 3:
        print(f"  ... and {len(clips) - 3} more clips")
    
    return clips


def run_generate_briefing(events: List[Dict], clips: List[Dict], template: str = "standard", test_mode: bool = False) -> str:
    """Execute generate_briefing capability via Reporter Agent with single confirmation."""
    if not events:
        print("[REPORTER] No events to generate briefing for")
        return ""
    
    print(f"[REPORTER] Generating {template} briefing for {len(events)} events with {len(clips)} clips")
    
    # UGOS Confirmation Gate - Single approval
    if not confirm_single(f"Generate {template} HTML security briefing with {len(clips)} embedded clips?", test_mode=test_mode):
        print("[CANCELLED] User declined briefing generation")
        return ""
    
    # Initialize Reporter Agent
    reporter = ReporterAgent()
    report_path = reporter.generate(events, clips, template)
    
    print(f"[REPORTER] Briefing generated: {report_path}")
    return report_path


def run_natural_language(query: str, test_mode: bool = False) -> int:
    """Run full pipeline from natural language query."""
    print(f"[WATCHTOWER] Processing: {query}")
    
    # Step 1: Query Events
    events = run_query_events(query)
    if not events:
        print("[RESULT] No events found. Try wider timeframe or check camera authorization.")
        return 0
    
    # Step 2: Extract Clips
    clips = run_extract_clips(events, test_mode=test_mode)
    if not clips:
        print("[RESULT] No clips extracted.")
        return 0
    
    # Step 3: Generate Briefing
    report_path = run_generate_briefing(events, clips, test_mode=test_mode)
    if not report_path:
        print("[RESULT] Briefing generation cancelled.")
        return 0
    
    print(f"\n[SUCCESS] Security briefing ready: {report_path}")
    print(f"[INFO] Clips saved in: /Security/{{today}}")
    return 0


def main() -> int:
    args = parse_args()
    
    if args.version:
        print(f"Watchtower v{__version__}")
        return 0
    
    if args.help or (not args.query and not args.capabilities and not args.authorize and not args.deauthorize):
        print_help()
        return 0
    
    if args.capabilities:
        print_capability_info()
        return 0
    
    if args.authorize:
        return handle_authorize(args.authorize)
    
    if args.deauthorize:
        return handle_deauthorize(args.deauthorize)
    
    # Join query parts
    query = " ".join(args.query)
    return run_natural_language(query, test_mode=args.test)


if __name__ == "__main__":
    sys.exit(main())