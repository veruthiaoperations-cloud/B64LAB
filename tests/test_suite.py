"""
Comprehensive Automated Test Suite for B64Lab.
Covers Bitwise Math, Entropy, Magic Bytes, Carver, Unpacker, and Dynamic Anti-Cheat CTF solving.
Run via: python -m unittest tests/test_suite.py
Zero external dependencies required.
"""

import unittest
import base64
import gzip
import zlib
import os
import sys

# Ensure b64lab is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from b64lab.core.bitwise import BitwiseEngine
from b64lab.core.alphabets import Alphabets, CustomAlphabet
from b64lab.core.entropy import ShannonEntropy
from b64lab.core.signatures import SignatureDB
from b64lab.core.unpacker import RecursiveUnpacker
from b64lab.triage.carver import ArtifactCarver
from b64lab.forge.powershell import PowerShellForge
from b64lab.forge.dropper import DropperForge
from b64lab.ctf.engine import CTFAntiCheat, CHALLENGE_DEFINITIONS

class TestBitwiseEngine(unittest.TestCase):
    """Verifies first-principles bitwise operations match RFC 4648 standard."""

    def test_encode_matches_stdlib(self):
        test_cases = [
            b"",
            b"f",
            b"fo",
            b"foo",
            b"foob",
            b"fooba",
            b"foobar",
            b"Man",
            b"Security Operations Center",
            bytes(range(256)),
        ]
        for data in test_cases:
            std = base64.b64encode(data).decode("ascii")
            custom = BitwiseEngine.encode(data)
            self.assertEqual(custom, std, f"Failed on input: {data}")

    def test_decode_matches_stdlib(self):
        test_strings = [
            "",
            "Zg==",
            "Zm8=",
            "Zm9v",
            "TWFu",
            "U2VjdXJpdHk=",
        ]
        for s in test_strings:
            std = base64.b64decode(s)
            custom = BitwiseEngine.decode(s)
            self.assertEqual(custom, std, f"Decode failed on: {s}")

    def test_bitwise_trace_structure(self):
        traces = BitwiseEngine.trace_encode(b"Man")
        self.assertEqual(len(traces), 1)
        t = traces[0]
        self.assertEqual(t.sextets_dec, [19, 22, 5, 46])
        self.assertEqual(t.output_chars, ["T", "W", "F", "u"])
        self.assertEqual(t.padding_count, 0)

    def test_padding_traces(self):
        t1 = BitwiseEngine.trace_encode(b"A")[0]
        self.assertEqual(t1.padding_count, 2)
        self.assertEqual(t1.output_chars[-2:], ["=", "="])

        t2 = BitwiseEngine.trace_encode(b"AB")[0]
        self.assertEqual(t2.padding_count, 1)
        self.assertEqual(t2.output_chars[-1], "=")


class TestAlphabets(unittest.TestCase):
    """Verifies custom alphabet substitution and translation."""

    def test_custom_alphabet_roundtrip(self):
        original = "SecretPayload1234!"
        std_b64 = base64.b64encode(original.encode()).decode()
        custom_alpha = CustomAlphabet.generate_shuffled(seed=42)

        # Translate to custom and back
        custom_b64 = CustomAlphabet.translate_standard_to_custom(std_b64, custom_alpha)
        reverted_std = CustomAlphabet.translate_custom_to_standard(custom_b64, custom_alpha)

        self.assertEqual(reverted_std, std_b64)
        decoded = base64.b64decode(reverted_std).decode()
        self.assertEqual(decoded, original)


class TestEntropy(unittest.TestCase):
    """Verifies Shannon entropy calculation thresholds."""

    def test_zero_entropy(self):
        self.assertEqual(ShannonEntropy.calculate("AAAAAAA"), 0.0)

    def test_natural_language_entropy(self):
        text = "This is a normal English sentence with low randomness."
        ent = ShannonEntropy.calculate(text)
        self.assertTrue(3.0 <= ent <= 4.8, f"Unexpected text entropy: {ent}")

    def test_base64_entropy_clustering(self):
        b64 = base64.b64encode(os.urandom(128)).decode()
        ent = ShannonEntropy.calculate(b64)
        self.assertTrue(5.0 <= ent <= 6.0, f"Base64 entropy out of range: {ent}")


