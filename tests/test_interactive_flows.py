"""
End-to-End Comprehensive CLI & Interactive User Flow Test Suite for B64Lab.
Exercises all headless subcommands and all interactive menu paths.
Zero external dependencies. Pure Python standard library.
"""

import os
import sys
import unittest
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_b64lab_process(input_text: str, timeout: float = 10.0, extra_args=None):
    """Executes B64Lab in a subprocess with input string streamed to stdin."""
    cmd = [sys.executable, "-m", "b64lab"]
    if extra_args:
        cmd.extend(extra_args)

    proc = subprocess.Popen(
        cmd,
        cwd=PROJECT_ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    stdout, stderr = proc.communicate(input=input_text, timeout=timeout)
    return proc.returncode, stdout, stderr

class TestInteractiveUserFlows(unittest.TestCase):
    """Verifies all interactive TUI user paths complete cleanly without exceptions."""

    def test_flow_main_menu_exit(self):
        """User launches app and exits immediately."""
        code, stdout, stderr = run_b64lab_process("0\n")
        self.assertEqual(code, 0)
        self.assertIn("Exiting B64Lab", stdout)
        self.assertEqual(stderr, "")

    def test_flow_academy_complete_traversal(self):
        """User traverses all 4 Academy modules and their sub-lessons."""
        inputs = [
            "1",      # Main menu -> Academy
            # Module 1
            "1",      # Academy -> Module 1 (Bitwise)
            "1", "",  # Walkthrough 'Man', pause
            "2", "Secret", "", # Custom string, pause
            "3", "",  # Padding mechanics, pause
            "0",      # Back to Academy
            # Module 2
            "2",      # Academy -> Module 2 (RFC 4648)
            "1", "",  # Base64URL, pause
            "2", "",  # Base32, pause
            "3", "",  # Padding matrix, pause
            "0",      # Back to Academy
            # Module 3
            "3",      # Academy -> Module 3 (Offensive)
            "1", "",  # PowerShell UTF-16LE, pause
            "2", "",  # Droppers, pause
            "3", "",  # Custom alphabet, pause
            "4", "",  # Evasion, pause
            "0",      # Back to Academy
            # Module 4
            "4",      # Academy -> Module 4 (Defensive)
            "1", "",  # Shannon Entropy, pause
            "2", "",  # Magic Bytes, pause
            "3", "",  # Log Carving, pause
            "4", "",  # Defanged Handling, pause
            "0",      # Back to Academy
            # Exit
            "0",      # Academy -> Main Menu
            "0",      # Main Menu -> Exit
        ]
        stdin_stream = "\n".join(inputs) + "\n"
        code, stdout, stderr = run_b64lab_process(stdin_stream, timeout=15.0)
        self.assertEqual(code, 0)
        self.assertIn("MODULE 1: BITWISE MECHANICS", stdout)
        self.assertIn("MODULE 2: RFC 4648 STANDARDS", stdout)
        self.assertIn("MODULE 3: ADVERSARY TRADECRAFT", stdout)
        self.assertIn("MODULE 4: DEFENSIVE TRIAGE", stdout)
        self.assertIn("Exiting B64Lab", stdout)
        self.assertEqual(stderr, "")

    def test_flow_triage_blue_team(self):
        """User tests all Defensive Triage workbench functions."""
        inputs = [
            "2",                      # Main Menu -> Triage
            "1", "SGVsbG8gV29ybGQ=", "N", "",  # Single string triage, decline export, pause
            "2", "samples/sample_web_access.log", "1", "N", "", # Carve file, inspect #1, decline export, pause
            "3", "samples/sample_nested_dropper.txt", "", # Recursive unpack file, pause
            "4", "N", "",             # Inspect built-in sample, decline export, pause
            "0",                      # Return to Main Menu
            "0",                      # Exit
        ]
        stdin_stream = "\n".join(inputs) + "\n"
        code, stdout, stderr = run_b64lab_process(stdin_stream, timeout=15.0)
        self.assertEqual(code, 0)
        self.assertIn("DEFENSIVE TRIAGE & FORENSIC CARVING LAB", stdout)
        self.assertIn("INCIDENT TRIAGE CARD", stdout)
        self.assertIn("DECONSTRUCTION TREE", stdout)
        self.assertIn("Exiting B64Lab", stdout)
        self.assertEqual(stderr, "")

    def test_flow_forge_red_team(self):
        """User tests all Offensive Payload Forge functions."""
        inputs = [
            "3",                      # Main Menu -> Forge
            "1", "1", "",             # PowerShell preset command 1, pause
            "1", "C", "whoami", "",   # PowerShell custom command, pause
            "2", "", "",              # Multi-stage dropper (default payload), pause
            "3", "Infiltrate", "1", "", # Custom alphabet (reversed), pause
            "4", "admin=1", "",       # Evasion sandbox, pause
            "5", "1", "",             # Generate synthetic web access log, pause
            "0",                      # Return to Main Menu
            "0",                      # Exit
        ]
        stdin_stream = "\n".join(inputs) + "\n"
        code, stdout, stderr = run_b64lab_process(stdin_stream, timeout=15.0)
        self.assertEqual(code, 0)
        self.assertIn("OFFENSIVE SIMULATION & PAYLOAD FORGE LAB", stdout)
        self.assertIn("POWERSHELL FORGE SPEC", stdout)
        self.assertIn("DROPPER DEPLOYMENT STACK", stdout)
        self.assertIn("CUSTOM ALPHABET RESULT", stdout)
        self.assertIn("EVASION ARTIFACTS", stdout)
        self.assertIn("Exiting B64Lab", stdout)
        self.assertEqual(stderr, "")

        # Cleanup generated sample log
        synthetic_log = os.path.join(PROJECT_ROOT, "samples", "synthetic_access.log")
        if os.path.exists(synthetic_log):
            try:
                os.remove(synthetic_log)
            except Exception:
                pass

    def test_flow_ctf_arena(self):
        """User enters CTF Arena, checks challenge prompt, requests hint, attempts flag."""
        inputs = [
            "4",                      # Main Menu -> CTF Arena
            "1",                      # Select Challenge 1
            "H",                      # Request Hint
            "S", "INCORRECT_FLAG",    # Submit incorrect flag
            "0",                      # Return to Arena
            "0",                      # Return to Main Menu
            "0",                      # Exit
        ]
        stdin_stream = "\n".join(inputs) + "\n"
        code, stdout, stderr = run_b64lab_process(stdin_stream, timeout=15.0)
        self.assertEqual(code, 0)
        self.assertIn("CTF CHALLENGE ARENA", stdout)
        self.assertIn("Level 1: First Contact", stdout)
        self.assertIn("[HINT]:", stdout)
        self.assertIn("INCORRECT FLAG", stdout)
        self.assertIn("Exiting B64Lab", stdout)
        self.assertEqual(stderr, "")

    def test_flow_quick_workbench(self):
        """User tests all 8 Quick Workbench encoder/decoder utilities."""
        inputs = [
            "5",                      # Main Menu -> Workbench
            "1", "Test Plaintext", "", # Standard encode, pause
            "2", "Test Plaintext", "", # URL-Safe encode, pause
            "3", "Test Plaintext", "", # Base32 encode, pause
            "4", "VGVzdCBQbGFpbnRleHQ=", "", # Base64 decode, pause
            "5", "KRSXG5CTMVRXEZLU", "",     # Base32 decode, pause
            "6", "HighEntropyString1234!#$%", "", # Shannon entropy, pause
            "7", "samples/sample_nested_dropper.txt", "N", "", # Data URI encode, decline export, pause
            "8", "data:image/png;base64,TVqQAAMAAAAEAAAA//8AALg=", "", # Data URI decode & HTML smuggling alert, pause
            "0",                      # Return to Main Menu
            "0",                      # Exit
        ]
        stdin_stream = "\n".join(inputs) + "\n"
        code, stdout, stderr = run_b64lab_process(stdin_stream, timeout=15.0)
        self.assertEqual(code, 0)
        self.assertIn("QUICK WORKBENCH: MULTI-FORMAT ENCODER / DECODER", stdout)
        self.assertIn("Base64 Encoded:", stdout)
        self.assertIn("Base64URL Encoded:", stdout)
        self.assertIn("Base32 Encoded:", stdout)
        self.assertIn("CRITICAL MIME MISMATCH! (HTML Smuggling Indicator T1027.006)", stdout)
        self.assertIn("Exiting B64Lab", stdout)
        self.assertEqual(stderr, "")

    def test_flow_glossary_and_mitre(self):
        """User searches glossary and inspects MITRE ATT&CK techniques."""
        inputs = [
            "6",                      # Main Menu -> Reference
            "1", "S", "entropy", "1", "", "0", # Glossary search 'entropy', select 1, pause, return
            "2", "1", "", "0",        # MITRE Reference, select 1 (T1027), pause, return
            "0",                      # Return to Main Menu
            "0",                      # Exit
        ]
        stdin_stream = "\n".join(inputs) + "\n"
        code, stdout, stderr = run_b64lab_process(stdin_stream, timeout=15.0)
        self.assertEqual(code, 0)
        self.assertIn("REFERENCE & INTELLIGENCE DATABASE", stdout)
        self.assertIn("Shannon Entropy", stdout)
        self.assertIn("MITRE ATT&CK MAPPINGS: ENCODING & OBFUSCATION", stdout)
        self.assertIn("ATT&CK T1027", stdout)
        self.assertIn("Exiting B64Lab", stdout)
        self.assertEqual(stderr, "")

    def test_flow_settings_theme_switching(self):
        """User cycles through all 5 themes in the settings menu."""
        inputs = [
            "7",                      # Main Menu -> Settings
            "1",                      # Amber
            "2",                      # Phosphor
            "3",                      # Ice Blue
            "4",                      # Crimson
            "5",                      # Mono
            "0",                      # Return to Main Menu
            "0",                      # Exit
        ]
        stdin_stream = "\n".join(inputs) + "\n"
        code, stdout, stderr = run_b64lab_process(stdin_stream, timeout=15.0)
        self.assertEqual(code, 0)
        self.assertIn("SETTINGS & PALETTE CUSTOMIZER", stdout)
        self.assertIn("Applied 80s IBM / Cyberpunk Warm Amber", stdout)
        self.assertIn("Applied Phosphor Green theme", stdout)
        self.assertIn("Applied Neon Ice Blue theme", stdout)
        self.assertIn("Applied Tactical Crimson Red theme", stdout)
        self.assertIn("Applied High-Contrast Monochrome theme", stdout)
        self.assertIn("Exiting B64Lab", stdout)
        self.assertEqual(stderr, "")

class TestHeadlessSubcommands(unittest.TestCase):
    """Verifies all non-interactive headless CLI subcommands."""

    def test_cmd_encode(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["encode", "Hello World"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.strip(), "SGVsbG8gV29ybGQ=")

    def test_cmd_encode_url(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["encode", "Subject?query=yes", "--url"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.strip(), "U3ViamVjdD9xdWVyeT15ZXM=")

    def test_cmd_decode_standard(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["decode", "SGVsbG8gV29ybGQ="])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.strip(), "Hello World")

    def test_cmd_decode_unpadded(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["decode", "SGVsbG8gV29ybGQ"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.strip(), "Hello World")

    def test_cmd_decode_utf16le(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["decode", "RwBlAHQALQBQAHIAbwBjAGUAcwBzAA==", "--utf16"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.strip(), "Get-Process")

    def test_cmd_decode_malformed_graceful(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["decode", "ABCDE"])
        self.assertEqual(code, 0)
        self.assertIn("[!] Error: Unable to decode Base64 payload", stdout)

    def test_cmd_ps(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["ps", "whoami"])
        self.assertEqual(code, 0)
        self.assertIn("UTF-16LE Base64:", stdout)
        self.assertIn("powershell.exe -NoProfile", stdout)

    def test_cmd_entropy(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["entropy", "Standard Text"])
        self.assertEqual(code, 0)
        self.assertIn("Entropy:", stdout)
        self.assertIn("Threat: LOW", stdout)

    def test_cmd_trace_nonblocking(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["trace", "Man"])
        self.assertEqual(code, 0)
        self.assertIn("BITWISE TRACE: 'MAN'", stdout)
        self.assertIn("Final Result: \"TWFu\"", stdout)

    def test_cmd_carve_table(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["carve", "samples/sample_web_access.log"])
        self.assertEqual(code, 0)
        self.assertIn("[+] Carved", stdout)
        self.assertIn("EXE", stdout)

    def test_cmd_carve_csv(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["carve", "samples/sample_web_access.log", "--format", "csv"])
        self.assertEqual(code, 0)
        self.assertIn("ID,Line,Threat,Entropy,Signature,SHA256,Raw_B64", stdout)

    def test_cmd_carve_json(self):
        code, stdout, _ = run_b64lab_process("", extra_args=["carve", "samples/sample_web_access.log", "--format", "json"])
        self.assertEqual(code, 0)
        self.assertIn('"threat":', stdout)
        self.assertIn('"raw_b64":', stdout)

    def test_cmd_carve_file_output_and_cleanup(self):
        csv_file = os.path.join(PROJECT_ROOT, "test_flow_carve.csv")
        try:
            code, stdout, _ = run_b64lab_process("", extra_args=["carve", "samples/sample_web_access.log", "--format", "csv", "-o", csv_file])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(csv_file))
            with open(csv_file, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("Artifact_ID", content)
        finally:
            if os.path.exists(csv_file):
                os.remove(csv_file)

if __name__ == "__main__":
    unittest.main()
