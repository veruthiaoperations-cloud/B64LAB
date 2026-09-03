# B64Lab Installation & Operational Setup Guide

> **Zero-Dependency, Cross-Platform Deployment for Windows, Linux, macOS, and Air-Gapped Systems**

---

## ⚡ 1. System Requirements

* **Python Version:** Python 3.8 or newer (3.8, 3.9, 3.10, 3.11, 3.12+ supported).
* **Operating Systems:**
  * Windows 10 / Windows 11 / Windows Server (PowerShell, CMD, Windows Terminal)
  * Linux (Ubuntu, Debian, Fedora, Arch, Alpine, Kali, REMnux, SIFT)
  * macOS (Terminal, iTerm2)
* **Hardware:** Any hardware capable of running Python (~20 MB RAM footprint).
* **Dependencies:** **Zero external packages.** No `pip install`, no `requirements.txt`, no `npm`, no C compilers.

---

## 🚀 2. Quickstart (Clone & Run)

```bash
# 1. Clone repository
git clone https://github.com/veruthiaoperations-cloud/B64LAB.git
cd B64LAB

# 2. Run immediately using Python
python b64lab.py
```

You can also run B64Lab directly as a Python module:
```bash
python -m b64lab
```

---

## 🖥️ 3. Operating System Specific Configurations

### Windows 10 / Windows 11 Setup

B64Lab features a hand-crafted ANSI/VT100 24-bit TrueColor engine that automatically activates Windows Virtual Terminal Processing via the Windows Kernel API (`ctypes.windll.kernel32.SetConsoleMode`).

For the sharpest visual experience in Windows CMD or PowerShell:
1. **Use Windows Terminal (Recommended):** Pre-installed on Windows 11; available via Microsoft Store or winget for Windows 10.
2. **Enable UTF-8 Code Page (If Unicode borders look distorted):**
   ```powershell
   chcp 65001
   ```
3. **Font Recommendation:** Use any TrueType monospace font with box-drawing support (e.g., *Cascadia Code*, *Consolas*, *Fira Code*, *JetBrains Mono*).

### Linux / macOS Setup

On Unix systems, standard VT100 escape codes and UTF-8 encoding are supported natively out of the box:
```bash
# Ensure execution permissions (optional)
chmod +x b64lab.py

# Launch
./b64lab.py
```

---

## 🔒 4. Air-Gapped / Isolated Forensic Workstation Deployment

Because B64Lab relies **100% on the Python Standard Library**, it is specifically designed for restricted jumpboxes, malware analysis sandboxes, and air-gapped forensic environments (e.g., SANS SIFT, REMnux, FlareVM):

1. **Package the Repository (On an Internet-Connected Machine):**
   ```bash
   git clone https://github.com/veruthiaoperations-cloud/B64LAB.git
   tar -czvf b64lab-airgap.tar.gz B64LAB/
   ```
2. **Transfer via Secure USB or SCP to the Air-Gapped Machine.**
3. **Extract and Run Directly:**
   ```bash
   tar -xzvf b64lab-airgap.tar.gz
   cd B64LAB
   python3 b64lab.py
   ```
*No pip wheels, compiler toolchains, or network calls are ever required.*

---

## 🐳 5. Headless Docker & CI/CD Pipelines

To run B64Lab in automated security pipelines or containers without an interactive terminal:

### Docker One-Liner (Zero-Build)
You can run B64Lab using the standard lightweight official Python Alpine image:

```bash
docker run --rm -v $(pwd):/data python:3-alpine python /data/b64lab.py carve /data/samples/sample_web_access.log --format csv -o /data/triage.csv
```

### Headless CLI Flags
* **Carve logs to CSV spreadsheet:**
  ```bash
  python b64lab.py carve /var/log/apache2/access.log --format csv -o incident.csv
  ```
* **Carve logs to SQLite database:**
  ```bash
  python b64lab.py carve /var/log/syslog --format sqlite -o forensics.db
  ```
* **Unix Pipe Streaming:**
  ```bash
  cat /var/log/nginx/access.log | python b64lab.py carve - --format json
  ```

---

## 🧪 6. Verifying Installation & Integrity

Run the built-in automated test suite to confirm all cryptographic, bitwise, and carving engines function properly on your environment:

```bash
python -m unittest tests/test_suite.py -v
```

**Expected Output:**
```
Ran 30 tests in 0.047s
OK
```
