#!/usr/bin/env python3
"""
B64Lab - The Zero-Dependency Cybersecurity Base64 Academy, Simulator & Triage Engine.
v1.0.0 (SEC-STD-EDITION)
Pure Python Standard Library. Zero NPM. Zero External Dependencies.
"""

import sys
import os

# Ensure the parent directory is in sys.path so b64lab package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from b64lab.cli import main

if __name__ == "__main__":
    main()
