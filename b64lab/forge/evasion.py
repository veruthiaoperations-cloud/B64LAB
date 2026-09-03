"""
Adversary Evasion & Custom Alphabet Simulation Engine.
Pure Python standard library implementation.
"""

import base64
import random
from typing import Dict, Any

from ..core.alphabets import Alphabets, CustomAlphabet

class EvasionForge:
    """
    Simulates evasion tricks used by threat actors to test detection rules:
    - Custom alphabet substitution
    - Padding stripping
    - Whitespace / newline fragmentation
    """

    @classmethod
    def apply_custom_alphabet(cls, text: str, alphabet: str) -> Dict[str, str]:
        """Translates standard Base64 into a custom threat-actor alphabet."""
        std_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
        custom_b64 = CustomAlphabet.translate_standard_to_custom(std_b64, alphabet)

        return {
            "standard_b64": std_b64,
            "custom_b64": custom_b64,
            "alphabet_used": alphabet,
        }

    @classmethod
    def strip_padding(cls, std_b64: str) -> str:
        """Removes all trailing '=' characters to evade padding-strict regexes."""
        return std_b64.rstrip("=")

    @classmethod
    def inject_whitespace(cls, b64_str: str, chunk_size: int = 16) -> str:
        """Splits Base64 string with random tabs and carriage returns."""
        chunks = [b64_str[i:i + chunk_size] for i in range(0, len(b64_str), chunk_size)]
        delimiters = [" ", "\t", "\r\n", "  "]
        result = []
        for c in chunks:
            result.append(c)
            result.append(random.choice(delimiters))
        return "".join(result).strip()
