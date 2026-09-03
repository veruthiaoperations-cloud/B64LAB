"""
Pure Bitwise Engine for RFC 4648 Base64 Encoding and Decoding.
Implemented from first principles using bitwise shifts, masks, and buffers.
Zero external dependencies.
"""

from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

STANDARD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
STANDARD_DECODE_MAP = {char: idx for idx, char in enumerate(STANDARD_ALPHABET)}

@dataclass
class BitwiseChunkTrace:
    """Represents a detailed bitwise breakdown of a 3-byte -> 4-character step."""
    chunk_index: int
    raw_bytes: bytes
    raw_hex: List[str]
    raw_binaries: List[str]
    buffer_24bit_bin: str
    sextets_bin: List[str]
    sextets_dec: List[int]
    output_chars: List[str]
    padding_count: int
    note: str

class BitwiseEngine:
    """
    First-principles bitwise Base64 engine.
    Exposes bitwise transformation mechanics for visual education.
    """

    @staticmethod
    def encode(data: bytes, alphabet: str = STANDARD_ALPHABET, pad: bool = True) -> str:
        """Encodes raw bytes to Base64 using pure bitwise operations."""
        if not data:
            return ""
        
        result = []
        length = len(data)
        i = 0
        
        while i < length:
            b1 = data[i]
            b2 = data[i + 1] if (i + 1) < length else 0
            b3 = data[i + 2] if (i + 2) < length else 0
            
            # Combine 3 bytes into a single 24-bit integer
            buffer24 = (b1 << 16) | (b2 << 8) | b3
            
            # Extract 4 6-bit chunks using bit shifts and mask (0x3F = 00111111)
            c1 = alphabet[(buffer24 >> 18) & 0x3F]
            c2 = alphabet[(buffer24 >> 12) & 0x3F]
            c3 = alphabet[(buffer24 >> 6) & 0x3F]
            c4 = alphabet[buffer24 & 0x3F]
            
            remaining = length - i
            if remaining == 1:
                result.append(c1)
                result.append(c2)
                if pad:
                    result.append("==")
            elif remaining == 2:
                result.append(c1)
                result.append(c2)
                result.append(c3)
                if pad:
                    result.append("=")
            else:
                result.extend([c1, c2, c3, c4])
            
            i += 3
            
        return "".join(result)

    @staticmethod
    def decode(encoded: str, alphabet: str = STANDARD_ALPHABET) -> bytes:
        """Decodes a Base64 string to raw bytes using bitwise operations."""
        if not encoded:
            return b""
            
        # Fast character filtering
        if alphabet == STANDARD_ALPHABET:
            decode_map = STANDARD_DECODE_MAP
            clean = "".join(ch for ch in encoded if ch in decode_map)
        else:
            decode_map = {char: idx for idx, char in enumerate(alphabet)}
            clean = "".join(ch for ch in encoded if ch in decode_map)
        
        result = bytearray()
        length = len(clean)
        i = 0
        
        while i < length:
            # Gather up to 4 sextets
            s1 = decode_map[clean[i]]
            s2 = decode_map[clean[i + 1]] if (i + 1) < length else 0
            s3 = decode_map[clean[i + 2]] if (i + 2) < length else 0
            s4 = decode_map[clean[i + 3]] if (i + 3) < length else 0
            
            # Reconstruct 24-bit integer from 4 sextets
            buffer24 = (s1 << 18) | (s2 << 12) | (s3 << 6) | s4
            
            # Extract bytes
            remaining = length - i
            result.append((buffer24 >> 16) & 0xFF)
            if remaining >= 3:
                result.append((buffer24 >> 8) & 0xFF)
            if remaining >= 4:
                result.append(buffer24 & 0xFF)
                
            i += 4
            
        return bytes(result)

    @classmethod
    def trace_encode(cls, data: bytes, alphabet: str = STANDARD_ALPHABET) -> List[BitwiseChunkTrace]:
        """
        Generates an educational step-by-step trace of the bitwise transformation.
        Breaks down every 3-byte group into 24 bits, 4 sextets, and final characters.
        """
        traces = []
        length = len(data)
        chunk_idx = 0
        i = 0
        
        while i < length:
            chunk = data[i:i + 3]
            raw_hex = [f"0x{b:02X}" for b in chunk]
            raw_bin = [f"{b:08b}" for b in chunk]
            
            b1 = chunk[0]
            b2 = chunk[1] if len(chunk) > 1 else 0
            b3 = chunk[2] if len(chunk) > 2 else 0
            
            # 24-bit buffer
            buffer24 = (b1 << 16) | (b2 << 8) | b3
            buffer_bin = f"{buffer24:024b}"
            
            # 4 sextets
            idx1 = (buffer24 >> 18) & 0x3F
            idx2 = (buffer24 >> 12) & 0x3F
            idx3 = (buffer24 >> 6) & 0x3F
            idx4 = buffer24 & 0x3F
            
            sextets_dec = [idx1, idx2, idx3, idx4]
            sextets_bin = [f"{v:06b}" for v in sextets_dec]
            
            if len(chunk) == 1:
                output_chars = [alphabet[idx1], alphabet[idx2], "=", "="]
                padding_count = 2
                note = "1 byte (8 bits) + 4 zero bits = 2 sextets. Appended '==' padding."
            elif len(chunk) == 2:
                output_chars = [alphabet[idx1], alphabet[idx2], alphabet[idx3], "="]
                padding_count = 1
                note = "2 bytes (16 bits) + 2 zero bits = 3 sextets. Appended '=' padding."
            else:
                output_chars = [alphabet[idx1], alphabet[idx2], alphabet[idx3], alphabet[idx4]]
                padding_count = 0
                note = "Complete 3-byte chunk (24 bits) maps cleanly to 4 sextets (no padding)."
                
            traces.append(
                BitwiseChunkTrace(
                    chunk_index=chunk_idx,
                    raw_bytes=chunk,
                    raw_hex=raw_hex,
                    raw_binaries=raw_bin,
                    buffer_24bit_bin=buffer_bin,
                    sextets_bin=sextets_bin,
                    sextets_dec=sextets_dec,
                    output_chars=output_chars,
                    padding_count=padding_count,
                    note=note,
                )
            )
            chunk_idx += 1
            i += 3
            
        return traces

BitwiseTrace = BitwiseChunkTrace
