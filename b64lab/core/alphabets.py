"""
RFC 4648 Alphabet Standards & Custom Threat Actor Substitution Tables.
Pure Python standard library implementation.
"""

import random
from typing import Dict, Optional, Tuple

class Alphabets:
    """Standardized and security-relevant encoding alphabets."""
    
    # RFC 4648 Section 4: Base64
    STANDARD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    # RFC 4648 Section 5: Base64 with URL and Filename Safe Alphabet
    URL_SAFE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    
    # RFC 4648 Section 6: Base32
    BASE32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    
    # RFC 4648 Section 8: Base16 / Hex
    HEX = "0123456789ABCDEF"
    
    # Threat Actor Samples (Historical APT custom alphabets)
    # Example 1: Reversed standard alphabet (used by simple droppers to break static signatures)
    REVERSED = "/+9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA"
    
    # Example 2: Numbers first, lowercase, uppercase (Common custom malware table)
    ALPHANUM_FIRST = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"


class CustomAlphabet:
    """
    Simulates custom alphabet substitution used by threat actors (e.g., APT29, FIN7)
    to defeat standard static YARA/AV detection signatures.
    """
    
    @staticmethod
    def generate_shuffled(seed: Optional[int] = None) -> str:
        """Generates a pseudo-random permutation of the 64 Base64 characters."""
        chars = list(Alphabets.STANDARD)
        rng = random.Random(seed)
        rng.shuffle(chars)
        return "".join(chars)

    @staticmethod
    def translate_standard_to_custom(standard_b64: str, custom_alphabet: str) -> str:
        """
        Translates a standard Base64 string into a custom alphabet representation.
        Padding '=' characters remain untouched.
        """
        if len(custom_alphabet) != 64:
            raise ValueError("Custom alphabet must contain exactly 64 unique characters.")
        
        trans_table = str.maketrans(Alphabets.STANDARD, custom_alphabet)
        return standard_b64.translate(trans_table)

    @staticmethod
    def translate_custom_to_standard(custom_b64: str, custom_alphabet: str) -> str:
        """
        Translates a custom alphabet Base64 string back into standard Base64.
        """
        if len(custom_alphabet) != 64:
            raise ValueError("Custom alphabet must contain exactly 64 unique characters.")
            
        trans_table = str.maketrans(custom_alphabet, Alphabets.STANDARD)
        return custom_b64.translate(trans_table)

    @staticmethod
    def derive_from_known_plaintext(known_bytes: bytes, custom_b64_sample: str) -> Dict[str, str]:
        """
        Demonstrates a basic known-plaintext attack against a custom alphabet:
        If you know the first bytes are an executable (e.g. 'MZ' = 'TVq'), you can deduce
        the custom characters that correspond to standard characters!
        """
        import base64
        standard_b64_prefix = base64.b64encode(known_bytes).decode('ascii')
        
        mapping = {}
        for std_char, cust_char in zip(standard_b64_prefix, custom_b64_sample):
            if std_char != '=':
                mapping[cust_char] = std_char
                
        return mapping
