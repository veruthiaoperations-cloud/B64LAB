"""
Interactive Multi-Format Cryptographic & Encoding Workbench.
Pure Python standard library implementation.
"""

import base64
from typing import Optional

from .ui.components import UIComponents
from .ui.themes import Theme
from .ui.ansi import ANSI
from .ui.hexdump import HexViewer
from .core.bitwise import BitwiseEngine
from .core.entropy import ShannonEntropy
from .core.signatures import SignatureDB

class Workbench:
    """Fast, interactive encoder/decoder and forensic inspector."""

    @classmethod
    def run(cls) -> None:
        while True:
            UIComponents.header(
                "QUICK WORKBENCH: MULTI-FORMAT ENCODER / DECODER",
                "Direct transformation, entropy inspection, and canonical hex dumps"
            )

            print("  [1] Encode: Text to Standard Base64")
            print("  [2] Encode: Text to URL-Safe Base64")
            print("  [3] Encode: Text to Base32")
            print("  [4] Decode: Standard / URL-Safe Base64 to Text & Hex")
            print("  [5] Decode: Base32 to Text")
            print("  [6] Inspect Entropy of String")
            print("  [0] Return to Main Menu\n")

            choice = UIComponents.prompt("Select workbench tool (0-6)")
            if choice == "0":
                break
            elif choice == "1":
                txt = input("\n  Enter text to encode: ")
                enc = base64.b64encode(txt.encode("utf-8")).decode("ascii")
                print(f"\n  [+] Base64 Encoded: {ANSI.BOLD}{enc}{ANSI.RESET}\n")
                UIComponents.pause()
            elif choice == "2":
                txt = input("\n  Enter text to encode: ")
                enc = base64.urlsafe_b64encode(txt.encode("utf-8")).decode("ascii")
                print(f"\n  [+] Base64URL Encoded: {ANSI.BOLD}{enc}{ANSI.RESET}\n")
                UIComponents.pause()
            elif choice == "3":
                txt = input("\n  Enter text to encode: ")
                enc = base64.b32encode(txt.encode("utf-8")).decode("ascii")
                print(f"\n  [+] Base32 Encoded: {ANSI.BOLD}{enc}{ANSI.RESET}\n")
                UIComponents.pause()
            elif choice == "4":
                raw = input("\n  Enter Base64 to decode: ").strip()
                try:
                    # Auto repair padding
                    rem = len(raw) % 4
                    if rem == 2:
                        raw += "=="
                    elif rem == 3:
                        raw += "="
                    decoded = base64.b64decode(raw, validate=False)
                    print(f"\n  [+] Decoded ({len(decoded)} bytes):")
                    
                    is_txt, txt_val = SignatureDB.is_text(decoded)
                    if is_txt and txt_val:
                        print(f"  Plaintext: {txt_val}\n")
                    
                    is_ps, ps_val = SignatureDB.is_powershell_utf16le(decoded)
                    if is_ps and ps_val:
                        print(f"  PowerShell UTF-16LE: {ps_val}\n")

                    print("  Canonical Hex Dump:")
                    print(HexViewer.render(decoded, max_bytes=128))
                except Exception as e:
                    print(f"\n  [!] Decoding failed: {e}")
                UIComponents.pause()
            elif choice == "5":
                raw = input("\n  Enter Base32 to decode: ").strip()
                try:
                    decoded = base64.b32decode(raw)
                    print(f"\n  [+] Decoded: {decoded.decode('utf-8', errors='ignore')}\n")
                except Exception as e:
                    print(f"\n  [!] Base32 decode failed: {e}")
                UIComponents.pause()
            elif choice == "6":
                txt = input("\n  Enter string for entropy calculation: ")
                report = ShannonEntropy.analyze(txt)
                bar = ShannonEntropy.render_bar(report.entropy)
                print(f"\n  Entropy: {bar}")
                print(f"  Class  : {report.classification} (Threat: {report.threat_level})")
                print(f"  Note   : {report.description}\n")
                UIComponents.pause()
