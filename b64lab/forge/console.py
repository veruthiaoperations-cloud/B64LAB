"""
Offensive Forge Console & Adversary Simulation Workbench.
Dynamic Crimson Red Theme.
Pure Python standard library implementation.
"""

import os
from typing import Optional

from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI
from ..core.alphabets import Alphabets, CustomAlphabet
from .powershell import PowerShellForge
from .dropper import DropperForge
from .evasion import EvasionForge
from .mock_logs import MockLogGenerator

class ForgeConsole:
    """
    Red Team / Offensive Simulation Console.
    Operates in the Tactical Crimson Red aesthetic.
    """

    @classmethod
    def run(cls) -> None:
        """Main Offensive Forge loop."""
        Theme.set_lane("OFFENSIVE")
        try:
            while True:
                UIComponents.header(
                    "OFFENSIVE SIMULATION & PAYLOAD FORGE LAB",
                    "Synthesize realistic attack artifacts, test evasion, and generate telemetry"
                )

                print("  [1] Forge PowerShell -EncodedCommand (UTF-16LE Architecture)")
                print("  [2] Build Multi-Stage Dropper (Base64 -> Gzip / Zlib Stager)")
                print("  [3] Custom Alphabet Cipher Forge (Defeating Static Signatures)")
                print("  [4] Evasion Sandbox (Strip Padding, Inject Whitespace)")
                print("  [5] Generate Synthetic Forensic Logs (Inject Payloads into Web/Event Logs)")
                print("  [0] Return to Main Menu\n")

                choice = UIComponents.prompt("Select offensive operation (0-5)")
                if choice == "0":
                    break
                elif choice == "1":
                    cls._forge_powershell()
                elif choice == "2":
                    cls._forge_dropper()
                elif choice == "3":
                    cls._forge_custom_alphabet()
                elif choice == "4":
                    cls._forge_evasion()
                elif choice == "5":
                    cls._forge_logs()
        finally:
            Theme.set_lane("NEUTRAL")

    @classmethod
    def _forge_powershell(cls) -> None:
        """Interactive PowerShell payload generator."""
        UIComponents.header("POWERSHELL -ENCODEDCOMMAND FORGE (UTF-16LE)")
        print("  Choose a sample safe command or enter your own:")
        for idx, cmd in enumerate(PowerShellForge.SAFE_COMMANDS, start=1):
            print(f"  [{idx}] {cmd}")
        print("  [C] Custom Command Input")

        sel = UIComponents.prompt("Select option (1-5 or C)")
        if sel.upper() == "C":
            script = input("\n  Enter command: ").strip()
        else:
            try:
                idx = int(sel)
                script = PowerShellForge.SAFE_COMMANDS[idx - 1]
            except Exception:
                script = "whoami"

        res = PowerShellForge.craft(script)
        palette = Theme.get_palette()
        p = palette.primary
        s = palette.secondary
        r = ANSI.RESET

        lines = [
            f"TARGET COMMAND   : {res['command']}",
            "",
            "VALID PAYLOAD (UTF-16LE):",
            f"  Bytes (Hex)    : {res['utf16_bytes_hex']}",
            f"  Base64 Output  : {res['b64_valid_utf16le']}",
            "",
            "BROKEN PAYLOAD (UTF-8) - FOR CONTRAST:",
            f"  Bytes (Hex)    : {res['utf8_bytes_hex']}",
            f"  Base64 Output  : {res['b64_broken_utf8']} (Will fail in powershell.exe -e!)",
            "",
            "EXECUTION CLI SYNTAX:",
            f"  {res['execution_syntax']}"
        ]
        UIComponents.box(lines, title="POWERSHELL FORGE SPEC", style="double")
        UIComponents.pause()

    @classmethod
    def _forge_dropper(cls) -> None:
        """Interactive multi-stage dropper builder."""
        UIComponents.header("MULTI-STAGE COMPRESSED DROPPER FORGE")
        sample_payload = input("\n  Enter payload text/script (or press Enter for default): ").strip()
        if not sample_payload:
            sample_payload = "Write-Host 'Stage 2 In-Memory Payload Active!' -ForegroundColor Cyan"

        res = DropperForge.build_gzip_dropper(sample_payload)
        lines = [
            f"ORIGINAL PAYLOAD SIZE   : {res['original_size']} bytes",
            f"COMPRESSED SIZE (GZIP)  : {res['compressed_size']} bytes",
            f"FINAL BASE64 STAGER     : {res['b64_payload']}",
            "",
            "IN-MEMORY POWERSHELL DECOMPRESSION STUB:",
            f"  {res['powershell_stub']}",
        ]
        UIComponents.box(lines, title="DROPPER DEPLOYMENT STACK", style="rounded")
        UIComponents.pause()

    @classmethod
    def _forge_custom_alphabet(cls) -> None:
        """Interactive custom alphabet substitution cipher."""
        UIComponents.header("CUSTOM ALPHABET ADVERSARY EMULATION")
        text = input("\n  Enter payload text to encode: ").strip()
        if not text:
            text = "cmd.exe /c echo Infiltrated!"

        print("\n  Select alphabet strategy:")
        print("  [1] Reversed Alphabet (Simple Anti-AV)")
        print("  [2] Shuffled Pseudo-Random Permutation (APT Simulation)")
        print("  [3] Alphanumeric-First Table")

        opt = UIComponents.prompt("Select strategy (1-3)")
        if opt == "1":
            alpha = Alphabets.REVERSED
        elif opt == "2":
            alpha = CustomAlphabet.generate_shuffled(seed=1337)
        else:
            alpha = Alphabets.ALPHANUM_FIRST

        res = EvasionForge.apply_custom_alphabet(text, alpha)
        lines = [
            f"INPUT PLAINTEXT : {text}",
            f"STANDARD BASE64 : {res['standard_b64']}",
            f"CUSTOM BASE64   : {res['custom_b64']}",
            "",
            f"CUSTOM ALPHABET (64 chars):",
            f"  {res['alphabet_used']}",
            "",
            "OBSERVATION:",
            "  Notice how the character set completely transforms.",
            "  Standard static detection signatures looking for 'cmd.exe' or 'powershell' will fail!"
        ]
        UIComponents.box(lines, title="CUSTOM ALPHABET RESULT", style="double")
        UIComponents.pause()

    @classmethod
    def _forge_evasion(cls) -> None:
        """Interactive padding & whitespace evasion sandbox."""
        UIComponents.header("PADDING STRIPPING & WHITESPACE EVASION SANDBOX")
        text = input("\n  Enter text to encode: ").strip()
        if not text:
            text = "SELECT * FROM users WHERE admin = 1"

        import base64
        std_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
        unpadded = EvasionForge.strip_padding(std_b64)
        spaced = EvasionForge.inject_whitespace(std_b64)

        lines = [
            f"STANDARD PADDED BASE64 : {std_b64}",
            f"UNPADDED VARIANT       : {unpadded}",
            f"WHITESPACE FRAGMENTED  : {spaced}",
            "",
            "DEFENSIVE EVALUATION:",
            "  - Unpadded strings evade signatures demanding strict '= / ==' terminations.",
            "  - Whitespace-injected strings evade length-based fixed window detectors."
        ]
        UIComponents.box(lines, title="EVASION ARTIFACTS", style="rounded")
        UIComponents.pause()

    @classmethod
    def _forge_logs(cls) -> None:
        """Generates realistic synthetic log files containing embedded payloads."""
        UIComponents.header("SYNTHETIC TELEMETRY & LOG GENERATOR")
        print("  [1] Generate Apache Web Server Access Log (with embedded SQLi/webshell)")
        print("  [2] Generate Windows Event Log 4104 (ScriptBlock Logging)")

        choice = UIComponents.prompt("Select log type (1-2)")
        out_dir = os.path.join(os.getcwd(), "samples")
        os.makedirs(out_dir, exist_ok=True)

        if choice == "1":
            import base64
            payload = base64.b64encode(b"<?php system($_GET['cmd']); ?>").decode("ascii")
            log_content = MockLogGenerator.generate_web_access_log(payload, total_lines=40)
            file_path = os.path.join(out_dir, "synthetic_access.log")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(log_content)
            print(f"\n  [+] Generated synthetic web access log with embedded webshell!")
            print(f"  [+] Saved to: {file_path}")
            print(f"  [!] Switch to the DEFENSIVE TRIAGE LANE to carve and hunt this log!")
        else:
            ps_craft = PowerShellForge.craft("Get-Process; whoami; net user")
            log_content = MockLogGenerator.generate_powershell_event_log(ps_craft["b64_valid_utf16le"])
            file_path = os.path.join(out_dir, "synthetic_powershell_event.xml")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(log_content)
            print(f"\n  [+] Generated synthetic Windows Event Log with encoded PowerShell!")
            print(f"  [+] Saved to: {file_path}")
            print(f"  [!] Switch to the DEFENSIVE TRIAGE LANE to carve and hunt this log!")

        UIComponents.pause()
