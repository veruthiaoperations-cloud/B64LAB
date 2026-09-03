"""
Defensive Tradecraft & Forensic Analysis Lesson.
Pure Python standard library implementation.
"""

from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI

class DefensiveLesson:
    """
    Teaches SOC analysts and incident responders how to hunt, carve,
    and de-obfuscate Base64 artifacts from enterprise telemetry and logs.
    """

    @classmethod
    def run(cls) -> None:
        while True:
            UIComponents.header(
                "MODULE 4: DEFENSIVE TRIAGE & FORENSIC ARTIFACT CARVING",
                "Learn the techniques SOC analysts use to detect, carve, and analyze encoded payloads"
            )

            print("  Defenders cannot rely on manual decoding during high-severity incidents.")
            print("  Automated carving, entropy analysis, and magic byte detection are core skills.\n")

            print("  [1] Shannon Entropy: Math, Thresholds, and Threat Scoring")
            print("  [2] Magic Bytes & File Signatures (Carving Hidden Executables)")
            print("  [3] Log File Triage: Carving from Windows Events & Web Logs")
            print("  [4] Defanged Payload Handling & Sandbox Export Protocols")
            print("  [0] Return to Academy Menu\n")

            choice = UIComponents.prompt("Select option (0-4)")
            if choice == "0":
                break
            elif choice == "1":
                cls._explain_shannon_entropy()
            elif choice == "2":
                cls._explain_magic_bytes()
            elif choice == "3":
                cls._explain_log_carving()
            elif choice == "4":
                cls._explain_defanged_handling()

    @classmethod
    def _explain_shannon_entropy(cls) -> None:
        UIComponents.header("SHANNON ENTROPY: MATHEMATICAL THREAT HUNTING")
        lines = [
            "DEFINITION:",
            "  Shannon Entropy measures the degree of randomness or information density in a sequence.",
            "  Formula: H(X) = - Σ ( P(x_i) * log2( P(x_i) ) )",
            "  Scale: 0.0 (zero randomness, e.g. 'AAAAAAAA') to 8.0 (pure random byte distribution).",
            "",
            "OPERATIONAL BENCHMARKS IN THREAT HUNTING:",
            "  • 0.00 - 3.50 : Repetitive padding, null byte arrays, or sparse memory buffers.",
            "  • 3.50 - 4.80 : Natural English text, source code, JSON, XML (Low threat).",
            "  • 5.10 - 5.95 : BASE64 ENCODED BLOB (Suspicious).",
            "                  Because Base64 evenly distributes 64 symbols, its entropy clusters",
            "                  reliably within this exact narrow band!",
            "  • 6.00 - 7.00 : Compressed files (ZIP, GZIP) or compiled machine code.",
            "  • 7.20 - 8.00 : High-grade cryptographic ciphertext or packed malware (Critical).",
            "",
            "SOC ANALYST APPLICATION:",
            "  SIEM and EDR queries filter web headers or DNS queries where entropy > 5.2 to",
            "  immediately isolate base64 beacons from benign browsing traffic."
        ]
        UIComponents.box(lines, title="ENTROPY THRESHOLD GUIDE", style="rounded")
        UIComponents.pause()

    @classmethod
    def _explain_magic_bytes(cls) -> None:
        UIComponents.header("MAGIC BYTES & FORENSIC FILE CARVING")
        lines = [
            "WHAT ARE MAGIC BYTES?",
            "  File extensions (.exe, .pdf, .jpg) can be easily spoofed or stripped.",
            "  Operating systems and forensic software rely on the first few bytes (the file signature)",
            "  to determine what a file actually is.",
            "",
            "CRITICAL FORENSIC SIGNATURES TO MEMORIZE FOR CERTS & INTERVIEWS:",
            "  • 4D 5A          ('MZ')    -> Windows Portable Executable (EXE/DLL)",
            "  • 7F 45 4C 46    ('\\x7fELF') -> Linux / Unix Executable",
            "  • 50 4B 03 04    ('PK..')  -> ZIP archive / Office OpenXML (.docx, .xlsx)",
            "  • 25 50 44 46    ('%PDF-') -> PDF Document",
            "  • 1F 8B 08                 -> GZIP Compressed Data",
            "  • 89 50 4E 47    ('\\x89PNG') -> PNG Image File",
            "",
            "BASE64 REPRESENTATIONS OF CRITICAL HEADERS:",
            "  When an attacker base64 encodes an executable, the 'MZ' bytes produce:",
            "  - 'TVq' (if offset 0 aligns with 3-byte boundary)",
            "  - 'TVo' or 'TVp' depending on adjacent padding",
            "  Seeing 'TVq' in an encoded parameter is an immediate red flag for an embedded PE!"
        ]
        UIComponents.box(lines, title="MAGIC BYTE SIGNATURES", style="double")
        UIComponents.pause()

    @classmethod
    def _explain_log_carving(cls) -> None:
        UIComponents.header("LOG CARVING: WINDOWS EVENTS & WEB SERVERS")
        lines = [
            "COMMON LOG SOURCES CONTAINING BASE64 THREATS:",
            "  1. Windows Event ID 4104 (ScriptBlock Logging):",
            "     Logs PowerShell execution. Attackers frequently invoke:",
            "     powershell.exe -e <Base64_UTF16LE_Blob>",
            "",
            "  2. Web Server Access Logs (Apache / Nginx / IIS):",
            "     Attackers inject Base64 payloads into HTTP headers (User-Agent, Cookie)",
            "     or URL query strings to stage webshells or deliver SQLi/command injection.",
            "",
            "  3. Sysmon Event ID 1 (Process Creation):",
            "     Captures full CLI arguments including encoded command lines.",
            "",
            "THE CARVING ALGORITHM:",
            "  A forensic carver scans the log with regex for strings of length >= 16 consisting of",
            "  valid Base64 characters, filters by entropy (5.1 - 5.95), decodes the bytes, checks",
            "  magic bytes, and produces a structured incident report."
        ]
        UIComponents.box(lines, title="LOG HUNTING PROTOCOL", style="rounded")
        UIComponents.pause()

    @classmethod
    def _explain_defanged_handling(cls) -> None:
        UIComponents.header("DEFANGED PAYLOAD SAFETY & ARTIFACT EXPORT")
        lines = [
            "SAFETY PROTOCOL FOR INCIDENT RESPONDERS:",
            "  1. NEVER directly execute carved scripts or binaries on your analysis machine.",
            "  2. Calculate cryptographic hashes immediately (MD5 and SHA-256) for IOC matching.",
            "  3. Check the hash against VirusTotal / MISP / threat intelligence feeds.",
            "  4. Defang URLs and IPs when reporting (e.g. hxxps://malicious[.]com).",
            "  5. Export carved payloads into an isolated, quarantined directory or sandbox."
        ]
        UIComponents.box(lines, title="DEFENSIVE SAFETY STANDARDS", style="rounded")
        UIComponents.pause()
