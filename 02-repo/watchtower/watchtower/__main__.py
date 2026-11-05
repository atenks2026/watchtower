#!/usr/bin/env python3
"""
Watchtower - AI Security Analyzer for UGREEN NAS
Main entry point for CLI
"""

import sys
from watchtower.cli import main

if __name__ == "__main__":
    sys.exit(main())