"""
Master Interactive Menu Router and CLI Controller for B64Lab.
Pure Python standard library implementation.
"""

import sys
import argparse
import os

from .ui.ansi import Terminal, ANSI
from .ui.themes import Theme
from .ui.components import UIComponents
from .academy.bitwise_lesson import BitwiseLesson
from .academy.rfc_lesson import RFCLesson
from .academy.offensive_lesson import OffensiveLesson
from .academy.defensive_lesson import DefensiveLesson
from .academy.glossary import Glossary
from .academy.mitre import MitreReference
from .triage.analyzer import TriageAnalyzer
from .triage.carver import ArtifactCarver
from .forge.console import ForgeConsole
from .forge.powershell import PowerShellForge
from .ctf.engine import CTFArena
from .workbench import Workbench
from .settings import SettingsMenu
from .core.bitwise import BitwiseEngine
from .core.entropy import ShannonEntropy

class B64LabApp:
    """Central Application Controller."""

    @classmethod
    def main_menu(cls) -> None:
        """Interactive Terminal Loop."""
        Terminal.initialize()

        while True:
            Terminal.clear()
            print(UIComponents.banner())

            palette = Theme.get_palette()
            s = palette.secondary
            t = palette.text
            d = palette.dim
            r = ANSI.RESET

            menu_items = [
                f"  {s}[1] ACADEMY         ::{r} {t}0-to-100 Interactive Bitwise & Security Theory{r}",
                f"  {ANSI.rgb_fg(0, 229, 255)}[2] TRIAGE / BLUE   ::{r} {t}Forensic Artifact Carver, Entropy & Magic Bytes{r}",
                f"  {ANSI.rgb_fg(255, 50, 50)}[3] FORGE / RED     ::{r} {t}Payload Simulation, UTF-16LE, Multi-stage Encoders{r}",
                f"  {s}[4] CTF CHALLENGES  ::{r} {t}8 Hands-on Forensic & De-obfuscation Labs{r}",
                f"  {s}[5] QUICK WORKBENCH ::{r} {t}Multi-Format Interactive Encoder/Decoder & Hex Dump{r}",
                f"  {s}[6] GLOSSARY & RFC  ::{r} {t}Cybersecurity Terms & MITRE ATT&CK Matrix{r}",
                f"  {s}[7] SETTINGS        ::{r} {t}Themes (Amber CRT, Phosphor Green, Ice Blue, Red){r}",
                f"  {d}[0] EXIT{r}",
            ]

            print("\n".join(menu_items))
            print()

            choice = UIComponents.prompt("Select module (0-7)")

            if choice == "0":
                print(f"\n  {d}[*] Exiting B64Lab. Happy hunting!{r}\n")
                break
            elif choice == "1":
                cls._academy_menu()
            elif choice == "2":
                TriageAnalyzer.run()
            elif choice == "3":
                ForgeConsole.run()
            elif choice == "4":
                CTFArena.run()
            elif choice == "5":
                Workbench.run()
            elif choice == "6":
                cls._reference_menu()
            elif choice == "7":
                SettingsMenu.run()

    @classmethod
    def _academy_menu(cls) -> None:
        """Submenu for educational courses."""
        while True:
            UIComponents.header(
                "B64LAB ACADEMY: 0-TO-100 CYBERSECURITY CURRICULUM",
                "Bitwise mathematics, RFC 4648 standards, and real-world tradecraft"
            )
            print("  [1] Module 1: Bitwise Mechanics & Binary Slicing (Octets to Sextets)")
            print("  [2] Module 2: RFC 4648 Standards (Base64, Base64URL, Base32, Hex)")
            print("  [3] Module 3: Offensive Tradecraft (PowerShell UTF-16LE, Droppers, Evasion)")
            print("  [4] Module 4: Defensive Triage (Shannon Entropy, Magic Bytes, Log Carving)")
            print("  [0] Return to Main Menu\n")

            sel = UIComponents.prompt("Select academy module (0-4)")
            if sel == "0":
                break
            elif sel == "1":
                BitwiseLesson.run()
            elif sel == "2":
                RFCLesson.run()
            elif sel == "3":
                OffensiveLesson.run()
            elif sel == "4":
                DefensiveLesson.run()

    @classmethod
    def _reference_menu(cls) -> None:
        """Submenu for references."""
        while True:
            UIComponents.header("REFERENCE & INTELLIGENCE DATABASE")
            print("  [1] Searchable Cybersecurity Glossary")
            print("  [2] MITRE ATT&CK Matrix Reference (T1027, T1059, T1132)")
            print("  [0] Return to Main Menu\n")

            sel = UIComponents.prompt("Select option (0-2)")
            if sel == "0":
                break
            elif sel == "1":
                Glossary.run()
            elif sel == "2":
                MitreReference.run()

    @classmethod
    def run_cli_args(cls) -> None:
        """Parses CLI flags for headless/scripted usage."""
        parser = argparse.ArgumentParser(
            prog="b64lab",
            description="B64Lab: The Zero-Dependency Cybersecurity Base64 Academy, Simulator & Triage Engine.",
        )
        subparsers = parser.add_subparsers(dest="command", help="Operational Subcommands")

        # Encode command
        enc_p = subparsers.add_parser("encode", help="Encode text or file to Base64")
        enc_p.add_argument("text", help="Text string to encode")
        enc_p.add_argument("--url", action="store_true", help="Use URL-safe alphabet")

        # Decode command
        dec_p = subparsers.add_parser("decode", help="Decode Base64 string to bytes/text")
        dec_p.add_argument("b64string", help="Base64 string to decode")
        dec_p.add_argument("--utf16", action="store_true", help="Decode as PowerShell UTF-16LE")

        # Trace command
        trace_p = subparsers.add_parser("trace", help="View step-by-step bitwise breakdown")
        trace_p.add_argument("text", help="Text string to trace")

        # Carve command
        carve_p = subparsers.add_parser("carve", help="Carve Base64 artifacts from a file or stdin")
        carve_p.add_argument("filepath", help="Path to file, log, or '-' for stdin")
        carve_p.add_argument("--format", choices=["table", "csv", "json", "sqlite"], default="table", help="Output format")
        carve_p.add_argument("--output", "-o", help="Write output to file (required for sqlite, optional for csv/json)")
        carve_p.add_argument("--min-len", type=int, default=16, help="Minimum Base64 string length")

        # PowerShell forge command
        ps_p = subparsers.add_parser("ps", help="Generate PowerShell -EncodedCommand (UTF-16LE)")
        ps_p.add_argument("script", help="PowerShell command script")

        # Entropy command
        ent_p = subparsers.add_parser("entropy", help="Calculate Shannon entropy")
        ent_p.add_argument("string", help="String to analyze")

        args = parser.parse_args()

        if not args.command:
            # If no args passed, launch interactive start menu!
            cls.main_menu()
            return

        Terminal.initialize()

        if args.command == "encode":
            import base64
            b = args.text.encode("utf-8")
            res = base64.urlsafe_b64encode(b).decode() if args.url else base64.b64encode(b).decode()
            print(res)

        elif args.command == "decode":
            import base64
            s, _ = BitwiseEngine.normalize_padding(args.b64string)
            try:
                raw = base64.b64decode(s, validate=False)
                if args.utf16:
                    print(raw.decode("utf-16le", errors="ignore"))
                else:
                    try:
                        print(raw.decode("utf-8"))
                    except UnicodeDecodeError:
                        print(raw)
            except Exception as e:
                print(f"[!] Error: Unable to decode Base64 payload: {e}")

        elif args.command == "trace":
            BitwiseLesson._walkthrough_example(args.text, pause=False)

        elif args.command == "carve":
            if args.filepath == "-":
                stream = sys.stdin
            else:
                if not os.path.exists(args.filepath):
                    print(f"[!] Error: File not found: {args.filepath}")
                    return
                stream = open(args.filepath, "r", encoding="utf-8", errors="ignore")

            try:
                artifacts = list(ArtifactCarver.carve_stream(stream, min_length=args.min_len))
            finally:
                if args.filepath != "-":
                    stream.close()

            # Output Formatting
            if args.format == "csv":
                if args.output:
                    ArtifactCarver.export_csv(artifacts, args.output)
                    print(f"[+] Exported {len(artifacts)} carved artifacts to CSV: {args.output}")
                else:
                    import csv
                    import io
                    buf = io.StringIO()
                    writer = csv.writer(buf)
                    writer.writerow(["ID", "Line", "Threat", "Entropy", "Signature", "SHA256", "Raw_B64"])
                    for a in artifacts:
                        sig = a.signature.extension if a.signature else ("ps1" if a.is_powershell else "None")
                        writer.writerow([a.artifact_id, a.line_number, a.threat_assessment, a.entropy, sig, a.sha256, a.raw_b64])
                    print(buf.getvalue().strip())

            elif args.format == "json":
                if args.output:
                    ArtifactCarver.export_jsonl(artifacts, args.output)
                    print(f"[+] Exported {len(artifacts)} carved artifacts to JSON Lines: {args.output}")
                else:
                    import json
                    for a in artifacts:
                        rec = {
                            "id": a.artifact_id,
                            "line": a.line_number,
                            "threat": a.threat_assessment,
                            "entropy": a.entropy,
                            "sig": a.signature.extension if a.signature else None,
                            "sha256": a.sha256,
                            "raw_b64": a.raw_b64
                        }
                        print(json.dumps(rec))

            elif args.format == "sqlite":
                out_db = args.output or "carved_artifacts.db"
                ArtifactCarver.export_sqlite(artifacts, out_db)
                print(f"[+] Exported {len(artifacts)} artifacts into SQLite database: {out_db}")
                print(f"    Table: 'carved_artifacts' (Indexed on sha256 and entropy)")

            else: # table format
                print(f"[+] Carved {len(artifacts)} Base64 artifacts:")
                headers = ["ID", "LINE", "ENTROPY", "DETECTED TYPE", "THREAT", "SHA256"]
                rows = []
                for a in artifacts:
                    sig = a.signature.extension.upper() if a.signature else ("PS1" if a.is_powershell else "RAW")
                    rows.append([f"#{a.artifact_id}", f"L:{a.line_number}", f"{a.entropy:.2f}", sig, a.threat_assessment.split()[0], a.sha256[:12]])
                UIComponents.table(headers, rows)

        elif args.command == "ps":
            res = PowerShellForge.craft(args.script)
            print(f"UTF-16LE Base64: {res['b64_valid_utf16le']}")
            print(f"CLI Invocation : {res['execution_syntax']}")

        elif args.command == "entropy":
            rep = ShannonEntropy.analyze(args.string)
            print(f"Entropy: {rep.entropy:.4f}/8.00 [{rep.classification}] Threat: {rep.threat_level}")

def main() -> None:
    """Entry point."""
    B64LabApp.run_cli_args()

if __name__ == "__main__":
    main()
