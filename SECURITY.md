# Security Policy

## ️ Responsible Disclosure

** Veruthia Consulting LLC** takes the security of our software and educational tools seriously. If you discover a potential vulnerability in B64Lab, we appreciate your cooperation in disclosing it responsibly.

### Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

---

## Reporting a Vulnerability

Please **do not** open public GitHub issues for security-sensitive bugs or potential exploits.

Instead, please report security issues through:
1. **GitHub Security Advisories:** Use the private reporting feature under **Security $\rightarrow$ Report a vulnerability** on the repository page.
2. **Email:** Contact `veruthiaoperations-cloud@users.noreply.github.com`.

Please include:
* Detailed steps to reproduce the issue.
* Sample input data (defanged).
* Affected platform/Python version.

We will acknowledge receipt within 48 hours and coordinate remediation.

---

## Antivirus & EDR False Positive Guidance

Because **B64Lab** is a dedicated cybersecurity engineering, forensic triage, and adversary emulation lab, it contains educational test fixtures that demonstrate techniques such as:
- PowerShell `-EncodedCommand` UTF-16LE formatting
- Recursive archive and GZIP stream de-obfuscation
- Magic byte identification (e.g. PE, ELF, PDF file signatures)

### Why Scanners May Alert (False Flags)
Commercial endpoint protection products (Bitdefender, Windows Defender, CrowdStrike, SentinelOne) utilize static heuristic scanners that search for strings such as `powershell.exe -EncodedCommand` or fileless memory decompression stubs. When these signatures are encountered in sample files or test fixtures, security software may generate a **heuristic false positive** (e.g. `Trojan.PowerShell.Generic` or `Heur.Bzc`).

### Safety Verification & Defanging Architecture
1. **Zero External Dependencies:** B64Lab uses exclusively Python standard library modules (`base64`, `gzip`, `zlib`, `sqlite3`, `re`, `argparse`).
2. **Zero Malicious Payloads:** No live exploits, compiled shellcode, backdoors, or command-and-control (C2) agents are bundled.
3. **Completely Defanged:** Sample artifacts in `samples/` are purely static text strings representing benign diagnostic scripts (`Write-Host`) designed for forensic extraction practice.
4. **No Network Beaconing:** B64Lab never opens outbound socket connections or calls external servers.

If your endpoint scanner flags a sample file, you may safely add a local folder exclusion or report the false positive to your security vendor.
