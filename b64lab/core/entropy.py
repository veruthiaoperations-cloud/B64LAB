"""
Shannon Entropy Calculation Engine for Anomaly & Obfuscation Detection.
Pure Python standard library implementation.
"""

import math
from collections import Counter
from dataclasses import dataclass
from typing import Union

@dataclass
class EntropyReport:
    """Detailed entropy analysis report for a given byte or character sequence."""
    entropy: float
    length: int
    classification: str
    threat_level: str  # LOW, SUSPICIOUS, HIGH, CRITICAL
    description: str
    is_likely_base64: bool
    is_likely_encrypted: bool

class ShannonEntropy:
    """
    Shannon Entropy Engine:
    H(X) = -sum(P(x) * log2(P(x)))
    
    Used by SOC analysts and EDR engines to detect packed binaries,
    encrypted command-and-control beacons, and encoded strings.
    """

    @staticmethod
    def calculate(data: Union[str, bytes]) -> float:
        """Calculates Shannon entropy in bits per symbol (0.0 to 8.0)."""
        if not data:
            return 0.0
        
        # If string, analyze character frequency; if bytes, analyze byte frequency
        length = len(data)
        frequencies = Counter(data)
        
        entropy = 0.0
        for count in frequencies.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
            
        return round(entropy, 4)

    @classmethod
    def analyze(cls, data: Union[str, bytes]) -> EntropyReport:
        """
        Analyzes data and classifies it based on operational security thresholds.
        """
        entropy = cls.calculate(data)
        length = len(data)
        
        # Determine classification
        if length < 8:
            return EntropyReport(
                entropy=entropy,
                length=length,
                classification="SAMPLE_TOO_SHORT",
                threat_level="LOW",
                description="Sample length is too small for statistically valid entropy calculation.",
                is_likely_base64=False,
                is_likely_encrypted=False,
            )
            
        # Standard ASCII English text: 3.5 - 4.5
        if entropy < 4.5:
            classification = "PLAINTEXT_NATURAL_LANGUAGE"
            threat_level = "LOW"
            desc = "Low randomness. Consistent with natural language or un-obfuscated script code."
            likely_b64 = False
            likely_enc = False
        # Base64 strings typically cluster in the 5.1 - 5.95 range
        elif 4.9 <= entropy <= 6.1:
            classification = "ENCODED_DATA (BASE64 / BASE32)"
            threat_level = "SUSPICIOUS"
            desc = "Uniform 64-symbol distribution. High probability of Base64 or Base32 encoding."
            likely_b64 = True
            likely_enc = False
        # High entropy: compressed or encrypted payloads
        elif entropy > 6.1:
            classification = "ENCRYPTED_OR_COMPRESSED"
            threat_level = "HIGH" if entropy < 7.3 else "CRITICAL"
            desc = "Near-maximum randomness. Indicates cryptographic ciphertext, zlib/gzip compression, or packed shellcode."
            likely_b64 = False
            likely_enc = True
        else:
            classification = "MODERATE_STRUCTURED"
            threat_level = "LOW"
            desc = "Moderate randomness. Likely structured data (JSON, XML, HTML, CSV)."
            likely_b64 = False
            likely_enc = False
            
        return EntropyReport(
            entropy=entropy,
            length=length,
            classification=classification,
            threat_level=threat_level,
            description=desc,
            is_likely_base64=likely_b64,
            is_likely_encrypted=likely_enc,
        )

    @staticmethod
    def render_bar(entropy: float, max_width: int = 24) -> str:
        """Renders an ASCII visualization bar of entropy (0.0 to 8.0)."""
        clamped = max(0.0, min(8.0, entropy))
        filled = int((clamped / 8.0) * max_width)
        empty = max_width - filled
        return f"[{'█' * filled}{'░' * empty}] {entropy:.2f}/8.00"
