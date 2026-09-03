"""
Recursive De-obfuscation and Multi-Stage Unpacking Engine.
Pure Python standard library implementation using zlib and gzip.
"""

import gzip
import zlib
import base64
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union

from .signatures import SignatureDB, FileSignature
from .entropy import ShannonEntropy

@dataclass
class UnpackLayer:
    """Represents a single de-obfuscation step in the unpacking pipeline."""
    layer_number: int
    operation: str  # e.g., "BASE64_DECODE", "GZIP_DECOMPRESS", "ZLIB_DECOMPRESS", "UTF16LE_DECODE"
    input_size: int
    output_size: int
    entropy_before: float
    entropy_after: float
    signature_detected: Optional[str] = None
    detail: str = ""

@dataclass
class UnpackResult:
    """Final outcome of the recursive de-obfuscation pipeline."""
    original_input: Union[str, bytes]
    layers: List[UnpackLayer] = field(default_factory=list)
    final_payload: bytes = b""
    final_type: str = "UNKNOWN"
    final_description: str = ""
    is_nested: bool = False
    powershell_script: Optional[str] = None
    text_preview: Optional[str] = None

class RecursiveUnpacker:
    """
    Recursively unrolls nested obfuscation (Base64 -> Gzip -> Base64 -> Payload).
    Common in commodity malware droppers, Cobalt Strike stageless payloads, and living-off-the-land scripts.
    """

    MAX_RECURSION_DEPTH = 10
    MAX_DECOMPRESSED_SIZE = 25 * 1024 * 1024  # 25 MB safety ceiling for archive decompression

    @classmethod
    def unpack(cls, initial_data: Union[str, bytes]) -> UnpackResult:
        """
        Recursively unpacks data through all recognizable layers of Base64,
        compression, and character encoding.
        """
        result = UnpackResult(original_input=initial_data)
        current_data: bytes = b""
        
        # Normalize input to bytes
        if isinstance(initial_data, str):
            # Clean string
            cleaned_str = re.sub(r"\s+", "", initial_data)
            try:
                # Try standard base64 decode
                current_data = base64.b64decode(cleaned_str, validate=False)
                ent_before = ShannonEntropy.calculate(cleaned_str)
                ent_after = ShannonEntropy.calculate(current_data)
                result.layers.append(
                    UnpackLayer(
                        layer_number=1,
                        operation="BASE64_DECODE",
                        input_size=len(cleaned_str),
                        output_size=len(current_data),
                        entropy_before=ent_before,
                        entropy_after=ent_after,
                        detail="Initial Base64 string successfully decoded."
                    )
                )
            except Exception:
                current_data = initial_data.encode("utf-8")
        else:
            current_data = initial_data

        depth = len(result.layers)
        while depth < cls.MAX_RECURSION_DEPTH:
            depth += 1
            unpacked_something = False
            
            # 1. Check if payload is GZIP (1F 8B 08)
            if len(current_data) > 10 and current_data[:3] == b"\x1f\x8b\x08":
                try:
                    d_obj = zlib.decompressobj(16 + zlib.MAX_WBITS)
                    decompressed = d_obj.decompress(current_data, max_length=cls.MAX_DECOMPRESSED_SIZE)
                    capped = bool(d_obj.unconsumed_tail or not d_obj.eof)
                    ent_b = ShannonEntropy.calculate(current_data)
                    ent_a = ShannonEntropy.calculate(decompressed)
                    note = "Decompressed GZIP archive stream (capped at 25MB safety ceiling)." if capped else "Decompressed GZIP archive stream."
                    result.layers.append(
                        UnpackLayer(
                            layer_number=depth,
                            operation="GZIP_DECOMPRESS",
                            input_size=len(current_data),
                            output_size=len(decompressed),
                            entropy_before=ent_b,
                            entropy_after=ent_a,
                            signature_detected="GZIP",
                            detail=note
                        )
                    )
                    current_data = decompressed
                    unpacked_something = True
                    continue
                except Exception:
                    pass

            # 2. Check if payload is ZLIB / Deflate (78 9C, 78 01, 78 DA)
            if len(current_data) > 4 and current_data[:2] in [b"\x78\x9c", b"\x78\x01", b"\x78\xda", b"\x78\x5e"]:
                try:
                    d_obj = zlib.decompressobj(zlib.MAX_WBITS)
                    decompressed = d_obj.decompress(current_data, max_length=cls.MAX_DECOMPRESSED_SIZE)
                    capped = bool(d_obj.unconsumed_tail or not d_obj.eof)
                    ent_b = ShannonEntropy.calculate(current_data)
                    ent_a = ShannonEntropy.calculate(decompressed)
                    note = "Decompressed ZLIB/Deflate stream (capped at 25MB safety ceiling)." if capped else "Decompressed ZLIB/Deflate stream."
                    result.layers.append(
                        UnpackLayer(
                            layer_number=depth,
                            operation="ZLIB_DECOMPRESS",
                            input_size=len(current_data),
                            output_size=len(decompressed),
                            entropy_before=ent_b,
                            entropy_after=ent_a,
                            signature_detected="ZLIB",
                            detail=note
                        )
                    )
                    current_data = decompressed
                    unpacked_something = True
                    continue
                except Exception:
                    pass

            # 3. Check if current_data is ASCII text that is *another* Base64 blob
            is_text, text_val = SignatureDB.is_text(current_data)
            if is_text and text_val:
                clean_candidate = re.sub(r"\s+", "", text_val)
                # Ensure it matches Base64 alphabet and length constraints
                if len(clean_candidate) >= 16 and re.fullmatch(r"[A-Za-z0-9+/=]+", clean_candidate):
                    try:
                        next_bytes = base64.b64decode(clean_candidate, validate=True)
                        if len(next_bytes) > 0 and next_bytes != current_data:
                            ent_b = ShannonEntropy.calculate(clean_candidate)
                            ent_a = ShannonEntropy.calculate(next_bytes)
                            result.layers.append(
                                UnpackLayer(
                                    layer_number=depth,
                                    operation="BASE64_DECODE",
                                    input_size=len(clean_candidate),
                                    output_size=len(next_bytes),
                                    entropy_before=ent_b,
                                    entropy_after=ent_a,
                                    detail="Found inner nested Base64 encoded payload."
                                )
                            )
                            current_data = next_bytes
                            unpacked_something = True
                            continue
                    except Exception:
                        pass

            # If no further automatic unpacking could be performed, break
            if not unpacked_something:
                break

        # Final Analysis
        result.final_payload = current_data
        result.is_nested = len(result.layers) > 1

        # Check for PowerShell UTF-16LE
        is_ps, ps_script = SignatureDB.is_powershell_utf16le(current_data)
        if is_ps and ps_script:
            result.final_type = "POWERSHELL_UTF16LE"
            result.final_description = "Windows PowerShell Script (UTF-16LE Encoded Command)"
            result.powershell_script = ps_script
            result.text_preview = ps_script[:200]
            return result

        # Check for Magic Bytes Signature
        sig = SignatureDB.identify(current_data)
        if sig:
            result.final_type = sig.category
            result.final_description = sig.description
            return result

        # Check for Plaintext
        is_txt, text_val = SignatureDB.is_text(current_data)
        if is_txt and text_val:
            result.final_type = "PLAINTEXT_SCRIPT"
            result.final_description = "Plaintext ASCII/UTF-8 Script or Text"
            result.text_preview = text_val[:200]
            return result

        result.final_type = "RAW_BINARY"
        result.final_description = f"Raw Unidentified Binary Data ({len(current_data)} bytes)"
        return result
