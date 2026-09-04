"""
MITRE ATT&CK Matrix Reference Engine for Encoding Techniques.
Pure Python standard library implementation.
"""

from typing import List, Dict
from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI

MITRE_TECHNIQUES = [
    {
        "id": "T1027",
        "name": "Obfuscated Files or Information",
        "tactic": "Defense Evasion",
        "description": "Adversaries may attempt to make an executable or file difficult to discover or analyze by encrypting, encoding, or otherwise obfuscating its contents on the system.",
        "b64_role": "Adversaries encode executable binaries (PE/ELF) into Base64 strings to hide from signature-based antivirus solutions.",
        "mitigation": "Analyze entropy of files and scripts. Inspect decoded strings using magic byte detection before execution.",
    },
    {
        "id": "T1059.001",
        "name": "Command & Scripting Interpreter: PowerShell",
        "tactic": "Execution",
        "description": "Adversaries may abuse the PowerShell commands and scripts for execution, taking advantage of built-in LotL capabilities.",
        "b64_role": "Adversaries execute 'powershell.exe -EncodedCommand <UTF16LE_B64>' to bypass simple command-line keyword logging filters.",
        "mitigation": "Enable PowerShell ScriptBlock Logging (Event ID 4104) and Transcription. Audit command-line parameters for '-e', '-enc', and '-EncodedCommand'.",
    },
    {
        "id": "T1132.001",
        "name": "Data Encoding: Standard Cryptographic / Base64",
        "tactic": "Command and Control",
        "description": "Adversaries may encode data with a standard data encoding system to make the content of command and control traffic more difficult to detect.",
        "b64_role": "Beacon messages, system metadata, and command outputs are encoded in Base64 and embedded into HTTP headers or cookies.",
        "mitigation": "Inspect HTTP headers (Cookie, Authorization, User-Agent) for Base64 character sets and statistical entropy clustering between 5.10 and 5.95.",
    },
    {
        "id": "T1071.004",
        "name": "Application Layer Protocol: DNS (Tunneling)",
        "tactic": "Command and Control",
        "description": "Adversaries may communicate using the Domain Name System (DNS) application layer protocol to avoid detection / network filtering.",
        "b64_role": "Data is segmented into Base32 or Base64URL blobs and sent as subdomain queries (e.g. data.attacker.com).",
        "mitigation": "Monitor DNS server logs for abnormally long subdomains (>50 chars), high query volume to single domains, and high subdomain entropy.",
    },
]

class MitreReference:
    """Interactive browser for MITRE ATT&CK techniques related to encoding."""

    @classmethod
    def run(cls) -> None:
        while True:
            UIComponents.header(
                "MITRE ATT&CK MAPPINGS: ENCODING & OBFUSCATION",
                "Framework mapping of adversary tactics, techniques, and procedures (TTPs)"
            )

            headers = ["TECHNIQUE ID", "TECHNIQUE NAME", "TACTIC"]
            rows = [
                [t["id"], t["name"], t["tactic"]]
                for t in MITRE_TECHNIQUES
            ]
            UIComponents.table(headers, rows)

            print("\n  Select a technique for deep-dive analysis:")
            for idx, t in enumerate(MITRE_TECHNIQUES, start=1):
                print(f"  [{idx}] {t['id']}: {t['name']}")
            print("  [0] Return to Academy Menu\n")

            choice = UIComponents.prompt("Select technique (0-4)")
            if choice == "0":
                break
            try:
                num = int(choice)
                if 1 <= num <= len(MITRE_TECHNIQUES):
                    cls._display_technique(MITRE_TECHNIQUES[num - 1])
                else:
                    print("  [!] Invalid selection.")
            except ValueError:
                print("  [!] Please enter a valid number.")

    @classmethod
    def _display_technique(cls, t: Dict[str, str]) -> None:
        UIComponents.header(f"{t['id']} - {t['name']}", f"Tactic: {t['tactic']}")
        lines = [
            f"TECHNIQUE DESCRIPTION:",
            f"  {t['description']}",
            "",
            f"HOW ADVERSARIES WEAPONIZE BASE64:",
            f"  {t['b64_role']}",
            "",
            f"DEFENSIVE DETECTION & MITIGATION:",
            f"  {t['mitigation']}",
        ]
        UIComponents.box(lines, title=f"ATT&CK {t['id']}", style="double")
        UIComponents.pause()