class TestSignatures(unittest.TestCase):
    """Verifies magic byte detection."""

    def test_pe_detection(self):
        pe_bytes = b"MZ\x90\x00\x03\x00\x00\x00"
        sig = SignatureDB.identify(pe_bytes)
        self.assertIsNotNone(sig)
        self.assertEqual(sig.extension, "exe")
        self.assertEqual(sig.category, "EXECUTABLE")

    def test_elf_detection(self):
        elf_bytes = b"\x7fELF\x02\x01\x01\x00"
        sig = SignatureDB.identify(elf_bytes)
        self.assertIsNotNone(sig)
        self.assertEqual(sig.extension, "elf")

    def test_pdf_detection(self):
        pdf_bytes = b"%PDF-1.7\n%..."
        sig = SignatureDB.identify(pdf_bytes)
        self.assertIsNotNone(sig)
        self.assertEqual(sig.extension, "pdf")

    def test_powershell_utf16le_detection(self):
        cmd = "whoami; Get-Process"
        raw_utf16 = cmd.encode("utf-16le")
        is_ps, text = SignatureDB.is_powershell_utf16le(raw_utf16)
        self.assertTrue(is_ps)
        self.assertEqual(text, cmd)

    def test_java_serialization_signature(self):
        raw = b"\xac\xed\x00\x05sr\x00\x0bMyClass"
        sig = SignatureDB.identify(raw)
        self.assertIsNotNone(sig)
        self.assertEqual(sig.extension, "java-ser")
        self.assertEqual(sig.category, "SERIALIZATION")

    def test_viewstate_signature(self):
        raw = b"\xff\x01\x12\x34\x56"
        sig = SignatureDB.identify(raw)
        self.assertIsNotNone(sig)
        self.assertEqual(sig.extension, "viewstate")

    def test_pickle_signature(self):
        raw = b"\x80\x04\x95\x12\x00\x00\x00"
        sig = SignatureDB.identify(raw)
        self.assertIsNotNone(sig)
        self.assertEqual(sig.extension, "pickle")

    def test_html_smuggling_mime_mismatch(self):
        # Disguised EXE inside an image Data URI
        fake_pe = b"MZ" + b"\x00" * 30
        b64_pe = base64.b64encode(fake_pe).decode()
        html_line = f'<img src="data:image/png;base64,{b64_pe}">'
        artifacts = ArtifactCarver.carve_string(html_line)
        self.assertEqual(len(artifacts), 1)
        self.assertIn("HTML Smuggling", artifacts[0].threat_assessment)
        self.assertIn("image/png", artifacts[0].threat_assessment)


class TestUnpacker(unittest.TestCase):
    """Verifies recursive multi-stage de-obfuscation."""

    def test_gzip_nested_unpack(self):
        inner_payload = "Get-Process -Name lsass"
        dropper = DropperForge.build_gzip_dropper(inner_payload)
        
        result = RecursiveUnpacker.unpack(dropper["b64_payload"])
        self.assertTrue(result.is_nested)
        self.assertIn(inner_payload, result.final_payload.decode("utf-8"))

    def test_zlib_nested_unpack(self):
        inner_payload = "Get-Service | Where-Object Status -eq 'Running'"
        dropper = DropperForge.build_zlib_dropper(inner_payload)
        result = RecursiveUnpacker.unpack(dropper["b64_payload"])
        self.assertTrue(result.is_nested)
        self.assertIn(inner_payload, result.final_payload.decode("utf-8"))

    def test_unpacker_decompression_safety_limit(self):
        self.assertTrue(hasattr(RecursiveUnpacker, "MAX_DECOMPRESSED_SIZE"))
        self.assertGreaterEqual(RecursiveUnpacker.MAX_DECOMPRESSED_SIZE, 1024 * 1024)


