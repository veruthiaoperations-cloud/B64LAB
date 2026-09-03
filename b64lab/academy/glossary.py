"""
Comprehensive Searchable Cybersecurity Glossary.
Pure Python standard library implementation.
"""

from typing import Dict, List, Optional
from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI

GLOSSARY_DATA: Dict[str, Dict[str, str]] = {
    "BIT": {
        "term": "Bit (Binary Digit)",
        "definition": "The most fundamental unit of digital data, representing a microscopic electronic state of 0 (OFF) or 1 (ON).",
        "context": "All computer architectures, ciphers, and encoding algorithms manipulate collections of bits at the hardware level.",
    },
    "BYTE": {
        "term": "Byte / Octet (8 bits)",
        "definition": "A unit of digital storage consisting of 8 consecutive bits, representing a decimal value from 0 to 255 (2^8 = 256 states).",
        "context": "Base64 processes data in 3-byte blocks (3 * 8 = 24 bits) to produce four 6-bit characters.",
    },
    "ASCII": {
        "term": "ASCII Character Encoding",
        "definition": "American Standard Code for Information Interchange. A 7-bit character encoding defining 128 characters (English letters, digits, control codes).",
        "context": "Base64 translates raw binary data into safe, printable ASCII characters to prevent communication protocol corruption.",
    },
    "UTF-8": {
        "term": "UTF-8 Character Encoding",
        "definition": "A variable-width character encoding capable of encoding all 1,112,064 valid character code points in Unicode using 1 to 4 one-byte (8-bit) units.",
        "context": "The dominant encoding standard of the internet and modern operating systems (Linux, macOS).",
    },
    "UTF-16LE": {
        "term": "UTF-16LE (Little Endian)",
        "definition": "A 16-bit character encoding where standard ASCII characters are represented by 2 bytes (the character byte followed by a 0x00 null byte).",
        "context": "PowerShell's -EncodedCommand strictly requires UTF-16LE Base64 strings. Normal UTF-8 strings crash with syntax errors.",
    },
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
    "SEXTET": {
        "term": "Sextet (6 bits)",
        "definition": "A group of six bits, representing values from 0 to 63 (2^6 = 64).",
        "context": "Each Base64 character represents exactly one sextet.",
    },
    "PADDING": {
        "term": "Padding ('=' and '==')",
        "definition": "Special marker characters appended to the end of a Base64 string when the raw input length is not an exact multiple of 3 bytes.",
        "context": "1 remaining byte requires '=='; 2 remaining bytes require '='. Attackers often strip padding to evade strict regex detection rules.",
    },
    "DATA URI": {
        "term": "Data URI Scheme (RFC 2397)",
        "definition": "A Uniform Resource Identifier scheme that provides a way to include data in-line in web pages as if they were external resources (e.g. data:image/png;base64,...).",
        "context": "Abused in phishing emails to bypass external image blocking, and in HTML Smuggling attacks to assemble malware client-side.",
    },
    "HTML SMUGGLING": {
        "term": "HTML Smuggling (MITRE T1027.006)",
        "definition": "A cyberattack technique using HTML5 and JavaScript features to assemble malicious files client-side from Base64 strings, bypassing perimeter email and web filters.",
        "context": "No executable traverses the network perimeter; the binary is constructed directly inside the victim's local browser memory.",
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
    "DROPPER": {
        "term": "Malware Dropper / Stager",
        "definition": "A preliminary Trojan payload designed to stage, decompress, or install secondary malware onto a target system.",
        "context": "Droppers frequently store the secondary executable as a compressed Base64 string inside script files or Office macros.",
    },
    "C2 BEACON": {
        "term": "C2 Beacon (Command and Control)",
        "definition": "Periodic outbound network heartbeat signals sent from an infected host to an adversary-controlled server to request commands and exfiltrate data.",
        "context": "Often transmitted over DNS or HTTP using Base32 or Base64 encoding to blend with legitimate background web traffic.",
    },
    "SOC ANALYST": {
        "term": "SOC Analyst (Security Operations Center)",
        "definition": "A defensive cybersecurity professional responsible for monitoring organizational telemetry, triaging alerts, and responding to cyber incidents.",
        "context": "SOC analysts routinely triage encoded command lines, carve artifacts from web server access logs, and analyze phishing attachments.",
    },
    "SIEM": {
        "term": "SIEM (Security Information & Event Management)",
        "definition": "A centralized software platform (e.g. Splunk, Microsoft Sentinel) that aggregates, correlates, and analyzes log telemetry across an enterprise.",
        "context": "B64Lab outputs directly to JSON Lines and CSV so carved artifacts and entropy scores can be ingested into enterprise SIEM pipelines.",
    },
    "LIVING-OFF-THE-LAND": {
        "term": "Living-off-the-Land (LotL / LOLBins)",
        "definition": "A cyberattack technique where adversaries use legitimate, pre-installed operating system binaries to conduct malicious actions without downloading external tools.",
        "context": "Examples include using powershell.exe, certutil.exe, and wmic.exe to decode Base64 payloads natively.",
    },
    "DESERIALIZATION": {
        "term": "Insecure Deserialization",
        "definition": "A high-severity vulnerability where untrusted, encoded data is converted back into an application object, allowing attackers to execute arbitrary code.",
        "context": "Commonly encountered with Base64-transported Java objects (rO0AB), ASP.NET ViewState (/wEP), and Python Pickles (gASV).",
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
    "CTF": {
        "term": "CTF (Capture The Flag)",
        "definition": "A hands-on, gamified cybersecurity challenge competition where participants reverse-engineer code or investigate artifacts to discover secret proof tokens ('flags').",
        "context": "B64Lab includes 8 progressive CTF challenges with dynamic cryptographic anti-cheat flag generation.",
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
