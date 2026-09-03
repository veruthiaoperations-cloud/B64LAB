"""
Offensive Tradecraft & Adversary Emulation Lesson.
Pure Python standard library implementation.
"""

from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI

class OffensiveLesson:
    """
    Teaches how adversaries weaponize Base64 for Living-off-the-Land (LotL),
    payload delivery, and defense evasion.
    """

    @classmethod
    def run(cls) -> None:
        while True:
            UIComponents.header(
                "MODULE 3: ADVERSARY TRADECRAFT & OFFENSIVE OBFUSCATION",
                "Learn how threat actors use Base64 to bypass filters, stage droppers, and evade AV"
            )

            print("  Base64 provides zero cryptographic security, but adversaries use it heavily")
            print("  for evasion, filter-bypassing, and staging secondary malware components.\n")

            print("  [1] PowerShell -EncodedCommand: The UTF-16LE Architecture")
            print("  [2] Multi-Stage Droppers (Base64 -> Gzip -> Memory Injection)")
            print("  [3] Custom Alphabet Substitution (Bypassing Static Signatures)")
            print("  [4] Padding & Whitespace Evasion Techniques")
            print("  [0] Return to Academy Menu\n")

            choice = UIComponents.prompt("Select option (0-4)")
            if choice == "0":
                break
            elif choice == "1":
                cls._explain_powershell_utf16le()
            elif choice == "2":
                cls._explain_multistage_droppers()
            elif choice == "3":
                cls._explain_custom_alphabets()
            elif choice == "4":
                cls._explain_evasion_tricks()

    @classmethod
    def _explain_powershell_utf16le(cls) -> None:
        UIComponents.header("POWERSHELL -ENCODEDCOMMAND: THE UTF-16LE ARCHITECTURE")
        lines = [
            "THE CORE PRINCIPLE:",
            "  Windows PowerShell's command-line switch '-EncodedCommand' (or -e, -enc)",
            "  accepts a Base64-encoded Unicode script block.",
            "",
            "THE CRITICAL GOTCHA: WINDOWS UNICODE IS UTF-16LE, NOT UTF-8!",
            "  In UTF-16LE (Little Endian), standard ASCII characters are stored as TWO bytes,",
            "  with an alternating 0x00 null byte.",
            "",
            "  Command: 'whoami'",
            "  - In UTF-8 bytes    : 77 68 6f 61 6d 69 (6 bytes)",
            "    -> Base64 encode  : 'd2hvYW1p'",
            "    -> PowerShell runs: FAILS! Windows cannot parse UTF-8 bytes as an EncodedCommand.",
            "",
            "  - In UTF-16LE bytes : 77 00 68 00 6f 00 61 00 6d 00 69 00 (12 bytes)",
            "    -> Base64 encode  : 'dwBoAG8AYQBtAGkA'",
            "    -> PowerShell runs: SUCCESS!",
            "",
            "FORENSIC LESSON FOR SOC ANALYSTS:",
            "  When you decode an adversary's PowerShell script, you MUST decode using 'utf-16le'.",
            "  If you decode as ASCII, you get: 'w\\x00h\\x00o\\x00a\\x00m\\x00i\\x00'."
        ]
        UIComponents.box(lines, title="POWERSHELL ENCODING ARCHITECTURE", style="double")
        UIComponents.pause()

    @classmethod
    def _explain_multistage_droppers(cls) -> None:
        UIComponents.header("MULTI-STAGE DROPPERS & FILELESS EXECUTION")
        lines = [
            "TYPICAL ADVERSARY PAYLOAD CHAIN:",
            "",
            "  [Phishing Document / LNK file / Dropper Script]",
            "          │",
            "          ▼",
            "  [Stage 1: Base64 String in Memory]",
            "          │  (b64decode in RAM)",
            "          ▼",
            "  [Stage 2: GZIP / Deflate Compressed Stream]",
            "          │  (System.IO.Compression.GZipStream)",
            "          ▼",
            "  [Stage 3: Inner Base64 or Encrypted Shellcode]",
            "          │  (VirtualAlloc + RtlMoveMemory + CreateThread)",
            "          ▼",
            "  [Final Beacon / Cobalt Strike / Meterpreter Execution]",
            "",
            "WHY ATTACKERS DO THIS:",
            "  1. Compression drastically reduces payload footprint (evades email size limits).",
            "  2. Multi-layer nesting prevents standard string matching and Yara rules from firing.",
            "  3. Unpacking occurs purely in volatile RAM, bypassing disk-based antivirus scanners."
        ]
        UIComponents.box(lines, title="NESTED DEOBFUSCATION PIPELINE", style="rounded")
        UIComponents.pause()

    @classmethod
    def _explain_custom_alphabets(cls) -> None:
        UIComponents.header("CUSTOM ALPHABET SUBSTITUTION CIPHERS")
        lines = [
            "HOW THREAT ACTORS DEFEAT STATIC DETECTION:",
            "  Standard Base64 strings always begin with predictable sequences:",
            "  - A Windows PE executable always starts with 'TVq' or 'TVo' (from 'MZ').",
            "  - A Linux ELF binary always starts with 'f0VM' (from '\\x7fELF').",
            "  - A PDF document starts with 'JVBERi' (from '%PDF-').",
            "",
            "  Security tools create static YARA signatures looking for those exact strings!",
            "",
            "THE THREAT ACTOR COUNTERMEASURE:",
            "  Threat groups (e.g. FIN7, APT29) replace the standard alphabet:",
            "  Standard: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'",
            "  Custom  : '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'",
            "",
            "  With the custom table, 'MZ' no longer encodes to 'TVq'!",
            "  Defenders must reverse the translation table to reconstruct the original payload."
        ]
        UIComponents.box(lines, title="CUSTOM ALPHABET EVASION", style="double")
        UIComponents.pause()

    @classmethod
    def _explain_evasion_tricks(cls) -> None:
        UIComponents.header("PADDING & REGEX EVASION TRICKS")
        lines = [
            "EVASION TECHNIQUE 1: PADDING STRIPPING",
            "  Attackers omit trailing '=' characters.",
            "  Sloppy regex: '^[A-Za-z0-9+/]{4}*={0,2}$' fails to match!",
            "  Yet standard Python or C# decoders can easily be patched or configured to accept it.",
            "",
            "EVASION TECHNIQUE 2: WHITESPACE & NEWLINE INJECTION",
            "  RFC 4648 Section 3.1 allows decoders to ignore whitespace.",
            "  Attackers insert random carriage returns, spaces, or tabs inside the string to break",
            "  fixed-length regex rules.",
            "",
            "EVASION TECHNIQUE 3: CHUNK CONCATENATION",
            "  PowerShell scripts frequently assemble Base64 strings using variable concatenation:",
            "  $a = 'dwBoA'; $b = 'G8AYQ'; $c = 'BtAGkA'; &([char]105+[char]101+[char]120) ($a+$b+$c)"
        ]
        UIComponents.box(lines, title="EVASION RESILIENCE", style="rounded")
        UIComponents.pause()
