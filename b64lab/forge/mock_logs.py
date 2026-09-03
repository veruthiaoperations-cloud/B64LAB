"""
Mock Forensic Log Generator for Practice & Training.
Pure Python standard library implementation.
"""

import base64
import os
import random
import time
from typing import List, Tuple

class MockLogGenerator:
    """
    Generates realistic synthetic enterprise telemetry logs embedded with
    Base64 payloads for blue team triage exercises.
    """

    @classmethod
    def generate_web_access_log(cls, payload_b64: str, total_lines: int = 50) -> str:
        """Generates an Apache/Nginx web server access log with an embedded payload."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        ]
        endpoints = ["/index.html", "/login", "/about", "/static/css/main.css", "/api/v1/health", "/favicon.ico"]
        
        lines = []
        target_line_idx = random.randint(15, 35)

        for i in range(total_lines):
            ip = f"192.168.1.{random.randint(10, 250)}"
            timestamp = time.strftime("%d/%b/%Y:%H:%M:%S +0000", time.gmtime(time.time() - (total_lines - i) * 60))
            ua = random.choice(user_agents)

            if i == target_line_idx:
                # Malicious payload injection in query parameter
                lines.append(
                    f'{ip} - - [{timestamp}] "POST /upload.php?cmd={payload_b64} HTTP/1.1" 200 482 "-" "{ua}"'
                )
            else:
                ep = random.choice(endpoints)
                status = random.choice([200, 200, 200, 304, 404])
                size = random.randint(300, 4500)
                lines.append(
                    f'{ip} - - [{timestamp}] "GET {ep} HTTP/1.1" {status} {size} "-" "{ua}"'
                )

        return "\n".join(lines)

    @classmethod
    def generate_powershell_event_log(cls, encoded_command_b64: str) -> str:
        """Simulates a Windows Event Log 4104 (ScriptBlock Logging) snippet."""
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        log = (
            f"<Event xmlns='http://schemas.microsoft.com/win/2004/08/events/event'>\n"
            f"  <System>\n"
            f"    <Provider Name='Microsoft-Windows-PowerShell' Guid='{{A0C1853B-5C40-4B15-8766-3CF1C58F985A}}'/>\n"
            f"    <EventID>4104</EventID>\n"
            f"    <Version>1</Version>\n"
            f"    <Level>Information</Level>\n"
            f"    <TimeCreated SystemTime='{timestamp}'/>\n"
            f"    <Channel>Microsoft-Windows-PowerShell/Operational</Channel>\n"
            f"    <Computer>CORP-WORKSTATION-01.local</Computer>\n"
            f"  </System>\n"
            f"  <EventData>\n"
            f"    <Data Name='MessageNumber'>1</Data>\n"
            f"    <Data Name='MessageTotal'>1</Data>\n"
            f"    <Data Name='ScriptBlockText'>powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand {encoded_command_b64}</Data>\n"
            f"  </EventData>\n"
            f"</Event>"
        )
        return log
