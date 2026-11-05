"""
Tests for Watchtower Skill
"""

import pytest
from watchtower.utils.nlp import parse_natural_language_query, parse_timeframe_string
from watchtower.ugos.confirmation import confirm_single, confirm_batch, UGOSConfirmation
from watchtower.agents.scanner import ScannerAgent
from watchtower.agents.analyzer import AnalyzerAgent
from watchtower.agents.reporter import ReporterAgent


class TestNLPParser:
    """Test natural language query parsing."""
    
    def test_basic_timeframe(self):
        result = parse_natural_language_query("analyze last 24 hours")
        assert "timeframe" in result
        assert "start" in result["timeframe"]
        assert "end" in result["timeframe"]
    
    def test_event_type_filter(self):
        result = parse_natural_language_query("show person detections yesterday")
        assert "filters" in result
        assert "event_type" in result["filters"]
        assert "person" in result["filters"]["event_type"]
    
    def test_camera_filter(self):
        result = parse_natural_language_query("front door camera last week")
        assert "filters" in result
        assert "camera_id" in result["filters"]
        assert result["filters"]["camera_id"] == "cam-front"
    
    def test_confidence_filter(self):
        result = parse_natural_language_query("high confidence person detections")
        assert "filters" in result
        assert "min_confidence" in result["filters"]
        assert result["filters"]["min_confidence"] >= 80
    
    def test_timeframe_parsing(self):
        assert parse_timeframe_string("24h") == 24 * 3600
        assert parse_timeframe_string("7d") == 7 * 24 * 3600
        assert parse_timeframe_string("2w") == 2 * 7 * 24 * 3600


class TestConfirmation:
    """Test UGOS confirmation gates."""
    
    def test_confirm_single_yes(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        assert confirm_single("Test?") is True
    
    def test_confirm_single_no(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        assert confirm_single("Test?") is False
    
    def test_confirm_batch_yes(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        items = [{"desc": "item1"}, {"desc": "item2"}]
        assert confirm_batch("Test batch?", items) is True


class TestScannerAgent:
    """Test Scanner Agent."""
    
    def test_mock_query_returns_events(self):
        scanner = ScannerAgent()
        parsed = {"timeframe": {"start": "2026-11-01T00:00:00", "end": "2026-11-02T00:00:00"}, "filters": {}}
        events = scanner.query(parsed)
        assert isinstance(events, list)
        assert len(events) > 0
        for event in events:
            assert "id" in event
            assert "timestamp" in event
            assert "camera_id" in event
            assert "event_type" in event
            assert "confidence" in event
    
    def test_event_types(self):
        scanner = ScannerAgent()
        types = scanner.get_supported_event_types()
        assert "person" in types
        assert "vehicle" in types
        assert "motion" in types


class TestAnalyzerAgent:
    """Test Analyzer Agent."""
    
    def test_mock_extract(self):
        analyzer = AnalyzerAgent()
        events = [
            {"id": "evt_0001", "timestamp": "2026-11-02T14:32:15", "camera_id": "cam-front", "event_type": "person", "confidence": 94}
        ]
        clips = analyzer.extract(events, padding_seconds=30)
        assert isinstance(clips, list)
        assert len(clips) == 1
        clip = clips[0]
        assert "clip_path" in clip
        assert "event_ref" in clip
        assert "camera_id" in clip
    
    def test_fallback_extract(self):
        analyzer = AnalyzerAgent()
        event = {"id": "evt_0001", "camera_id": "cam-front", "event_type": "person"}
        fallback = analyzer._fallback_extract(event, 30, "/Security/2026-11-02/")
        assert fallback["fallback"] is True
        assert "FULL_RECORDING" in fallback["clip_path"]


class TestReporterAgent:
    """Test Reporter Agent."""
    
    def test_mock_generate(self):
        reporter = ReporterAgent()
        events = [
            {"id": "evt_0001", "timestamp": "2026-11-02T14:32:15", "camera_id": "cam-front", "camera_name": "Front Door", "event_type": "person", "confidence": 94}
        ]
        clips = [
            {"clip_path": "/Security/2026-11-02/evt_0001_cam-front_143215.mp4", "event_ref": "evt_0001"}
        ]
        path = reporter.generate(events, clips, "standard")
        assert path.startswith("/Security/")
        assert path.endswith(".html")
    
    def test_empty_report(self):
        reporter = ReporterAgent()
        path = reporter.generate([], [], "standard")
        assert path.startswith("/Security/")
        assert "All Quiet" in reporter._generate_empty_report("standard")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])