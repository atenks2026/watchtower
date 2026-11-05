"""
Scanner Agent - UGOS Surveillance Capability
Queries camera events via natural language parsing.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random


class ScannerAgent:
    """
    Scanner Agent - Queries camera events via UGOS Surveillance capability.
    
    In Round 1 (no real NAS): Returns mock events for demo.
    In Round 2 (real NAS): Calls actual UGOS Surveillance capability.
    """
    
    def __init__(self):
        self.capability_name = "surveillance"
        self.mock_mode = True  # Set False for Round 2 with real NAS
    
    def query(self, parsed_query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query camera events based on parsed natural language.
        
        Args:
            parsed_query: Dict with keys:
                - timeframe: Dict with start/end datetime
                - filters: Dict with camera_id, event_type, min_confidence
                - original_query: str
        
        Returns:
            List of event dicts with keys:
                - id: str
                - timestamp: ISO format string
                - camera_id: str
                - event_type: str (person/vehicle/motion/package/unknown)
                - confidence: int (0-100)
                - metadata: Dict (bounding box, zone, etc.)
        """
        if self.mock_mode:
            return self._mock_query(parsed_query)
        else:
            return self._real_query(parsed_query)
    
    def _mock_query(self, parsed: Dict) -> List[Dict]:
        """Generate realistic mock events for demo/testing."""
        # Determine timeframe
        end_time = datetime.now()
        timeframe = parsed.get("timeframe", {})
        if isinstance(timeframe, dict) and "start" in timeframe:
            start_time = timeframe["start"]
        else:
            # Default: last 24 hours
            start_time = end_time - timedelta(hours=24)
        
        # Determine filters
        filters = parsed.get("filters", {})
        event_types = filters.get("event_type", ["person", "vehicle", "motion"])
        if isinstance(event_types, str):
            event_types = [event_types]
        min_confidence = filters.get("min_confidence", 50)
        camera_filter = filters.get("camera_id")
        
        # Mock cameras
        cameras = [
            {"id": "cam-front", "name": "Front Door", "location": "entry"},
            {"id": "cam-garage", "name": "Garage", "location": "driveway"},
            {"id": "cam-backyard", "name": "Backyard", "location": "rear"},
            {"id": "cam-side", "name": "Side Gate", "location": "side"},
        ]
        if camera_filter:
            cameras = [c for c in cameras if c["id"] == camera_filter]
        
        # Generate events
        events = []
        event_id = 0
        current = start_time
        
        # Event type weights (person > vehicle > motion)
        type_weights = {"person": 0.4, "vehicle": 0.3, "motion": 0.2, "package": 0.1}
        
        while current < end_time:
            # Random gap between events (5 min to 3 hours)
            gap_minutes = random.randint(5, 180)
            current += timedelta(minutes=gap_minutes)
            if current >= end_time:
                break
            
            # Pick camera
            camera = random.choice(cameras)
            
            # Pick event type
            event_type = random.choices(
                list(type_weights.keys()),
                weights=list(type_weights.values())
            )[0]
            
            # Confidence based on type
            if event_type == "person":
                confidence = random.randint(75, 98)
            elif event_type == "vehicle":
                confidence = random.randint(70, 95)
            elif event_type == "package":
                confidence = random.randint(80, 95)
            else:  # motion
                confidence = random.randint(40, 85)
            
            if confidence < min_confidence:
                continue
            
            # Build event
            event_id += 1
            event = {
                "id": f"evt_{event_id:04d}",
                "timestamp": current.isoformat(),
                "camera_id": camera["id"],
                "camera_name": camera["name"],
                "camera_location": camera["location"],
                "event_type": event_type,
                "confidence": confidence,
                "metadata": {
                    "zone": f"zone_{random.randint(1, 4)}",
                    "bbox": [random.randint(100, 500), random.randint(100, 400), 
                            random.randint(200, 600), random.randint(200, 500)],
                    "duration_seconds": random.randint(2, 30)
                }
            }
            events.append(event)
        
        return events
    
    def _real_query(self, parsed: Dict) -> List[Dict]:
        """
        Real UGOS Surveillance capability call.
        To be implemented for Round 2 with actual NAS.
        """
        # TODO: Implement actual UGOS Surveillance API call
        # Example structure:
        # from uliya_skill_kit import UGOS
        # ugos = UGOS()
        # events = ugos.surveillance.query_events(
        #     start_time=parsed["timeframe"]["start"],
        #     end_time=parsed["timeframe"]["end"],
        #     filters=parsed.get("filters", {})
        # )
        # return events
        
        # For now, fall back to mock
        print("[WARNING] Real UGOS Surveillance not available, using mock data")
        return self._mock_query(parsed)
    
    def get_supported_event_types(self) -> List[str]:
        """Return list of supported event types."""
        return ["person", "vehicle", "motion", "package", "unknown"]
    
    def get_supported_cameras(self) -> List[Dict]:
        """Return list of authorized cameras."""
        # In real implementation, query UGOS for authorized cameras
        return [
            {"id": "cam-front", "name": "Front Door", "location": "entry"},
            {"id": "cam-garage", "name": "Garage", "location": "driveway"},
            {"id": "cam-backyard", "name": "Backyard", "location": "rear"},
            {"id": "cam-side", "name": "Side Gate", "location": "side"},
        ]


# For testing
if __name__ == "__main__":
    scanner = ScannerAgent()
    
    # Test query
    test_parsed = {
        "timeframe": {"start": datetime.now() - timedelta(hours=24), "end": datetime.now()},
        "filters": {"event_type": ["person", "vehicle"], "min_confidence": 70}
    }
    
    events = scanner.query(test_parsed)
    print(f"Generated {len(events)} mock events:")
    for e in events[:5]:
        print(f"  {e['timestamp']} | {e['camera_id']} | {e['event_type']} | {e['confidence']}%")