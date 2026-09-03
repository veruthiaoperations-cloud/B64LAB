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
            print("  [7] Data URI: Encode Image or File to data:<mime>;base64 (RFC 2397)")
            print("  [8] Data URI: Decode & Check for MIME Spoofing / HTML Smuggling")
            print("  [0] Return to Main Menu\n")

            choice = UIComponents.prompt("Select workbench tool (0-8)")
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
                    raw, _ = BitwiseEngine.normalize_padding(raw)
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
            elif choice == "7":
                fpath = input("\n  Enter path to file or image: ").strip().strip('"')
                import os
                if not os.path.exists(fpath):
                    print(f"  [!] File not found: {fpath}")
                else:
                    ext = os.path.splitext(fpath)[1].lower().lstrip(".")
                    mime_map = {
                        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                        "gif": "image/gif", "svg": "image/svg+xml", "pdf": "application/pdf",
                        "ico": "image/x-icon", "webp": "image/webp"
                    }
                    mime = mime_map.get(ext, "application/octet-stream")
                    with open(fpath, "rb") as f:
                        data = f.read()
                    enc_b64 = base64.b64encode(data).decode("ascii")
                    data_uri = f"data:{mime};base64,{enc_b64}"
                    print(f"\n  [+] Encoded {len(data)} bytes into RFC 2397 Data URI:")
                    print(f"      {data_uri[:100]}... (Total {len(data_uri)} chars)")
                    save_choice = UIComponents.prompt("Export full Data URI string to text file? [Y/N]")
                    if save_choice.upper() == "Y":
                        out_txt = fpath + ".datauri.txt"
                        with open(out_txt, "w") as out_f:
                            out_f.write(data_uri)
                        print(f"  [+] Saved Data URI to: {out_txt}")
                UIComponents.pause()
            elif choice == "8":
                raw_uri = input("\n  Paste Data URI (data:<mime>;base64,<data>): ").strip()
                import re
                m = re.match(r"data:(?P<mime>[\w/+-]+);base64,(?P<data>[A-Za-z0-9+/=]+)", raw_uri)
                if not m:
                    print("  [!] Invalid Data URI format. Expected 'data:<mime>;base64,<payload>'")
                else:
                    claimed_mime = m.group("mime")
                    b64_data, _ = BitwiseEngine.normalize_padding(m.group("data"))
                    try:
                        decoded = base64.b64decode(b64_data, validate=False)
                        sig = SignatureDB.identify(decoded)
                        print(f"\n  [+] Claimed MIME Type: {claimed_mime}")
                        print(f"  [+] Decoded Payload  : {len(decoded)} bytes")
                        if sig:
                            print(f"  [+] Detected Signature: {sig.description} (MIME: {sig.mime_type})")
                            if "image" in claimed_mime and sig.category in ["EXECUTABLE", "ARCHIVE"]:
                                print(f"  {ANSI.BRIGHT_RED}{ANSI.BOLD}[!] ALERT: CRITICAL MIME MISMATCH! (HTML Smuggling Indicator T1027.006){ANSI.RESET}")
                                print(f"      Claimed to be an image but contains a {sig.category} binary!")
                        else:
                            print(f"  [!] No recognized file signature.")
                        print("\n  Canonical Hex Dump:")
                        print(HexViewer.render(decoded, max_bytes=96))
                    except Exception as e:
                        print(f"  [!] Failed to decode: {e}")
                UIComponents.pause()
