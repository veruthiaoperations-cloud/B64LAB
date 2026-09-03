"""
Comprehensive Searchable Cybersecurity Glossary.
Pure Python standard library implementation.
"""

from typing import Dict, List, Optional
from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI

GLOSSARY_DATA: Dict[str, Dict[str, str]] = {
    "BASE64": {
        "term": "Base64 (RFC 4648 Section 4)",
        "definition": "A binary-to-text encoding scheme that represents binary data in an ASCII string format by translating it into a radix-64 representation using 64 printable characters (A-Z, a-z, 0-9, +, /).",
        "context": "Used in MIME email attachments, SSL/TLS certificates (PEM), and widely abused by malware droppers to conceal payloads.",
    },
    "BASE64URL": {
        "term": "Base64URL (RFC 4648 Section 5)",
        "definition": "A variant of Base64 where '+' is replaced by '-' and '/' is replaced by '_'. Padding '=' is typically omitted.",
        "context": "Standard for JSON Web Tokens (JWTs) and URL query parameters to avoid character collisions with URL delimiters and filename paths.",
    },
    "BASE32": {
        "term": "Base32 (RFC 4648 Section 6)",
        "definition": "A binary-to-text encoding using a 32-character case-insensitive alphabet (A-Z, 2-7). Encodes 5 bits per character.",
        "context": "Used in Two-Factor Authentication (TOTP secret keys) and abused by threat actors for DNS Tunneling exfiltration where DNS is case-insensitive.",
    },
    "OCTET": {
        "term": "Octet (8 bits)",
        "definition": "A unit of digital information in computing and telecommunications that consists of eight bits.",
        "context": "Base64 processes octets in 3-byte groups (3 * 8 = 24 bits) to produce 4 sextets.",
    },
    "SEXTET": {
        "term": "Sextet (6 bits)",
        "definition": "A group of six bits, representing values from 0 to 63 (2^6 = 64).",
        "context": "Each Base64 character represents exactly one sextet.",
    },
    "PADDING": {
        "term": "Padding ('=' and '==')",
        "definition": "Special marker characters appended to the end of a Base64 string when the raw input length is not a multiple of 3 bytes.",
        "context": "1 remaining byte requires '=='; 2 remaining bytes require '='. Attackers often strip padding to evade strict regex detection rules.",
    },
    "SHANNON ENTROPY": {
        "term": "Shannon Entropy",
        "definition": "A mathematical measurement of information density, randomness, and uncertainty in a dataset, measured from 0.0 to 8.0 bits per symbol.",
        "context": "Base64 strings cluster tightly between ~5.10 and ~5.95 bits/symbol. SOC analysts use this threshold to detect encoded beacons and droppers.",
    },
    "MAGIC BYTES": {
        "term": "Magic Bytes / File Signatures",
        "definition": "Specific byte sequences located at the beginning (offset 0) of a file format to uniquely identify its type regardless of file extension.",
        "context": "Examples include '4D 5A' ('MZ' for Windows executables) and '%PDF-' for PDFs. Crucial for carving files from encoded blobs.",
    },
    "UTF-16LE": {
        "term": "UTF-16LE (Little Endian)",
        "definition": "A character encoding format where characters are represented with two bytes, with the least significant byte stored first.",
        "context": "PowerShell's -EncodedCommand expects a Base64 string representing UTF-16LE bytes, introducing alternating 0x00 null bytes.",
    },
    "DROFFER": {
        "term": "Malware Dropper",
        "definition": "A type of Trojan designed to install or stage malware (viruses, backdoors) onto a target system.",
        "context": "Droppers frequently store the secondary executable as a compressed Base64 string inside script files or Office macros.",
    },
    "LIVING-OFF-THE-LAND": {
        "term": "Living-off-the-Land (LotL)",
        "definition": "A cyberattack technique where adversaries use legitimate, pre-installed operating system binaries (LOLBins) to conduct malicious actions.",
        "context": "Examples include using powershell.exe, certutil.exe, and wmic.exe to decode Base64 payloads without bringing foreign tools.",
    },
    "DEFANGING": {
        "term": "Defanging",
        "definition": "The practice of modifying malicious indicators (URLs, IPs, domain names) to prevent accidental execution or clicking in reports.",
        "context": "Example: Changing https://evil.com to hxxps://evil[.]com.",
    },
    "ARTIFACT CARVING": {
        "term": "Forensic Artifact Carving",
        "definition": "The process of extracting specific files, payloads, or fragments from raw disk images, memory dumps, or log files without file system metadata.",
        "context": "Carving Base64 strings involves regex pattern extraction followed by magic byte identification and hash computation.",
    },
}

class Glossary:
    """Searchable interactive cybersecurity terminology glossary."""

    @classmethod
    def run(cls) -> None:
        while True:
            UIComponents.header(
                "GLOSSARY: CYBERSECURITY & ENCODING TERMINOLOGY",
                "Quick reference for SOC analysts, incident responders, and cert candidates"
            )

            terms = list(GLOSSARY_DATA.keys())
            for idx, key in enumerate(terms, start=1):
                item = GLOSSARY_DATA[key]
                print(f"  [{idx:02d}] {item['term']}")

            print("\n  [S] Search by keyword")
            print("  [0] Return to Main Menu\n")

            choice = UIComponents.prompt("Select entry number or [S]earch (0 to return)")
            if choice == "0":
                break
            elif choice.upper() == "S":
                cls._search()
            else:
                try:
                    num = int(choice)
                    if 1 <= num <= len(terms):
                        cls._display_term(terms[num - 1])
                    else:
                        print("  [!] Invalid number.")
                except ValueError:
                    print("  [!] Please enter a valid number or 'S'.")

    @classmethod
    def _display_term(cls, key: str) -> None:
        item = GLOSSARY_DATA[key]
        UIComponents.header(item["term"])
        lines = [
            f"DEFINITION:",
            f"  {item['definition']}",
            "",
            f"CYBERSECURITY CONTEXT & OPERATIONAL RELEVANCE:",
            f"  {item['context']}",
        ]
        UIComponents.box(lines, title="TERM CARD", style="rounded")
        UIComponents.pause()

    @classmethod
    def _search(cls) -> None:
        query = input("\n  Enter search term: ").strip().lower()
        if not query:
            return

        matches = []
        for key, val in GLOSSARY_DATA.items():
            if query in key.lower() or query in val["term"].lower() or query in val["definition"].lower() or query in val["context"].lower():
                matches.append(key)

        if not matches:
            print(f"\n  [!] No glossary entries matched '{query}'.")
            UIComponents.pause()
            return

        print(f"\n  Found {len(matches)} matching entries:")
        for idx, key in enumerate(matches, start=1):
            print(f"  [{idx}] {GLOSSARY_DATA[key]['term']}")

        sel = UIComponents.prompt("Select match number (0 to cancel)")
        try:
            num = int(sel)
            if 1 <= num <= len(matches):
                cls._display_term(matches[num - 1])
        except ValueError:
            pass
