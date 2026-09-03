"""
Forensic Base64 Artifact Carver for Raw Text, Logs, and Scripts.
Pure Python standard library implementation.
"""

import re
import base64
import hashlib
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Any

from ..core.entropy import ShannonEntropy, EntropyReport
from ..core.signatures import SignatureDB, FileSignature
from ..core.unpacker import RecursiveUnpacker, UnpackResult

@dataclass
class CarvedArtifact:
    """Forensic record of a carved Base64 artifact."""
    artifact_id: int
    line_number: int
    start_offset: int
    raw_b64: str
    padded: bool
    entropy: float
    entropy_class: str
    decoded_bytes: bytes
    md5: str
    sha256: str
    signature: Optional[FileSignature]
    is_powershell: bool
    powershell_code: Optional[str]
    is_text: bool
    text_preview: Optional[str]
    threat_assessment: str

class ArtifactCarver:
    """
    Forensic regex carver that extracts Base64 sequences from unstructured data.
    Evaluates entropy, magic bytes, hashes, and character encodings.
    """

    # Regex matching Base64 chunks (min length 16 chars)
    # Permissive to capture both padded ('=', '==') and unpadded sequences
    B64_REGEX = re.compile(r"[A-Za-z0-9+/]{16,}={0,2}")

    @classmethod
    def carve_stream(cls, line_iterable, min_length: int = 16):
        """
        Streaming generator for enterprise logs.
        Yields CarvedArtifacts line-by-line without loading entire files into memory.
        """
        artifact_counter = 1
        for line_num, line in enumerate(line_iterable, start=1):
            matches = cls.B64_REGEX.finditer(line)
            for m in matches:
                candidate = m.group(0)
                if len(candidate) < min_length:
                    continue

                clean_candidate, padded_now = cls._normalize_padding(candidate)
                try:
                    decoded = base64.b64decode(clean_candidate, validate=False)
                    if not decoded:
                        continue
                except Exception:
                    continue

                ent_report = ShannonEntropy.analyze(candidate)
                md5_hash = hashlib.md5(decoded).hexdigest()
                sha256_hash = hashlib.sha256(decoded).hexdigest()

                sig = SignatureDB.identify(decoded)
                is_ps, ps_code = SignatureDB.is_powershell_utf16le(decoded)
                is_txt, txt_preview = SignatureDB.is_text(decoded)

                if sig and sig.category in ["EXECUTABLE", "SHELLCODE"]:
                    threat = "CRITICAL (Embedded Executable / Shellcode)"
                elif is_ps:
                    threat = "HIGH (PowerShell UTF-16LE Script)"
                elif sig and sig.category == "ARCHIVE":
                    threat = "HIGH (Embedded Archive / Dropper Stager)"
                elif ent_report.entropy > 6.5:
                    threat = "SUSPICIOUS (High Randomness / Encrypted Payload)"
                else:
                    threat = "LOW / INFORMATIONAL"

                yield CarvedArtifact(
                    artifact_id=artifact_counter,
                    line_number=line_num,
                    start_offset=m.start(),
                    raw_b64=candidate,
                    padded=padded_now,
                    entropy=ent_report.entropy,
                    entropy_class=ent_report.classification,
                    decoded_bytes=decoded,
                    md5=md5_hash,
                    sha256=sha256_hash,
                    signature=sig,
                    is_powershell=is_ps,
                    powershell_code=ps_code,
                    is_text=is_txt,
                    text_preview=txt_preview[:150] if txt_preview else None,
                    threat_assessment=threat,
                )
                artifact_counter += 1

    @classmethod
    def carve_string(cls, content: str, min_length: int = 16) -> List[CarvedArtifact]:
        """Scans a text string and carves all valid Base64 payloads."""
        return list(cls.carve_stream(content.splitlines(), min_length))

    @classmethod
    def carve_file(cls, filepath: str, min_length: int = 16) -> List[CarvedArtifact]:
        """Reads a file line-by-line from disk and carves all Base64 artifacts."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return list(cls.carve_stream(f, min_length))
        except Exception:
            return []

    @staticmethod
    def export_csv(artifacts: List[CarvedArtifact], output_filepath: str) -> None:
        """Exports carved artifacts to a spreadsheet-compatible CSV file."""
        import csv
        with open(output_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Artifact_ID", "Line_Number", "Threat_Assessment", "Entropy",
                "Entropy_Class", "File_Signature", "Is_PowerShell", "MD5",
                "SHA256", "Decoded_Size_Bytes", "Text_Preview", "Raw_Base64"
            ])
            for a in artifacts:
                sig_desc = a.signature.description if a.signature else ("PowerShell" if a.is_powershell else "None")
                preview = a.powershell_code if a.is_powershell else (a.text_preview or "")
                writer.writerow([
                    a.artifact_id, a.line_number, a.threat_assessment, a.entropy,
                    a.entropy_class, sig_desc, a.is_powershell, a.md5,
                    a.sha256, len(a.decoded_bytes), preview.replace("\n", " ")[:100], a.raw_b64
                ])

    @staticmethod
    def export_jsonl(artifacts: List[CarvedArtifact], output_filepath: str) -> None:
        """Exports carved artifacts to JSON Lines for SIEM / Splunk / Elastic ingestion."""
        import json
        with open(output_filepath, "w", encoding="utf-8") as f:
            for a in artifacts:
                record = {
                    "artifact_id": a.artifact_id,
                    "line_number": a.line_number,
                    "threat_assessment": a.threat_assessment,
                    "entropy": a.entropy,
                    "entropy_class": a.entropy_class,
                    "file_signature": a.signature.extension if a.signature else None,
                    "is_powershell": a.is_powershell,
                    "md5": a.md5,
                    "sha256": a.sha256,
                    "decoded_bytes_len": len(a.decoded_bytes),
                    "text_preview": a.text_preview,
                    "raw_b64": a.raw_b64,
                }
                f.write(json.dumps(record) + "\n")

    @staticmethod
    def export_sqlite(artifacts: List[CarvedArtifact], db_filepath: str) -> None:
        """Exports carved artifacts to an indexed SQLite database for SQL queries."""
        import sqlite3
        conn = sqlite3.connect(db_filepath)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carved_artifacts (
                id INTEGER PRIMARY KEY,
                line_number INTEGER,
                threat_assessment TEXT,
                entropy REAL,
                entropy_class TEXT,
                signature TEXT,
                is_powershell INTEGER,
                md5 TEXT,
                sha256 TEXT,
                size_bytes INTEGER,
                text_preview TEXT,
                raw_b64 TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sha256 ON carved_artifacts(sha256)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entropy ON carved_artifacts(entropy)")

        for a in artifacts:
            sig_name = a.signature.extension if a.signature else ("ps1" if a.is_powershell else "unknown")
            cursor.execute("""
                INSERT INTO carved_artifacts (
                    line_number, threat_assessment, entropy, entropy_class,
                    signature, is_powershell, md5, sha256, size_bytes, text_preview, raw_b64
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                a.line_number, a.threat_assessment, a.entropy, a.entropy_class,
                sig_name, 1 if a.is_powershell else 0, a.md5, a.sha256,
                len(a.decoded_bytes), a.text_preview, a.raw_b64
            ))
        conn.commit()
        conn.close()

    @staticmethod
    def _normalize_padding(b64_str: str) -> Tuple[str, bool]:
        """Ensures length is a multiple of 4 by appending '=' padding if needed."""
        remainder = len(b64_str) % 4
        if remainder == 0:
            return b64_str, True
        elif remainder == 2:
            return b64_str + "==", False
        elif remainder == 3:
            return b64_str + "=", False
        return b64_str, False
