"""
PowerShell UTF-16LE -EncodedCommand Forge.
Pure Python standard library implementation.
"""

import base64
from typing import Dict, Tuple

class PowerShellForge:
    """
    Generates authentic, syntactically valid PowerShell -EncodedCommand payloads.
    Contrasts UTF-16LE against UTF-8 to educate students on the Windows architecture quirk.
    """

    SAFE_COMMANDS = [
        "whoami",
        "Get-Process | Select-Object -First 5",
        "Get-Date",
        "Write-Host '[B64Lab] Simulation Test Payload Executed Successfully!' -ForegroundColor Green",
        "Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version",
    ]

    @classmethod
    def craft(cls, script_text: str) -> Dict[str, str]:
        """
        Crafts both the functional UTF-16LE payload and the broken UTF-8 payload
        for side-by-side comparison and testing.
        """
        # 1. Functional: UTF-16LE
        utf16_bytes = script_text.encode("utf-16le")
        b64_valid = base64.b64encode(utf16_bytes).decode("ascii")

        # 2. Broken: UTF-8 (Common junior mistake)
        utf8_bytes = script_text.encode("utf-8")
        b64_broken = base64.b64encode(utf8_bytes).decode("ascii")

        # Hex representations
        utf16_hex = " ".join(f"{b:02X}" for b in utf16_bytes[:16]) + ("..." if len(utf16_bytes) > 16 else "")
        utf8_hex = " ".join(f"{b:02X}" for b in utf8_bytes[:16]) + ("..." if len(utf8_bytes) > 16 else "")

        return {
            "command": script_text,
            "b64_valid_utf16le": b64_valid,
            "b64_broken_utf8": b64_broken,
            "utf16_bytes_hex": utf16_hex,
            "utf8_bytes_hex": utf8_hex,
            "execution_syntax": f"powershell.exe -NoProfile -NonInteractive -EncodedCommand {b64_valid}",
        }
