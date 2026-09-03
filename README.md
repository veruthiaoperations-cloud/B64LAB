# B64Lab: The Cyber Base64 Simulator, Academy & Triage Engine

> *An authoritative open-source security engineering & forensic simulation project by **Veruthia Consulting LLC**.*

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ██████╗  ██████╗ ██╗  ██╗ ██╗       █████╗  ██████╗                          ║
║ ██╔══██╗██╔════╝ ██║  ██║ ██║      ██╔══██╗ ██╔══██╗ [ ZERO-DEPENDENCY ]     ║
║ ██████╔╝███████╗ ███████║ ██║      ███████║ ██████╔╝ [ RFC 4648 SPEC ]       ║
║ ██╔══██╗██╔═══██╗╚════██║ ██║      ██╔══██║ ██╔══██╗ [ BITWISE & CTF ]       ║
║ ██████╔╝╚██████╔╝     ██║ ███████╗ ██║  ██║ ██████╔╝ [ FORENSIC LAB ]        ║
║ ╚═════╝  ╚═════╝      ╚═╝ ╚══════╝ ╚═╝  ╚═╝ ╚═════╝  v1.0.0 (SEC-STD)        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

[![Language](https://img.shields.io/badge/Language-Pure%20Python%203-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Library)-brightgreen.svg)]()
[![Standards](https://img.shields.io/badge/Standard-RFC%204648-orange.svg)](https://datatracker.ietf.org/doc/html/rfc4648)
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-T1027%20%7C%20T1059-red.svg)](https://attack.mitre.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

> **"Anyone should be able to sit down knowing nothing about Base64 and walk away understanding it at an assembly/bitwise and SOC-analyst level."**

** B64Lab** is a zero-dependency, air-gapped cybersecurity simulation workbench, educational academy, and forensic triage engine. It bridges the gap between low-level computer science theory (octets, sextets, bit-shifting, Shannon entropy) and real-world adversary tradecraft (PowerShell UTF-16LE droppers, multi-stage nesting, magic-byte carving, custom alphabet evasion).

---

## Executive Overview: Plain English Breakdown

If you are new to technology or cybersecurity, the technical specifications can sound intimidating. Here is what this project is actually about in simple everyday terms:

### The Problem
* The internet was originally designed to carry **plain text** (letters and numbers). If you attempt to transmit raw computer files (such as executables, images, or compressed archives) across text-only channels, the data corrupts or breaks.
* **Base64 is the "Waterproof Shipping Container" of the internet:** It translates any computer file into safe, ordinary letters and numbers (`A-Z`, `a-z`, `0-9`) so it can travel anywhere across the web without breaking.

### The Cybersecurity Cat-and-Mouse Game
1. **The Attackers (Red Team):** Adversaries abuse Base64 to conceal malicious code inside ordinary-looking text. To traditional perimeter filters, it resembles harmless text strings, allowing payloads to bypass inspection.
2. **The Defenders (Blue Team / SOC Analysts):** Defensive analysts inspect thousands of log events and network streams daily, detect encoded payloads, de-obfuscate them, and determine the attacker's intent.

### What B64Lab Delivers
**B64Lab** functions as both an **educational laboratory** and an **automated operational utility**:
* **The Educational Laboratory (Academy & CTF Labs):** Guides learners from first principles through binary bit manipulation, PowerShell nuances, and obfuscation techniques using interactive Capture The Flag challenges.
* **The Operational Utility (Forensic Triage Engine):** Scans multi-megabyte log files in milliseconds, calculates Shannon entropy, identifies disguised executables, and exports structured CSV/JSON/SQLite databases for enterprise incident response.

> **New to technical terminology?** Explore [**The Cyber Jargon Buster & Master Technical Index** (`docs/07_CYBER_JARGON_BUSTER_AND_DICTIONARY.md`)](docs/07_CYBER_JARGON_BUSTER_AND_DICTIONARY.md) for clear, non-technical definitions of every concept.

---

## Why B64Lab Was Built: The Mission & The Gap

During cybersecurity certification training (Security+, CySA+, BTL1, OSCP), students repeatedly encounter Base64 in JWT tokens, phishing attachments, PowerShell `-EncodedCommand` invocations, and malware droppers. 

Yet traditional resources only teach:
```python
import base64
print(base64.b64decode("SGV5"))
```
In enterprise operations, you encounter **50 MB noisy web logs**, **PowerShell UTF-16LE null-byte gotchas**, **multi-stage GZIP droppers**, and **evasive stripped-padding attacks**.

### The Tool Landscape: What Existed vs. The Gap Filled

*** GCHQ CyberChef:** The Swiss-Army knife of decoding, but it is a generic browser utility. It doesn't teach cybersecurity, offers zero offensive/defensive lab simulations, and won't automate log triage.
*** Didier Stevens' `base64dump.py`:** A legendary CLI carver, but a barebones script with cryptic parameters and zero educational curriculum.
*** Ciphey:** Automated heuristic decryption, but general-purpose cryptography with heavy third-party ML dependencies.

| Feature / Capability | GCHQ CyberChef | Didier Stevens `base64dump.py` | Ciphey | **B64Lab** |
| :--- | :---: | :---: | :---: | :---: |
| **Air-Gapped CLI (No Browser Required)** |  |  |  | ** (Pure Stdlib)** |
| **Zero Third-Party Dependencies** |  (Web) |  (Python) |  (Many wheels) | ** (100% Built-in)** |
| **0-to-100 Interactive Academy** |  |  |  | ** (Built-in Modules)** |
| **Visual 24-Bit Bitwise Step-Through** |  |  |  | ** (Interactive Tracer)** |
| **PowerShell UTF-16LE Subsystem** |  (Manual) |  |  | ** (Auto-Detect & Craft)** |
| **Shannon Entropy Threat Meter** | Manual Recipe |  | Partial | ** (Colorized Meter)** |
| **Magic Byte Signature Identification** | Manual Recipe |  |  | ** (PE/ELF/PDF/ZIP/GZ)** |
| **Recursive Multi-Stage Dropper Unpacker** | Manual Recipe |  | Partial | ** (Recursive Engine)** |
| **Adversary Payload Forge & Evasion** |  |  |  | ** (Red Team Lane)** |
| **Dynamic Anti-Cheat CTF Challenge Arena**|  |  |  | ** (HMAC-SHA256)** |

---

## Multi-Modal Learning Architecture

People learn through different sensory and cognitive pathways. B64Lab adapts to all four:
1. **Kinesthetic Learners (Doing):** Launch the terminal CLI, forge custom payloads, carve raw logs, and solve 8 dynamic CTF labs.
2. **Visual Learners (Seeing):** Trace real-time 24-bit binary regroupings, view canonical syntax-highlighted hex dumps, and experience dynamic lane themes (**Amber CRT**, **Neon Ice Blue**, **Tactical Crimson**).
3. **Analytical Learners (Reading):** Study in-depth technical guides with CPU-level bit-shifts, padding proofs, and MITRE ATT&CK mappings in `docs/`.
4. **Auditory & External Learners (Watching):** Access curated video lectures (Computerphile, John Hammond, LiveOverflow) and canonical RFC standards in [docs/04_LEARNING_PATHWAYS_AND_RESOURCES.md](docs/04_LEARNING_PATHWAYS_AND_RESOURCES.md).

---

## Key Architectural Highlights

*** Zero Dependencies (Air-Gapped Ready):** Built **100% on the Python Standard Library**. No `npm`, no `pip`, no external wheels. Runs cleanly on isolated forensic workstations, restricted jumpboxes, and air-gapped networks.
*** Hand-Crafted ANSI/VT100 Terminal UI:** Nostalgic 80s IBM/BBS terminal experience with custom Unicode box-drawing, canonical hex dumping, and dynamic theme switching.
*** Dynamic Simulation Lanes:**
  *  **Amber CRT (Default):** 80s Cyberpunk warm phosphor for Theory, Academy, and CTF Challenges.
  *  **Neon Ice Blue (Defensive Lane):** Cold, analytical forensic interface for artifact carving, entropy scoring, and magic-byte hunting.
  *  **Tactical Crimson (Offensive Lane):** Adversary simulation interface for crafting UTF-16LE scripts, multi-stage droppers, and custom alphabet ciphers.
*** 0-to-100 Educational Depth:** Interactive visual lessons breaking down binary bit manipulation step-by-step.
*** Built-in CTF Arena:** 8 progressive offline forensic de-obfuscation challenges with automated flag verification.

---

## Quickstart & Setup

Clone the repository and run—no installation, compilers, or third-party packages required:

```bash
# Clone the repository
git clone https://github.com/veruthiaoperations-cloud/B64LAB.git
cd B64LAB

# Launch interactive terminal environment
python b64lab.py
```

>  **Need OS-specific guidance, air-gapped jumpbox instructions, or Docker one-liners?**  
> See the complete [**SETUP.md**](SETUP.md) deployment guide.

You can also run B64Lab directly as a Python module:
```bash
python -m b64lab
```

### Headless / CLI Scripting Pipeline
B64Lab also functions as a fast command-line triage utility for automation scripts:

```bash
# Encode or decode
python b64lab.py encode "Security Operations Center"
python b64lab.py decode "U2VjdXJpdHkgT3BlcmF0aW9ucyBDZW50ZXI="

# De-obfuscate PowerShell UTF-16LE command lines
python b64lab.py decode "dwBoAG8AYQBtAGkA" --utf16

# View real-time visual bitwise breakdown (3 bytes -> 4 chars)
python b64lab.py trace "Man"

# Calculate Shannon Entropy and anomaly rating
python b64lab.py entropy "TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAA"

# Carve all embedded Base64 payloads from a log file (Interactive Table)
python b64lab.py carve samples/sample_web_access.log

# Export carved artifacts directly to Excel-ready CSV
python b64lab.py carve samples/sample_web_access.log --format csv -o triage_report.csv

# Export carved artifacts to JSON Lines for Splunk / Elastic SIEM ingestion
python b64lab.py carve samples/sample_web_access.log --format json -o siem_events.jsonl

# Export carved artifacts to an indexed SQLite database for SQL analysis
python b64lab.py carve samples/sample_web_access.log --format sqlite -o forensic_triage.db

# Unix STDIN Streaming Pipeline (Low latency, constant memory)
cat /var/log/nginx/access.log | python b64lab.py carve - --format csv > live_triage.csv
```

---

## ️ Project Architecture

```
B64Lab/
├── b64lab.py                     # Single zero-install root executable launcher
├── b64lab/
│   ├── __init__.py               # Package metadata
│   ├── __main__.py               # Module entry point (python -m b64lab)
│   ├── cli.py                    # Master CLI parser & start menu loop
│   ├── workbench.py              # Multi-format encoder, decoder & hex viewer
│   ├── settings.py               # Theme customizer (Amber, Ice Blue, Red, Phosphor)
│   ├── core/                     # Pure Bitwise & Forensic Engines
│   │   ├── bitwise.py            # Pure bit-shift/masking engine with visual trace
│   │   ├── alphabets.py          # RFC 4648 specs & custom threat actor tables
│   │   ├── entropy.py            # Shannon entropy calculation H(X)
│   │   ├── signatures.py         # Magic byte database (PE, ELF, PDF, ZIP, GZIP)
│   │   └── unpacker.py           # Recursive multi-stage de-obfuscator
│   ├── ui/                       # Hand-Crafted ANSI Terminal Engine
│   │   ├── ansi.py               # ANSI codes, TrueColor, Windows VT-100 enabler
│   │   ├── themes.py             # Dynamic lane color palettes & switching
│   │   ├── components.py         # Box drawing, headers, tables, aligned badges
│   │   └── hexdump.py            # Canonical forensic hex dump renderer
│   ├── academy/                  # 0-to-100 Educational Modules
│   │   ├── bitwise_lesson.py     # Octets -> 24-bit buffer -> Sextets -> Padding
│   │   ├── rfc_lesson.py         # RFC 4648 (Base64, Base64URL, Base32, Hex)
│   │   ├── offensive_lesson.py   # Adversary tradecraft, droppers, evasion
│   │   ├── defensive_lesson.py   # SOC triage, entropy hunting, file carving
│   │   ├── glossary.py           # Searchable cybersecurity terminology database
│   │   └── mitre.py              # MITRE ATT&CK technique reference
│   ├── triage/                   # Defensive / Blue Team Lane (Ice Blue)
│   │   ├── carver.py             # Stream & log carver with entropy filter
│   │   └── analyzer.py           # Forensic report generator & payload exporter
│   ├── forge/                    # Offensive / Red Team Lane (Crimson Red)
│   │   ├── powershell.py         # UTF-16LE -EncodedCommand generator
│   │   ├── dropper.py            # Recursive GZIP/ZLIB multi-stage builder
│   │   ├── evasion.py            # Custom alphabet scrambler & padding stripper
│   │   ├── mock_logs.py          # Synthetic web access and Sysmon log generator
│   │   └── console.py            # Offensive simulation console
│   └── ctf/                      # Hands-on CTF Arena
│       └── engine.py             # 8 progressive forensic labs with flag scoring
├── tests/
│   └── test_suite.py             # Automated unit tests (python -m unittest)
├── samples/                      # Safe defanged mock logs & scripts for triage
├── LICENSE                       # MIT License
└── README.md
```

---

## Deep-Dive: Cybersecurity Theory & Mechanics

### 1. The 24-bit Bitwise Transformation
Base64 expands binary data by **33.3%** because computers group bytes into 8-bit octets, whereas Base64 groups them into 6-bit sextets ($2^6 = 64$ printable symbols):

```
Text Input   :  'M'           'a'           'n'
Hex Values   :   0x4D          0x61          0x6E
Binary Octets:   01001101      01100001      01101110
                 ──────────────────────────────────────────
24-bit Buffer:   0 1 0 0 1 1 0 1 0 1 1 0 0 0 0 1 0 1 1 0 1 1 1 0
                 ──────────────────────────────────────────
6-bit Sextets:   010011     010110     000101     101110
Decimal Index:     19         22          5         46
Lookup Char  :    'T'        'W'        'F'        'u'   ==> "TWFu"
```

### 2. Why '=' and '==' Padding Exist (The Math)
When input bytes do not divide cleanly by 3:
*** Remainder = 1 byte (8 bits):** 4 zero bits padded $\rightarrow$ 2 sextets $\rightarrow$ Appends **`==`** (e.g. `'A'` $\rightarrow$ `'QQ=='`).
*** Remainder = 2 bytes (16 bits):** 2 zero bits padded $\rightarrow$ 3 sextets $\rightarrow$ Appends **`=`** (e.g. `'AB'` $\rightarrow$ `'QUI='`).
*** Remainder = 0 bytes (24 bits):** Clean mapping $\rightarrow$ **No padding required**.

> **Adversary Note:** Threat actors frequently strip `=` padding to break naive IDS regex signatures that search exclusively for `^[A-Za-z0-9+/]{4}*={0,2}$`. B64Lab's carver automatically detects and normalizes unpadded sequences.

### 3. The PowerShell UTF-16LE Architecture Gotcha
Windows PowerShell's `-EncodedCommand` switch requires **UTF-16LE** (Little Endian) bytes:
* Command: `whoami`
* UTF-8 Bytes: `77 68 6f 61 6d 69` $\rightarrow$ Base64: `d2hvYW1p`  *(Fails in PowerShell)*
* UTF-16LE Bytes: `77 00 68 00 6f 00 61 00 6d 00 69 00` $\rightarrow$ Base64: `dwBoAG8AYQBtAGkA`  *(Executes)*

### 4. Shannon Entropy as an Anomaly Detection Metric
Shannon Entropy measures randomness on a scale from $0.00$ to $8.00$:
$$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

| Entropy Score | Threat Level | Typical Classification |
| :--- | :--- | :--- |
| **0.00 - 3.50** | `LOW` | Repetitive buffers, null bytes, padding |
| **3.50 - 4.80** | `LOW` | Plaintext English, standard script code, JSON, XML |
| **5.10 - 5.95** | `SUSPICIOUS` | **Base64 / Base32 Encoded Blobs** (Narrow distribution band) |
| **6.00 - 7.00** | `HIGH` | Compressed data (GZIP, ZIP), compiled bytecode |
| **7.20 - 8.00** | `CRITICAL` | Cryptographic ciphertext, packed malware shellcode |

---

## Built-In CTF Challenges (Anti-Cheat Powered)

B64Lab features a **dynamic HMAC-SHA256 anti-cheat challenge engine**. **Zero static flags exist in the source code.** Every challenge dynamically synthesizes unique session flags and payloads derived from a local cryptographic salt. Flags cannot be looked up on Google, copied from friends, or found by grepping the repository!

*** Level 1 (First Contact):** Standard token extraction from HTTP headers.
*** Level 2 (The Broken Pad):** Repairing stripped padding on an evasion payload.
*** Level 3 (The Ghost Shell):** De-obfuscating PowerShell UTF-16LE Windows Event logs.
*** Level 4 (Needle in the Haystack):** Carving Base64 payloads out of raw web access logs.
*** Level 5 (Magic Masquerade):** Identifying disguised executables via magic bytes (`MZ`).
*** Level 6 (The Russian Doll):** Multi-stage unpacking (Base64 $\rightarrow$ GZIP $\rightarrow$ Payload).
*** Level 7 (The Shifted Table):** Reversing a custom threat-actor alphabet substitution cipher.
*** Level 8 (Incident Response Final):** Triage an active C2 DNS-tunneling beacon.

---

## Comprehensive Documentation Suite & Educational Lab

Explore the complete visual curriculum, cheat sheets, and architectural guides in `docs/`:
* [**Start Here: The 0-to-100 Curriculum Roadmap** (`docs/00_START_HERE_CURRICULUM.md`)](docs/00_START_HERE_CURRICULUM.md) — Ground-floor guide covering bits, bytes, and step-by-step guidance on how to maximize your learning.
* [**The Cyber Jargon Buster & Master Technical Index** (`docs/07_CYBER_JARGON_BUSTER_AND_DICTIONARY.md`)](docs/07_CYBER_JARGON_BUSTER_AND_DICTIONARY.md) — Plain English (ELI5) definitions of every technical term, acronym, and buzzword from Bit to SIEM.
* [**Complete Schema Cheat Sheet & Visualizer** (`docs/05_BASE64_CHEAT_SHEET_AND_VISUALIZER.md`)](docs/05_BASE64_CHEAT_SHEET_AND_VISUALIZER.md) — The full 64-character lookup grid (0–63), worked `"Hello"` step-by-step encoding/decoding, and padding visualizer.
* [**The Mission & The Gap** (`docs/00_WHY_B64LAB_EXISTS.md`)](docs/00_WHY_B64LAB_EXISTS.md) — The student origin story, competitive landscape analysis (CyberChef, base64dump, Ciphey), and multi-modal pedagogy.
* ️ [**Module 1: Low-Level Bitwise Architecture** (`docs/01_BITWISE_ARCHITECTURE.md`)](docs/01_BITWISE_ARCHITECTURE.md) — 24-bit shift buffers, octet-to-sextet regrouping, CPU bit-shifts, and mathematical padding proofs.
* [**Module 2: Adversary Tradecraft & Malware Obfuscation** (`docs/02_MALWARE_OBFUSCATION.md`)](docs/02_MALWARE_OBFUSCATION.md) — PowerShell UTF-16LE vs. UTF-8 sequence diagrams, multi-stage dropper pipelines, and APT custom alphabets.
* ️ [**Module 3: Defensive Triage & Forensic Carving** (`docs/03_SOC_TRIAGE_FORENSICS.md`)](docs/03_SOC_TRIAGE_FORENSICS.md) — Shannon Entropy mathematical formulas, magic byte carving catalogs, and SIEM/EDR log hunting protocols.
* [**Module 4: Study Pathways & Curated Resources** (`docs/04_LEARNING_PATHWAYS_AND_RESOURCES.md`)](docs/04_LEARNING_PATHWAYS_AND_RESOURCES.md) — Curated video lectures (Computerphile, John Hammond, LiveOverflow), canonical RFC standards, and certification alignment roadmaps (Security+, CySA+, BTL1, OSCP).
* [**Module 5: Data URIs, HTML Smuggling & Web Exploitation** (`docs/06_DATA_URIS_HTML_SMUGGLING_AND_VARIANTS.md`)](docs/06_DATA_URIS_HTML_SMUGGLING_AND_VARIANTS.md) — RFC 2397 Data URIs, HTML Smuggling (T1027.006), MIME spoofing detection, and Java/ViewState deserialization gadgets.

---

## ️ MITRE ATT&CK Mapping

| ID | Technique Name | Tactic | B64Lab Simulation / Detection |
| :--- | :--- | :--- | :--- |
| **T1027** | Obfuscated Files or Information | Defense Evasion | Multi-stage unpacker & entropy scoring |
| **T1027.006** | HTML Smuggling | Defense Evasion | Data URI parser & MIME mismatch detection |
| **T1059.001** | PowerShell Scripting Interpreter | Execution | UTF-16LE generator and Event 4104 carver |
| **T1132.001** | Standard Cryptographic Data Encoding | Command & Control | Carving embedded Base64 from web headers |
| **T1071.004** | DNS Protocol: DNS Tunneling | Command & Control | Base32 exfiltration laboratory simulation |

---

## Running Automated Tests

Run the full automated test suite using Python's built-in `unittest` runner:

```bash
python -m unittest tests/test_suite.py -v
```

All tests pass out of the box with zero external dependencies.

---

## License, Governance & Legal

This project is licensed under the [MIT License](LICENSE) — Copyright (c) 2026 **Veruthia Consulting LLC**.

* ️ **Legal Disclaimer & Limitation of Liability:** See [DISCLAIMER.md](DISCLAIMER.md)
* ️ **Security Policy & Vulnerability Reporting:** See [SECURITY.md](SECURITY.md)
* ️ **Project Governance & Contribution Guidelines:** See [CONTRIBUTING.md](CONTRIBUTING.md)
* **Installation & Air-Gapped Setup:** See [SETUP.md](SETUP.md)
