"""
Analyzer Agent - UGOS Video + Files Capabilities
Extracts video clips around events and saves to /Security/ folder.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import os
import shutil
import uuid


class AnalyzerAgent:
    """
    Analyzer Agent - Extracts video clips around events via UGOS Video capability
    and saves them via UGOS Files capability.
    
    In Round 1 (no real NAS): Simulates clip extraction with mock files.
    In Round 2 (real NAS): Calls actual UGOS Video + Files capabilities.
    """
    
    def __init__(self):
        self.video_capability = "video"
        self.files_capability = "files"
        self.mock_mode = True  # Set False for Round 2 with real NAS
        self.default_padding = 30  # seconds
        self.default_output_base = "/Security"
    
    def extract(
        self,
        events: List[Dict[str, Any]],
        padding_seconds: int = 30,
        output_folder: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract video clips around events.
        
        Args:
            events: List of event dicts from Scanner Agent
            padding_seconds: Seconds before/after event timestamp
            output_folder: Destination folder (default: /Security/YYYY-MM-DD/)
        
        Returns:
            List of clip metadata dicts:
                - clip_path: str
                - event_ref: str
                - camera_id: str
                - start_time: ISO string
                - end_time: ISO string
                - duration: float (seconds)
                - file_size: int (bytes)
        """
        if not events:
            return []
        
        if output_folder is None:
            today = datetime.now().strftime("%Y-%m-%d")
            output_folder = f"{self.default_output_base}/{today}/"
        
        if self.mock_mode:
            return self._mock_extract(events, padding_seconds, output_folder)
        else:
            return self._real_extract(events, padding_seconds, output_folder)
    
    def _mock_extract(
        self,
        events: List[Dict],
        padding_seconds: int,
        output_folder: str
    ) -> List[Dict]:
        """Simulate clip extraction for demo/testing."""
        clips = []
        
        for event in events:
            event_id = event.get("id", f"evt_{uuid.uuid4().hex[:8]}")
            timestamp = event.get("timestamp", datetime.now().isoformat())
            camera_id = event.get("camera_id", "unknown")
            
            # Parse timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                dt = datetime.now()
            
            start_time = dt - timedelta(seconds=padding_seconds)
            end_time = dt + timedelta(seconds=padding_seconds)
            
            # Generate mock clip filename
            clip_filename = f"{event['id']}_{camera_id}_{dt.strftime('%H%M%S')}.mp4"
            clip_path = f"{output_folder.rstrip('/')}/{clip_filename}"
            
            # In mock mode, we don't actually create files
            # In real mode, this would call UGOS Video extract + Files write
            
            clip = {
                "clip_path": clip_path,
                "event_ref": event.get("id"),
                "camera_id": camera_id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration": padding_seconds * 2,
                "file_size": 1024 * 1024 * 5,  # Mock 5MB
                "event_type": event.get("event_type", "unknown"),
                "confidence": event.get("confidence", 0)
            }
            clips.append(clip)
        
        return clips
    
    def _real_extract(
        self,
        events: List[Dict],
        padding_seconds: int,
        output_folder: str
    ) -> List[Dict]:
        """
        Real UGOS Video + Files capability calls.
        To be implemented for Round 2 with actual NAS.
        """
        # TODO: Implement actual UGOS API calls
        # Example structure:
        # from uliya_skill_kit import UGOS
        # ugos = UGOS()
        # 
        # # Ensure output folder exists
        # ugos.files.mkdir(output_folder, parents=True, exist_ok=True)
        # 
        # clips = []
        # for event in events:
        #     clip = ugos.video.extract_clip(
        #         camera_id=event["camera_id"],
        #         start_time=event["timestamp"] - padding_seconds,
        #         end_time=event["timestamp"] + padding_seconds,
        #         output_path=f"{output_folder}/{event['id']}_{event['camera_id']}.mp4"
        #     )
        #     clips.append({...})
        # 
        # return clips
        
        print("[WARNING] Real UGOS Video/Files not available, using mock data")
        return self._mock_extract(events, padding_seconds, output_folder)
    
    def _fallback_extract(self, event: Dict, padding_seconds: int, output_folder: str) -> Dict:
        """
        Fallback when video extraction fails (codec issues, seek errors).
        Copies full source file with timestamp metadata in filename.
        """
        # In real implementation: copy source recording file
        # For mock: return special marker
        return {
            "clip_path": f"{output_folder}/{event['id']}_FULL_RECORDING.mp4",
            "event_ref": event.get("id"),
            "camera_id": event.get("camera_id"),
            "start_time": "FULL_RECORDING",
            "end_time": "FULL_RECORDING",
            "duration": 0,
            "file_size": 0,
            "fallback": True,
            "reason": "Video extraction failed - copied full recording"
        }
    
    def validate_output_folder(self, folder: str) -> bool:
        """Validate output folder path is safe and authorized."""
        # Prevent path traversal
        normalized = os.path.normpath(folder)
        if ".." in normalized or normalized.startswith("/") and not normalized.startswith(self.default_output_base):
            return False
        return True


# For testing
if __name__ == "__main__":
    analyzer = AnalyzerAgent()
    
    # Mock events from scanner
    test_events = [
        {
            "id": "evt_0001",
            "timestamp": "2026-11-02T14:32:15",
            "camera_id": "cam-front",
            "event_type": "person",
            "confidence": 94
        },
        {
            "id": "evt_0002",
            "timestamp": "2026-11-02T16:15:30",
            "camera_id": "cam-garage",
            "event_type": "vehicle",
            "confidence": 87
        }
    ]
    
    clips = analyzer.extract(test_events, padding_seconds=30)
    print(f"Mock extracted {len(clips)} clips:")
    for clip in clips:
        print(f"  {clip['clip_path']} | {clip['camera_id']} | {clip['duration']}s")