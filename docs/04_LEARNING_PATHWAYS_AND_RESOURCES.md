# Learning Pathways & Curated Cybersecurity Resources

> **Verified Reputable Sources: Canonical RFCs, Industry Standards & Video Lectures**  
> *Target Audience: Students, Self-Taught Hackers, SOC Analysts, and Certification Candidates*

---

## 1. Authoritative Industry Standards & Specifications

Always refer to the official specifications used by security engineers worldwide:

* **[IETF RFC 4648 - The Base16, Base32, and Base64 Data Encodings](https://datatracker.ietf.org/doc/html/rfc4648)**
  * *The definitive IETF specification:* Defines the 64-char standard alphabet (Section 4), the URL-safe alphabet (Section 5), Base32 (Section 6), and padding rules (Section 4.3).
* **[MDN Web Docs: Base64 Glossary & Technical Guide](https://developer.mozilla.org/en-US/docs/Glossary/Base64)**
  * *Mozilla Developer Network:* Clear explanations of binary-to-text conversion, character sets, and DOM APIs (`btoa()` and `atob()`).
* **[IETF RFC 2045 - Multipurpose Internet Mail Extensions (MIME)](https://datatracker.ietf.org/doc/html/rfc2045)**
  * *Historical origin:* Section 6.8 details why Base64 was standardized to transport attachments over 7-bit SMTP email gateways.
* **[Cloudflare Learning Center: What is a JSON Web Token (JWT)?](https://www.cloudflare.com/learning/access-management/what-is-json-web-token/)**
  * *Modern Web Security:* Explains how JWTs serialize authentication tokens into three Base64URL-encoded segments.
* **[OWASP Foundation: REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/)**
  * *Application Security:* Guidance on validating and sanitizing encoded payloads before decoding to avoid deserialization exploits.

---

## 2. Curated High-Yield Video Lectures (Search Paths)

Direct video IDs often break or get removed over time. Use these direct canonical search queries to access the verified lectures from trusted educators:

### 1. Computer Science & Bitwise Fundamentals
* **[Computerphile: "Base64" Channel Search](https://www.youtube.com/results?search_query=Computerphile+Base64)**
  * *Recommended Video:* *"Base64 (and why 64?)"* featuring Dr. Mike Pound from the University of Nottingham.
  * *Core Concept:* Visual paper breakdown of 3 bytes of 8 bits mapping into 4 characters of 6 bits.
* **[Ben Eater: Binary, Hexadecimal, and Data Representations](https://www.youtube.com/results?search_query=Ben+Eater+Binary)**
  * *Recommended Content:* High-yield visual computer architecture series explaining how bits, registers, and binary logic work from first principles.

### 2. Real-World Malware De-Obfuscation
* **[John Hammond: "PowerShell EncodedCommand" Search](https://www.youtube.com/results?search_query=John+Hammond+PowerShell+EncodedCommand)**
  * *Recommended Content:* Live incident walkthroughs analyzing obfuscated `-EncodedCommand` droppers, UTF-16LE decoding, and fileless malware.
* **[LiveOverflow: "Encoding vs Encryption" Search](https://www.youtube.com/results?search_query=LiveOverflow+Encoding+vs+Encryption)**
  * *Recommended Content:* Clarifies why Base64 is an encoding format rather than encryption, and how CTF challenges use it.

---

## 3. Classic Industry Tool References

* **[GCHQ CyberChef](https://gchq.github.io/CyberChef/):** The legendary web-based decoding and forensic pipeline created by the UK Government Communications Headquarters.
* **[Didier Stevens' Security Blog: base64dump.py](https://blog.didierstevens.com/):** Technical articles by malware researcher Didier Stevens on carving and extracting Base64 from malicious documents and PCAPs.
* **[SANS Internet Storm Center](https://isc.sans.edu/):** Real-time threat diaries detailing active malware campaigns utilizing encoded commands.

---

## 4. Certification Alignment Roadmap

| Certification | Exam Objective | How B64Lab Prepares You |
| :--- | :--- | :--- |
| **CompTIA Security+ (SY0-701)** | 2.4: Cryptographic concepts | Module 1 explains encoding vs hashing vs encryption. |
| **CompTIA CySA+ (CS0-003)** | 1.3: Threat hunting & log analysis | Blue Lane carves Base64 from noisy web & Sysmon logs. |
| **Blue Team Level 1 (BTL1)** | Digital Forensics & SIEM triage | Shannon Entropy scoring, Magic Byte detection (`MZ`, `ELF`). |
| **OSCP / PNPT** | Evasion & Living-off-the-Land | Red Lane crafts valid UTF-16LE PowerShell droppers. |
