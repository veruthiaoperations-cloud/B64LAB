"""
Defensive Triage Workbench & Forensic Analysis Console.
Dynamic Ice Blue / Cyan Theme.
Pure Python standard library implementation.
"""

import os
import sys
from typing import List, Optional

from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI
from ..ui.hexdump import HexViewer
from ..core.entropy import ShannonEntropy
from ..core.unpacker import RecursiveUnpacker
from .carver import ArtifactCarver, CarvedArtifact

class TriageAnalyzer:
    """
    Blue Team Forensic Triage Console.
    Operates in the Defensive Ice Blue aesthetic.
    """

    @classmethod
    def run(cls) -> None:
        """Main Defensive Triage loop."""
        Theme.set_lane("DEFENSIVE")
        try:
            while True:
                UIComponents.header(
                    "DEFENSIVE TRIAGE & FORENSIC CARVING LAB",
                    "Analyze encoded payloads, calculate Shannon entropy, and carve embedded binaries"
                )

                print("  [1] Triage Single Base64 String / Paste")
                print("  [2] Carve & Inspect Log File or Script (Scan for Embedded Payloads)")
                print("  [3] Multi-Stage Recursive De-obfuscator (Base64 -> Gzip -> Payload)")
                print("  [4] Inspect Sample Defense Artifact (Pre-packaged SOC Exercise)")
                print("  [0] Return to Main Menu\n")

                choice = UIComponents.prompt("Select defensive operation (0-4)")
                if choice == "0":
                    break
                elif choice == "1":
                    cls._triage_single_string()
                elif choice == "2":
                    cls._carve_file_interactive()
                elif choice == "3":
                    cls._run_recursive_unpacker()
                elif choice == "4":
                    cls._inspect_sample_artifact()
        finally:
            Theme.set_lane("NEUTRAL")

    @classmethod
    def _triage_single_string(cls) -> None:
        """Analyzes a single user-provided Base64 string."""
        UIComponents.header("INTERACTIVE STRING FORENSIC TRIAGE")
        raw_input_str = input("\n  Paste Base64 encoded payload: ").strip()
        if not raw_input_str:
            print("  [!] Input cannot be empty.")
            UIComponents.pause()
            return

        artifacts = ArtifactCarver.carve_string(raw_input_str, min_length=4)
        if not artifacts:
            print("  [!] Unable to decode valid Base64 data from provided input.")
            UIComponents.pause()
            return

        cls._display_artifact_details(artifacts[0])

    @classmethod
    def _display_artifact_details(cls, art: CarvedArtifact) -> None:
        """Displays full forensic profile of a carved payload."""
        palette = Theme.get_palette()
        p = palette.primary
        s = palette.secondary
        r = ANSI.RESET

        UIComponents.header(f"FORENSIC REPORT: ARTIFACT #{art.artifact_id}")

        entropy_bar = ShannonEntropy.render_bar(art.entropy)
        sig_desc = art.signature.description if art.signature else "NO RECOGNIZED MAGIC BYTES"

        lines = [
            f"THREAT ASSESSMENT : {art.threat_assessment}",
            f"RAW STRING LENGTH : {len(art.raw_b64)} characters (Padded: {art.padded})",
            f"DECODED SIZE      : {len(art.decoded_bytes)} bytes",
            f"SHANNON ENTROPY   : {entropy_bar} [{art.entropy_class}]",
            f"FILE SIGNATURE    : {sig_desc}",
            f"MD5 HASH          : {art.md5}",
            f"SHA-256 HASH      : {art.sha256}",
        ]

        if art.is_powershell:
            lines.append("")
            lines.append("POWERSHELL SCRIPT DETECTED (UTF-16LE):")
            lines.append(f"  {art.powershell_code[:300]}")
        elif art.text_preview:
            lines.append("")
            lines.append("PLAINTEXT PREVIEW:")
            lines.append(f"  {art.text_preview[:200]}")

        UIComponents.box(lines, title="INCIDENT TRIAGE CARD", style="double")

        # Hex Dump
        print(f"\n  {s}{ANSI.BOLD}─── CANONICAL FORENSIC HEX DUMP ───{r}")
        print(HexViewer.render(art.decoded_bytes, max_bytes=128, color=True))
        print()

        # Export Option
        export_choice = UIComponents.prompt("Export carved payload to disk? [Y/N]")
        if export_choice.upper() == "Y":
            cls._export_payload(art)

        UIComponents.pause()

    @classmethod
    def _export_payload(cls, art: CarvedArtifact) -> None:
        """Safely saves carved payload to disk with an IOC report."""
        out_dir = os.path.join(os.getcwd(), "carved_artifacts")
        os.makedirs(out_dir, exist_ok=True)

        raw_ext = art.signature.extension if art.signature else ("ps1" if art.is_powershell else "bin")
        # Defang executable extensions to prevent instant AV/EDR quarantine on analyst workstations
        if raw_ext.lower() in ("exe", "elf", "macho", "dll", "so", "dylib", "jar", "bin"):
            safe_ext = f"{raw_ext}.defanged" if raw_ext.lower() in ("exe", "elf", "macho", "dll") else raw_ext
        else:
            safe_ext = raw_ext

        bin_filename = f"artifact_{art.artifact_id}_{art.sha256[:8]}.{safe_ext}"
        bin_path = os.path.join(out_dir, bin_filename)

        with open(bin_path, "wb") as f:
            f.write(art.decoded_bytes)

        report_filename = f"artifact_{art.artifact_id}_{art.sha256[:8]}_report.txt"
        report_path = os.path.join(out_dir, report_filename)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"B64Lab Forensic Triage Report\n")
            f.write(f"=================================\n")
            f.write(f"SHA-256 : {art.sha256}\n")
            f.write(f"MD5     : {art.md5}\n")
            f.write(f"Size    : {len(art.decoded_bytes)} bytes\n")
            f.write(f"Entropy : {art.entropy}\n")
            f.write(f"Threat  : {art.threat_assessment}\n")
            f.write(f"Raw B64 : {art.raw_b64}\n")

        print(f"  [+] Saved payload to: {bin_path}")
        print(f"  [+] Saved IOC report to: {report_path}")

    @classmethod
    def _carve_file_interactive(cls) -> None:
        """Carves Base64 strings from a user-specified file."""
        UIComponents.header("FORENSIC LOG & SCRIPT CARVER")
        filepath = input("\n  Enter file path to carve: ").strip().strip('"')
        if not os.path.exists(filepath):
            print(f"  [!] File not found: {filepath}")
            UIComponents.pause()
            return

        print(f"\n  [*] Scanning '{filepath}' for Base64 artifacts...")
        artifacts = ArtifactCarver.carve_file(filepath)

        if not artifacts:
            print("  [!] No valid Base64 payloads detected in file.")
            UIComponents.pause()
            return

        print(f"\n  [+] Found {len(artifacts)} carved artifacts!\n")

        headers = ["ID", "LINE", "LEN", "ENTROPY", "DETECTED TYPE", "THREAT LEVEL"]
        rows = []
        for art in artifacts:
            sig = art.signature.extension.upper() if art.signature else ("PS1" if art.is_powershell else "TXT/BIN")
            rows.append([
                f"#{art.artifact_id}",
                f"L:{art.line_number}",
                f"{len(art.raw_b64)}",
                f"{art.entropy:.2f}",
                sig,
                art.threat_assessment.split()[0],
            ])

        UIComponents.table(headers, rows)

        sel = UIComponents.prompt("\nSelect artifact ID to inspect in detail (0 to cancel)")
        try:
            clean_sel = sel.lstrip('#').strip()
            art_id = int(clean_sel)
            selected = next((a for a in artifacts if a.artifact_id == art_id), None)
            if selected:
                cls._display_artifact_details(selected)
        except ValueError:
            pass

    @classmethod
    def _run_recursive_unpacker(cls) -> None:
        """Deep recursive de-obfuscator."""
        UIComponents.header("MULTI-STAGE RECURSIVE DE-OBFUSCATOR", "Unrolls Base64 -> GZIP / ZLIB -> Payload pipelines")
        user_input = input("\n  Paste nested Base64 string OR file path: ").strip().strip('"')
        if not user_input:
            return

        # Auto-detect if user passed a file path
        if os.path.isfile(user_input):
            try:
                with open(user_input, "r", encoding="utf-8", errors="ignore") as f:
                    file_content = f.read()
                carved = ArtifactCarver.carve_string(file_content, min_length=16)
                if carved:
                    raw_b64 = max(carved, key=lambda a: len(a.raw_b64)).raw_b64
                    print(f"  [+] Automatically carved Base64 payload from file ({len(raw_b64)} chars)...")
                else:
                    raw_b64 = file_content.strip()
            except Exception as e:
                print(f"  [!] Error reading file: {e}")
                raw_b64 = user_input
        else:
            raw_b64 = user_input

        print("\n  [*] Executing recursive deconstruction pipeline...")
        result = RecursiveUnpacker.unpack(raw_b64)

        palette = Theme.get_palette()
        p = palette.primary
        s = palette.secondary
        r = ANSI.RESET

        print(f"\n  {s}{ANSI.BOLD}─── DECONSTRUCTION TREE ({len(result.layers)} Stages Unrolled) ───{r}")
        for layer in result.layers:
            print(f"  Stage {layer.layer_number}: {p}{layer.operation}{r} | Size: {layer.input_size}B -> {layer.output_size}B | Entropy: {layer.entropy_before:.2f} -> {layer.entropy_after:.2f}")
            if layer.signature_detected:
                print(f"            └─ Detected Signature: {layer.signature_detected}")
            if layer.detail:
                print(f"            └─ Note: {layer.detail}")

        print(f"\n  {palette.accent}Final Extracted Payload:{r}")
        print(f"  Classification: {result.final_type}")
        print(f"  Description   : {result.final_description}")
        print(f"  Final Size    : {len(result.final_payload)} bytes")

        if result.powershell_script:
            print(f"\n  {palette.primary}[+] De-obfuscated PowerShell Script:{r}")
            print(f"  {result.powershell_script}")
        elif result.text_preview:
            print(f"\n  {palette.primary}[+] Extracted Plaintext:{r}")
            print(f"  {result.text_preview}")

        print(f"\n  {s}Hex View of Final Payload:{r}")
        print(HexViewer.render(result.final_payload, max_bytes=96, color=True))
        UIComponents.pause()

    @classmethod
    def _inspect_sample_artifact(cls) -> None:
        """Demonstrates carving against a built-in defanged forensic sample."""
        # Built-in sample: An obfuscated log line with an embedded harmless calc.exe PE header
        sample_log = (
            "2026-09-03 14:22:01 [WARN] Suspicious HTTP POST /api/upload from 192.168.1.105 "
            "Payload: TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
            "AAAAAAAAAAAAAAEAALcNiAAAAIg4HbDkAD43eHRlc3QAAAAAAAAA"
            " User-Agent: Mozilla/5.0"
        )
        print("\n  [+] Loading built-in forensic incident sample...")
        print(f"  {sample_log}\n")
        artifacts = ArtifactCarver.carve_string(sample_log)
        if artifacts:
            cls._display_artifact_details(artifacts[0])
