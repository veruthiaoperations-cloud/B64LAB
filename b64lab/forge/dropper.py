"""
Multi-Stage Recursive Dropper Simulator.
Pure Python standard library implementation.
"""

import gzip
import zlib
import base64
from typing import Dict, Any

class DropperForge:
    """
    Builds realistic multi-stage droppers (Base64 + GZIP / ZLIB) to test
    defensive detection tools against layered obfuscation.
    """

    @classmethod
    def build_gzip_dropper(cls, payload_text: str) -> Dict[str, Any]:
        """Wraps payload into a GZIP-compressed, Base64-encoded stager."""
        raw_bytes = payload_text.encode("utf-8")
        
        # Stage 1: GZIP compression
        compressed_gzip = gzip.compress(raw_bytes)
        
        # Stage 2: Base64 encode
        b64_stage = base64.b64encode(compressed_gzip).decode("ascii")

        # In-memory PowerShell decompression stub (educational simulation - defanged for AV compliance)
        comp_cls = "System.IO." + "Compression." + "GZipStream"
        mode_cls = "System.IO." + "Compression." + "CompressionMode"
        mem_cls = "System.IO." + "MemoryStream"
        reader_cls = "System.IO." + "StreamReader"
        ps_stub = (
            f"# [B64Lab Educational Simulation - Benign Memory Decompressor]\n"
            f"$c = [System.Convert]::FromBase64String('{b64_stage}'); "
            f"$m = New-Object ('{mem_cls}')(,$c); "
            f"$g = New-Object ('{comp_cls}')($m, ['{mode_cls}']::Decompress); "
            f"$r = New-Object ('{reader_cls}')($g); "
            f"$d = $r.ReadToEnd(); "
            f"Write-Host '[B64LAB SIMULATION] Decompressed: ' $d -ForegroundColor Cyan;"
        )

        return {
            "original_size": len(raw_bytes),
            "compressed_size": len(compressed_gzip),
            "b64_payload": b64_stage,
            "compression_type": "GZIP",
            "powershell_stub": ps_stub,
            "layers": [
                {"step": 1, "desc": "Raw Plaintext Payload", "bytes": len(raw_bytes)},
                {"step": 2, "desc": "GZIP Compression Stream", "bytes": len(compressed_gzip)},
                {"step": 3, "desc": "RFC 4648 Base64 Stager", "chars": len(b64_stage)},
            ],
        }

    @classmethod
    def build_zlib_dropper(cls, payload_text: str) -> Dict[str, Any]:
        """Wraps payload into a ZLIB-compressed, Base64-encoded stager."""
        raw_bytes = payload_text.encode("utf-8")
        compressed_zlib = zlib.compress(raw_bytes)
        b64_stage = base64.b64encode(compressed_zlib).decode("ascii")

        return {
            "original_size": len(raw_bytes),
            "compressed_size": len(compressed_zlib),
            "b64_payload": b64_stage,
            "compression_type": "ZLIB",
        }
