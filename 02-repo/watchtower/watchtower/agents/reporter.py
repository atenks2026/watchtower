"""
Reporter Agent - UGOS Knowledge + Files Capabilities
Generates HTML security briefing with embedded video clips using AI reasoning.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import uuid


class ReporterAgent:
    """
    Reporter Agent - Generates HTML security briefing via UGOS Knowledge (AI reasoning)
    and saves via UGOS Files capability.
    
    In Round 1 (no real NAS): Generates HTML with mock AI reasoning.
    In Round 2 (real NAS): Calls actual UGOS Knowledge (Nemotron) + Files capabilities.
    """
    
    def __init__(self):
        self.knowledge_capability = "knowledge"
        self.files_capability = "files"
        self.mock_mode = True  # Set False for Round 2 with real NAS
        self.model_name = "nvidia/nemotron-3-ultra-550b-a55b"  # Via NVIDIA NIM
        self.templates = {
            "standard": self._template_standard,
            "executive": self._template_executive,
            "detailed": self._template_detailed,
        }
    
    def generate(
        self,
        events: List[Dict[str, Any]],
        clips: List[Dict[str, Any]],
        template: str = "standard"
    ) -> str:
        """
        Generate HTML security briefing.
        
        Args:
            events: List of event dicts from Scanner Agent
            clips: List of clip metadata from Analyzer Agent
            template: "standard" | "executive" | "detailed"
        
        Returns:
            Path to generated HTML report
        """
        if not events:
            return self._generate_empty_report(template)
        
        template_func = self.templates.get(template, self._template_standard)
        
        if self.mock_mode:
            return self._mock_generate(events, clips, template, template_func)
        else:
            return self._real_generate(events, clips, template, template_func)
    
    def _mock_generate(
        self,
        events: List[Dict],
        clips: List[Dict],
        template: str,
        template_func
    ) -> str:
        """Generate HTML report with mock AI reasoning."""
        today = datetime.now().strftime("%Y%m%d_%H%M")
        report_filename = f"security_briefing_{today}.html"
        report_path = f"/Security/{today}/{report_filename}"
        
        # Count events by type
        event_counts = {}
        threat_levels = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
        cameras_involved = set()
        
        for event in events:
            event_type = event.get("event_type", "unknown")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            # Assign threat level based on type and confidence
            confidence = event.get("confidence", 0)
            if event.get("event_type") == "person" and confidence >= 90:
                threat_levels["Critical"] += 1
            elif event.get("event_type") == "person" and confidence >= 70:
                threat_levels["High"] += 1
            elif event.get("event_type") == "vehicle" and confidence >= 80:
                threat_levels["Medium"] += 1
            else:
                threat_levels["Low"] += 1
            
            cameras_involved.add(event.get("camera_id", "unknown"))
        
        # Generate HTML using template
        html = template_func(
            events=events,
            clips=clips,
            event_counts=event_counts,
            threat_levels=threat_levels,
            cameras_involved=cameras_involved,
            report_path=report_path,
            generated_at=datetime.now().isoformat()
        )
        
        # In mock mode, we don't actually write the file
        # In real mode, this would call UGOS Files write
        print(f"[MOCK] HTML report would be saved to: {report_path}")
        print(f"[MOCK] Report size: ~{len(html)} characters")
        
        return report_path
    
    def _real_generate(
        self,
        events: List[Dict],
        clips: List[Dict],
        template: str,
        template_func
    ) -> str:
        """
        Real UGOS Knowledge + Files capability calls.
        To be implemented for Round 2 with actual NAS.
        """
        # TODO: Implement actual UGOS API calls
        # Example structure:
        # from uliya_skill_kit import UGOS
        # ugos = UGOS()
        # 
        # # Prepare prompt for Nemotron
        # prompt = self._build_prompt(events, clips, template)
        # 
        # # Call Knowledge capability (Nemotron via NIM)
        # ai_response = ugos.knowledge.generate(
        #     model=self.model_name,
        #     prompt=prompt,
        #     max_tokens=4096,
        #     temperature=0.3
        # )
        # 
        # # Generate HTML from AI response
        # html = self._format_html(ai_response, events, clips, template)
        # 
        # # Save via Files capability
        # today = datetime.now().strftime("%Y%m%d_%H%M")
        # report_path = f"/Security/{today}/security_briefing_{today}.html"
        # ugos.files.write(report_path, html)
        # 
        # return report_path
        
        print("[WARNING] Real UGOS Knowledge/Files not available, using mock data")
        return self._mock_generate(events, clips, template, template_func)
    
    def _generate_empty_report(self, template: str) -> str:
        """Generate report for no events found."""
        today = datetime.now().strftime("%Y%m%d_%H%M")
        report_path = f"/Security/{today}/security_briefing_{today}.html"
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Briefing - All Quiet</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
        .quiet {{ text-align: center; padding: 3rem; color: #2ecc71; }}
        .icon {{ font-size: 4rem; margin-bottom: 1rem; }}
    </style>
</head>
<body>
    <div class="quiet">
        <div class="icon">🛡️</div>
        <h1>All Quiet</h1>
        <p>No security events detected in the specified timeframe.</p>
        <p><em>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</em></p>
    </div>
</body>
</html>"""
        
        print(f"[MOCK] Empty report would be saved to: {report_path}")
        return report_path
    
    # ===== TEMPLATES =====
    
    def _template_standard(
        self,
        events: List[Dict],
        clips: List[Dict],
        event_counts: Dict,
        threat_levels: Dict,
        cameras_involved: set,
        report_path: str,
        generated_at: str
    ) -> str:
        """Standard security briefing template."""
        
        # Build timeline HTML
        timeline_html = ""
        for event in events[:20]:  # Limit to 20 events
            dt = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
            time_str = dt.strftime("%H:%M:%S")
            threat_class = self._get_threat_class(event)
            clip_link = ""
            
            # Find matching clip
            for clip in clips:
                if clip.get("event_ref") == event.get("id"):
                    clip_link = f'<a href="{clip["clip_path"]}" target="_blank">▶ Play Clip</a>'
                    break
            
            timeline_html += f"""
            <div class="timeline-item {threat_class}">
                <div class="time">{time_str}</div>
                <div class="event">
                    <span class="camera">{event.get('camera_name', event['camera_id'])}</span>
                    <span class="type">{event['event_type'].title()}</span>
                    <span class="confidence">{event['confidence']}%</span>
                </div>
                <div class="actions">{clip_link}</div>
            </div>
            """
        
        # Build threat summary
        threat_html = ""
        for level, count in threat_levels.items():
            if count > 0:
                threat_html += f'<span class="threat-badge {level.lower()}">{level}: {count}</span>'
        
        # Camera summary
        camera_html = ""
        for cam_id in cameras_involved:
            cam_events = [e for e in events if e.get("camera_id") == cam_id]
            camera_html += f"""
            <div class="camera-summary">
                <h4>{cam_id}</h4>
                <p>{len(cam_events)} events</p>
            </div>
            """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Briefing - {datetime.now().strftime("%Y-%m-%d")}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 1rem;
            background: #f8f9fa;
            color: #212529;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #1a2a4a 0%, #2c3e6b 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .header h1 {{ margin: 0; font-size: 1.8rem; }}
        .header .meta {{ opacity: 0.9; font-size: 0.9rem; margin-top: 0.5rem; }}
        .threat-summary {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin: 1.5rem 0;
        }}
        .threat-badge {{
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        .critical {{ background: #ffebee; color: #c62828; }}
        .high {{ background: #fff3e0; color: #ef6c00; }}
        .medium {{ background: #e8f5e9; color: #2e7d32; }}
        .low {{ background: #e3f2fd; color: #1565c0; }}
        .info {{ background: #f5f5f5; color: #616161; }}
        .timeline {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        .timeline-item {{
            display: grid;
            grid-template-columns: 100px 1fr auto;
            gap: 1rem;
            padding: 1rem;
            border-bottom: 1px solid #eee;
            align-items: center;
        }}
        .timeline-item:last-child {{ border-bottom: none; }}
        .timeline-item.critical {{ border-left: 4px solid #c62828; background: #fff8f8; }}
        .timeline-item.high {{ border-left: 4px solid #ef6c00; background: #fff8f0; }}
        .timeline-item.medium {{ border-left: 4px solid #2e7d32; background: #f0fdf4; }}
        .timeline-item.low {{ border-left: 4px solid #1565c0; background: #f0f7ff; }}
        .time {{ font-weight: 600; color: #666; font-family: monospace; }}
        .event {{ display: flex; gap: 1rem; align-items: center; }}
        .camera {{ background: #e3f2fd; color: #1565c0; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; }}
        .type {{ text-transform: capitalize; font-weight: 500; }}
        .confidence {{ color: #666; font-size: 0.85rem; }}
        .actions a {{
            background: #1a2a4a;
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.85rem;
            transition: background 0.2s;
        }}
        .actions a:hover {{ background: #2c3e6b; }}
        .camera-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        .camera-summary {{
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        .camera-summary h4 {{ margin: 0 0 0.5rem; color: #1a2a4a; }}
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.85rem;
            border-top: 1px solid #eee;
            margin-top: 2rem;
        }}
        video {{
            max-width: 100%;
            border-radius: 8px;
            margin: 0.5rem 0;
        }}
        @media (max-width: 600px) {{
            .timeline-item {{ grid-template-columns: 80px 1fr; }}
            .actions {{ grid-column: span 2; margin-top: 0.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Security Briefing</h1>
        <div class="meta">
            Generated: {datetime.fromisoformat(generated_at).strftime("%Y-%m-%d %H:%M")} | 
            Events: {len(events)} | 
            Clips: {len(clips)} | 
            Cameras: {len(cameras_involved)}
        </div>
    </div>
    
    <div class="threat-summary">
        {threat_html}
    </div>
    
    <div class="timeline">
        {timeline_html}
    </div>
    
    <div class="camera-grid">
        {camera_html}
    </div>
    
    <div class="footer">
        <p>Watchtower AI Security Analyzer | Built on UGREEN UGOS</p>
        <p>Local processing • No cloud • Your data stays yours</p>
    </div>
</body>
</html>"""
    
    def _template_executive(self, events, clips, event_counts, threat_levels, cameras_involved, report_path, generated_at):
        """Executive summary template - condensed version."""
        return self._template_standard(events, clips, event_counts, threat_levels, cameras_involved, report_path, generated_at)
    
    def _template_detailed(self, events, clips, event_counts, threat_levels, cameras_involved, report_path, generated_at):
        """Detailed template - same as standard for now."""
        return self._template_standard(events, clips, event_counts, threat_levels, cameras_involved, report_path, generated_at)
    
    def _get_threat_class(self, event: Dict) -> str:
        """Determine CSS threat class for timeline item."""
        event_type = event.get("event_type", "unknown")
        confidence = event.get("confidence", 0)
        
        if event_type == "person" and confidence >= 90:
            return "critical"
        elif event_type == "person" and confidence >= 70:
            return "high"
        elif event_type == "vehicle" and confidence >= 80:
            return "medium"
        return "low"
    
    def _build_prompt(self, events: List[Dict], clips: List[Dict], template: str) -> str:
        """Build prompt for Nemotron AI reasoning."""
        prompt = f"""You are a security analyst. Generate a professional security briefing.

Events ({len(events)}):
{json.dumps(events[:10], indent=2)}

Clips available: {len(clips)}
Template: {template}

Generate a concise security briefing with:
1. Executive summary (2-3 sentences)
2. Key anomalies detected
3. Per-camera summary
4. Recommendations for user

Format as structured text for HTML conversion."""
        return prompt


# For testing
if __name__ == "__main__":
    reporter = ReporterAgent()
    
    test_events = [
        {"id": "evt_0001", "timestamp": "2026-11-02T14:32:15", "camera_id": "cam-front", "camera_name": "Front Door", "event_type": "person", "confidence": 94},
        {"id": "evt_0002", "timestamp": "2026-11-02T16:15:30", "camera_id": "cam-garage", "camera_name": "Garage", "event_type": "vehicle", "confidence": 87},
    ]
    
    test_clips = [
        {"clip_path": "/Security/2026-11-02/evt_0001_cam-front_143215.mp4", "event_ref": "evt_0001"},
        {"clip_path": "/Security/2026-11-02/evt_0002_cam-garage_161530.mp4", "event_ref": "evt_0002"},
    ]
    
    path = reporter.generate(test_events, test_clips, "standard")
    print(f"Report path: {path}")