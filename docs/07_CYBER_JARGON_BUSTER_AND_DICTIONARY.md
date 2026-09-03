# The Cyber Jargon Buster & Master Technical Index

> **From Absolute Zero to Fluency: Every Term, Concept, and Buzzword Explained in Plain English**  
> *Written for absolute beginners, self-taught students, non-technical colleagues, and junior analysts.*

---

## 📖 How to Use This Dictionary

If you are reading cybersecurity tutorials, documentation, or certification material and encounter words that feel like intimidating alphabet soup, look them up here.

Each entry includes:
1. **👶 Explain Like I'm 5 (ELI5):** An everyday real-world analogy with zero confusing jargon.
2. **⚙️ Technical Definition:** The precise computer science and engineering explanation.
3. **🎯 Why It Matters in Cybersecurity:** The practical reason hackers and defenders care about it.

---

## 🗂️ Quick Category Navigation

* [1. Foundational Computer Science & Binary Basics](#1-foundational-computer-science--binary-basics) (Bit, Byte, Octet, Hex, ASCII, UTF-8, UTF-16LE, Radix)
* [2. Base64 & Encoding Mechanics](#2-base64--encoding-mechanics) (Sextet, Padding, Base64URL, Base32, Base85, Data URI, MIME)
* [3. Adversary Tradecraft & Attack Buzzwords](#3-adversary-tradecraft--attack-buzzwords) (Obfuscation, PowerShell `-EncodedCommand`, Malware Dropper, Living-off-the-Land, HTML Smuggling, C2 Beacon, Deserialization)
* [4. Defensive Operations & SOC Terminology](#4-defensive-operations--soc-terminology) (SOC Analyst, SIEM, EDR, Shannon Entropy, Magic Bytes, Forensic Carving, Defanging, CTF)

---

## 1. Foundational Computer Science & Binary Basics

### Bit
* **👶 ELI5:** A microscopic light switch that is either OFF (`0`) or ON (`1`). Everything on every computer is made of these switches.
* **⚙️ Technical:** The smallest unit of digital data, representing a single binary value of `0` or `1`.
* **🎯 Why It Matters in Cyber:** At the hardware and processor level, all security controls, encryption ciphers, and memory exploits manipulate bits.

### Byte / Octet
* **👶 ELI5:** A box that holds exactly 8 bits. It can store a number between `0` and `255`, which is enough to represent a single letter like `'A'`.
* **⚙️ Technical:** A unit of digital storage consisting of 8 consecutive bits. "Octet" is the formal telecommunications term for an 8-bit byte.
* **🎯 Why It Matters in Cyber:** Computer memory, network packets, and malware signatures are measured in bytes. Base64 works by grouping 3 bytes ($3 \times 8 = 24$ bits) at a time.

### Hexadecimal (Hex / Base-16)
* **👶 ELI5:** A shorthand way for humans to read bytes without writing out long strings of eight zeros and ones. It uses digits `0-9` and letters `A-F`.
* **⚙️ Technical:** A base-16 positional numeral system. One hex digit represents 4 bits (a nibble); two hex digits (`0x00` to `0xFF`) represent exactly 1 byte.
* **🎯 Why It Matters in Cyber:** Security analysts read memory dumps, shellcode, and file signatures in Hex (e.g., `4D 5A` for Windows executables).

### ASCII
* **👶 ELI5:** An official lookup dictionary created in the 1960s so computers know that number `65` means capital letter `'A'`, and `66` means `'B'`.
* **⚙️ Technical:** American Standard Code for Information Interchange. A 7-bit character encoding standard defining 128 characters (English letters, digits, punctuation, and control codes).
* **🎯 Why It Matters in Cyber:** Base64 converts raw machine bytes into printable ASCII text so it can safely pass through text-only systems without getting corrupted.

### UTF-8 vs. UTF-16LE
* **👶 ELI5:**
  * **UTF-8:** Uses 1 byte for English letters (`'w'` = `0x77`). It's what the entire internet and Linux use.
  * **UTF-16LE:** Uses 2 bytes for every letter, inserting a blank zero byte after each letter (`'w'` = `0x77 0x00`). It's what Windows uses internally.
* **⚙️ Technical:** UTF-8 is a variable-length encoding (1–4 bytes per code point). UTF-16LE (Little Endian) uses 16-bit code units with the least significant byte stored first.
* **🎯 Why It Matters in Cyber:** Windows PowerShell's `-EncodedCommand` strictly requires UTF-16LE Base64 strings. If a hacker or student encodes as normal UTF-8, PowerShell crashes with a syntax error.

---

## 2. Base64 & Encoding Mechanics

### Base64
* **👶 ELI5:** The "Waterproof Shipping Container" of the internet. It takes any computer file (picture, song, virus) and turns it into safe ordinary letters and numbers (`A-Z`, `a-z`, `0-9`, `+`, `/`) so it can be sent through emails or web forms without breaking.
* **⚙️ Technical:** A binary-to-text radix-64 encoding algorithm (RFC 4648) that groups 24 bits of input into four 6-bit chunks.
* **🎯 Why It Matters in Cyber:** Base64 is the single most common encoding format abused by attackers to conceal payloads and hide in web traffic.

### Sextet
* **👶 ELI5:** A group of 6 bits. It can represent numbers from `0` to `63`.
* **⚙️ Technical:** A 6-bit binary integer ($2^6 = 64$ unique states). Each sextet maps directly to one character in the Base64 alphabet table.
* **🎯 Why It Matters in Cyber:** Base64 reads 3 bytes (24 bits) and slices them into 4 sextets (6 bits each).

### Padding (`=` and `==`)
* **👶 ELI5:** Packing peanuts added to the end of a shipment box when the items don't completely fill the box.
* **⚙️ Technical:** Equal sign (`=`) characters appended to the end of a Base64 string to ensure the final output length is an exact multiple of 4.
* **🎯 Why It Matters in Cyber:** Hackers often strip padding characters from their payloads to bypass antivirus rules that look for `=` at the end.

### Base64URL
* **👶 ELI5:** A web-safe twin of Base64 that swaps out characters that could break internet website links (it changes `+` to `-` and `/` to `_`).
* **⚙️ Technical:** RFC 4648 Section 5 URL and Filename Safe Alphabet. Avoids percent-encoding in HTTP headers and JSON Web Tokens (JWTs).
* **🎯 Why It Matters in Cyber:** Modern web authentication tokens (JWTs) and API keys use Base64URL.

### Data URI
* **👶 ELI5:** Embedding an entire file (like an image or program) directly inside a line of HTML code, formatted as `data:image/png;base64,...`.
* **⚙️ Technical:** RFC 2397 specification allowing web authors to inline media rather than linking to external files.
* **🎯 Why It Matters in Cyber:** Attackers use Data URIs in phishing emails so fake login logos load without being blocked, and in HTML Smuggling to deliver malware.

---

## 3. Adversary Tradecraft & Attack Buzzwords

### Obfuscation
* **👶 ELI5:** Digital camouflage. Making code look like a chaotic mess of gibberish so security scanners can't tell what it does, but the computer can still run it.
* **⚙️ Technical:** The transformation of source or binary code to make it resistant to human comprehension and static pattern-matching engines while preserving its execution semantics.
* **🎯 Why It Matters in Cyber:** Classified under MITRE ATT&CK technique **T1027**. Attackers obfuscate code with Base64, compression, and variable randomization.

### De-obfuscation
* **👶 ELI5:** Stripping off the camouflage. Peeling back the layers of gibberish until the original, human-readable malicious command is revealed.
* **⚙️ Technical:** The analytical process of decoding, decompressing, and unmasking layered payloads to reconstruct the adversary's original intent.
* **🎯 Why It Matters in Cyber:** A primary daily task of Tier 2/3 SOC Analysts and incident response investigators.

### PowerShell `-EncodedCommand`
* **👶 ELI5:** A built-in Windows trick that lets you give PowerShell a scrambled Base64 string instead of normal typing. PowerShell quietly unscrambles it and runs it immediately.
* **⚙️ Technical:** A CLI parameter (`-e`, `-enc`, `-EncodedCommand`) in `powershell.exe` that accepts a Base64-encoded UTF-16LE command string.
* **🎯 Why It Matters in Cyber:** Classified under MITRE ATT&CK **T1059.001**. It is the #1 most common technique used in fileless Windows malware attacks.

### Malware Dropper / Stager
* **👶 ELI5:** A Trojan horse. A tiny, harmless-looking starter program whose only job is to sneak onto your computer, unwrap a compressed virus hidden inside it, and launch it.
* **⚙️ Technical:** A preliminary stage payload designed to establish a foothold, decompress an embedded secondary executable from memory, and execute it using API calls like `VirtualAlloc` and `CreateThread`.
* **🎯 Why It Matters in Cyber:** Modern ransomware rarely arrives as a raw `.exe`. It arrives as a multi-stage dropper that chains Base64 and GZIP compression.

### Living-off-the-Land (LotL / LOLBins)
* **👶 ELI5:** A burglar who breaks into a house and uses the homeowner's own kitchen knives and tools instead of bringing their own crowbar.
* **⚙️ Technical:** Cyberattackers using legitimate, pre-installed operating system binaries (e.g., `powershell.exe`, `certutil.exe`, `wmic.exe`, `curl.exe`) to execute attacks without downloading foreign hacking tools.
* **🎯 Why It Matters in Cyber:** Antivirus software trusts built-in Windows tools, making LotL attacks extremely difficult to detect.

### HTML Smuggling
* **👶 ELI5:** Sneaking a disassembled bicycle into a building piece-by-piece inside innocent-looking letters, and having the recipient's web browser assemble the bicycle and drop it into their downloads folder without the front-door security guard noticing.
* **⚙️ Technical:** MITRE ATT&CK **T1027.006**. Using HTML5 and JavaScript features (`Blob`, `atob()`, `URL.createObjectURL`) to assemble malicious binaries client-side from Base64 strings, bypassing network perimeter email gateways and firewalls.
* **🎯 Why It Matters in Cyber:** A favorite delivery mechanism of APT state-sponsored groups and commodity ransomware cartels (QakBot, Nobelium).

### C2 Beacon (Command and Control)
* **👶 ELI5:** A walkie-talkie signal. The infected computer quietly sends periodic "I'm alive, what do you want me to do next?" messages back to the hacker's secret server.
* **⚙️ Technical:** Covert periodic HTTP/DNS/TCP communication transmitted by an implant to an adversary-controlled server to request tasks and exfiltrate data.
* **🎯 Why It Matters in Cyber:** B64Lab simulates carving Base64 tokens from network logs to detect active C2 beacon communication.

---

## 4. Defensive Operations & SOC Terminology

### SOC Analyst (Security Operations Center)
* **👶 ELI5:** The cybersecurity "guard at the security monitors." A professional who watches live alarms, investigates suspicious computer activity, and stops hackers before they cause damage.
* **⚙️ Technical:** Front-line defensive engineers responsible for monitoring organizational telemetry, triaging alerts, and responding to cyber incidents.
* **🎯 Why It Matters in Cyber:** B64Lab is specifically engineered to train students to pass SOC certification exams (Sec+, CySA+, BTL1) and perform real-world triage.

### SIEM (Security Information & Event Management)
* **👶 ELI5:** A giant search engine for cybersecurity. It collects millions of log messages from every computer, server, and firewall in a company and alerts analysts when something looks weird.
* **⚙️ Technical:** Centralized security software (e.g., Splunk, Microsoft Sentinel, Elastic SIEM) that ingests, indexes, and correlates log data for real-time alerting and historical investigation.
* **🎯 Why It Matters in Cyber:** B64Lab outputs directly to JSON Lines (`.jsonl`) and CSV so its findings can be imported straight into corporate SIEMs.

### Shannon Entropy
* **👶 ELI5:** The "Randomness Meter." Normal English words have low randomness (~3.5). Base64 text has medium randomness (~5.5). Encrypted passwords and secret military codes have maximum randomness (~7.8).
* **⚙️ Technical:** A mathematical formula ($H(X) = -\sum P(x) \log_2 P(x)$) measuring information density and unpredictability, spanning from $0.0$ to $8.0$ bits per byte.
* **🎯 Why It Matters in Cyber:** Base64 strings almost always score between **5.10 and 5.95**. SOC analysts use this mathematical threshold to automatically spot hidden malicious payloads in noisy logs.

### Magic Bytes (File Signatures)
* **👶 ELI5:** A file's digital fingerprint or DNA. Even if a hacker renames a virus from `malware.exe` to `family_photo.png`, the very first bytes inside the file still say `MZ` (which means "I am actually a Windows program!").
* **⚙️ Technical:** Fixed unique byte sequences located at offset 0 of a file header that identify its true file format regardless of file extension.
  * `4D 5A` (`MZ` in ASCII) $\rightarrow$ Windows Executable (.exe)
  * `7F 45 4C 46` (`\x7fELF`) $\rightarrow$ Linux Executable (.elf)
  * `25 50 44 46` (`%PDF-`) $\rightarrow$ Adobe Document (.pdf)
  * `50 4B 03 04` (`PK\x03\x04`) $\rightarrow$ ZIP Archive (.zip, .docx)
* **🎯 Why It Matters in Cyber:** B64Lab decodes mystery Base64 strings and immediately checks magic bytes to tell defenders what kind of file was hidden.

### Forensic Artifact Carving
* **👶 ELI5:** Looking through a giant dumpster of shredded documents and extracting only the secret love letters or bank statements without needing to know who threw them away.
* **⚙️ Technical:** Extracting raw data structures, files, and encoded payloads from unstructured memory dumps, disk images, or log files based on byte patterns rather than file system tables.
* **🎯 Why It Matters in Cyber:** B64Lab's `carve` command scrapes 50 MB messy web logs and extracts every embedded Base64 payload in seconds.

### Defanging
* **👶 ELI5:** Putting a plastic safety cap on a syringe before passing it to a colleague.
* **⚙️ Technical:** The practice of modifying malicious indicators (URLs, IPs, domain names) so they cannot be accidentally clicked or executed in reports.
  * `http://malicious.com` $\rightarrow$ `hxxp://malicious[.]com`
* **🎯 Why It Matters in Cyber:** Prevents analysts and students from accidentally triggering malware or infecting their own machines while learning.

### CTF (Capture The Flag)
* **👶 ELI5:** A cybersecurity puzzle competition or game where you solve hacking and defense challenges to find a secret password (called a "flag") that proves you solved it.
* **⚙️ Technical:** Hands-on gamified cybersecurity exercises where participants analyze artifacts, reverse-engineer code, or exploit vulnerabilities to uncover secret tokens (`FLAG{...}`).
* **🎯 Why It Matters in Cyber:** B64Lab includes 8 progressive CTF challenges with dynamic anti-cheat flag synthesis to test real skills.