class TestArtifactCarver(unittest.TestCase):
    """Verifies carving Base64 from noisy unstructured logs and exporting to CSV/JSON/SQLite."""

    def test_carve_from_log_line(self):
        secret = "FLAG{carver_test_passed}"
        b64_secret = base64.b64encode(secret.encode()).decode()
        log_line = f"192.168.1.1 - - [03/Sep/2026:10:00:00] 'GET /index.php?data={b64_secret} HTTP/1.1' 200 412"

        artifacts = ArtifactCarver.carve_string(log_line)
        self.assertGreaterEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].decoded_bytes.decode(), secret)

    def test_export_csv(self):
        import tempfile, csv
        payload = base64.b64encode(b"Enterprise Logging Test Payload 12345").decode()
        artifacts = ArtifactCarver.carve_string(f"Payload: {payload}")
        self.assertGreaterEqual(len(artifacts), 1)

        fd, temp_path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            ArtifactCarver.export_csv(artifacts, temp_path)
            with open(temp_path, "r", encoding="utf-8") as f:
                reader = list(csv.reader(f))
                self.assertGreaterEqual(len(reader), 2)
                self.assertIn("Artifact_ID", reader[0])
                self.assertIn("SHA256", reader[0])
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_export_jsonl(self):
        import tempfile, json
        payload = base64.b64encode(b"Enterprise Logging Test Payload 12345").decode()
        artifacts = ArtifactCarver.carve_string(f"Payload: {payload}")
        self.assertGreaterEqual(len(artifacts), 1)

        fd, temp_path = tempfile.mkstemp(suffix=".jsonl")
        os.close(fd)
        try:
            ArtifactCarver.export_jsonl(artifacts, temp_path)
            with open(temp_path, "r", encoding="utf-8") as f:
                lines = [json.loads(line) for line in f]
                self.assertEqual(len(lines), 1)
                self.assertEqual(lines[0]["raw_b64"], payload)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_export_sqlite(self):
        import tempfile, sqlite3
        payload = base64.b64encode(b"Enterprise Logging Test Payload 12345").decode()
        artifacts = ArtifactCarver.carve_string(f"Payload: {payload}")
        self.assertGreaterEqual(len(artifacts), 1)

        fd, temp_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            ArtifactCarver.export_sqlite(artifacts, temp_path)
            conn = sqlite3.connect(temp_path)
            c = conn.cursor()
            rows = c.execute("SELECT id, raw_b64 FROM carved_artifacts").fetchall()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][1], payload)
            conn.close()
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestDynamicAntiCheatCTF(unittest.TestCase):
    """
    Verifies the cryptographic HMAC-SHA256 dynamic anti-cheat flag generator.
    Ensures every challenge synthesizes accurately and solves mathematically.
    """

    def setUp(self):
        self.salt = "test_salt_alpha_9999_deadbeef1234"

    def test_different_salts_produce_unique_flags(self):
        flag_user1 = CTFAntiCheat.derive_flag(1, "user_1_salt_aaaa")
        flag_user2 = CTFAntiCheat.derive_flag(1, "user_2_salt_bbbb")
        self.assertNotEqual(flag_user1, flag_user2, "Anti-cheat failed: Flags should be unique per salt!")

    def test_challenge_1_dynamic_solve(self):
        c = CTFAntiCheat.synthesize_challenge(1, self.salt)
        recovered = base64.b64decode(c["payload"]).decode()
        self.assertEqual(recovered, c["flag"])

    def test_challenge_2_dynamic_solve(self):
        c = CTFAntiCheat.synthesize_challenge(2, self.salt)
        rem = len(c["payload"]) % 4
        pad = "==" if rem == 2 else "="
        recovered = base64.b64decode(c["payload"] + pad).decode()
        self.assertEqual(recovered, c["flag"])

    def test_challenge_3_dynamic_solve(self):
        c = CTFAntiCheat.synthesize_challenge(3, self.salt)
        recovered = base64.b64decode(c["payload"]).decode("utf-16le")
        self.assertEqual(recovered, c["flag"])

    def test_challenge_4_dynamic_solve(self):
        c = CTFAntiCheat.synthesize_challenge(4, self.salt)
        arts = ArtifactCarver.carve_string(c["prompt"])
        self.assertGreaterEqual(len(arts), 1)
        self.assertEqual(arts[0].decoded_bytes.decode(), c["flag"])

    def test_challenge_5_dynamic_solve(self):
        c = CTFAntiCheat.synthesize_challenge(5, self.salt)
        raw = base64.b64decode(c["payload"])
        sig = SignatureDB.identify(raw)
        self.assertIsNotNone(sig)
        self.assertIn(sig.extension.upper(), c["accepted_flags"])

    def test_challenge_6_dynamic_solve(self):
        c = CTFAntiCheat.synthesize_challenge(6, self.salt)
        unpacked = gzip.decompress(base64.b64decode(c["payload"])).decode()
        self.assertEqual(unpacked, c["flag"])

    def test_challenge_7_dynamic_solve(self):
        c = CTFAntiCheat.synthesize_challenge(7, self.salt)
        rev_alpha = "/+9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA"
        std_b64 = CustomAlphabet.translate_custom_to_standard(c["payload"], rev_alpha)
        recovered = base64.b64decode(std_b64).decode()
        self.assertEqual(recovered, c["flag"])

    def test_challenge_8_dynamic_solve(self):
        c = CTFAntiCheat.synthesize_challenge(8, self.salt)
        recovered = base64.b64decode(c["payload"]).decode()
        self.assertEqual(recovered, c["flag"])

    def test_ctf_state_file_resolution(self):
        path = CTFAntiCheat.get_state_file()
        self.assertTrue(isinstance(path, str))
        self.assertTrue(path.endswith(".b64lab_profile.json"))


class TestCLIModule(unittest.TestCase):
    """Verifies CLI argument execution and error boundaries."""

    def test_cli_decode_malformed_graceful(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "b64lab", "decode", "ABCDE"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("[!] Error: Unable to decode Base64 payload", result.stdout)

    def test_cli_encode(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "b64lab", "encode", "TestPayload123"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("VGVzdFBheWxvYWQxMjM=", result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
