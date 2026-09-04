"""
RFC 4648 Standards and Encoding Variants Lesson.
Pure Python standard library implementation.
"""

from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI

class RFCLesson:
    """
    Deconstructs the official RFC 4648 specifications:
    Base64, Base64URL, Base32, and Base16 variants.
    """

    @classmethod
    def run(cls) -> None:
        while True:
            UIComponents.header(
                "MODULE 2: RFC 4648 STANDARDS & ENCODING ECOSYSTEM",
                "Deep dive into RFC 4648: Base64, Base64URL, Base32, and Hex"
            )

            print("  RFC 4648 is the official IETF standard defining binary-to-text encodings.\n")

            headers = ["STANDARD", "CHUNK", "ALPHABET", "PADDING", "PRIMARY USE CASE"]
            rows = [
                ["Base64", "6-bit", "A-Z, a-z, 0-9, +, /", "Required (=)", "MIME, Certs, PEM"],
                ["Base64URL", "6-bit", "A-Z, a-z, 0-9, -, _", "Optional", "JWTs, URLs, Parameters"],
                ["Base32", "5-bit", "A-Z, 2-7", "Required (=)", "TOTP / 2FA, DNS Tunnels"],
                ["Base16 (Hex)", "4-bit", "0-9, A-F", "None", "Hashes (MD5, SHA), Hex"],
            ]
            UIComponents.table(headers, rows)

            print("\n  [1] Why Base64URL was Created (Web Application Security & JWTs)")
            print("  [2] Base32: Why Malware Uses It for DNS Tunneling & C2")
            print("  [3] Padding Specification Matrix (RFC 4648 Section 4.3)")
            print("  [0] Return to Academy Menu\n")

            choice = UIComponents.prompt("Select option (0-3)")
            if choice == "0":
                break
            elif choice == "1":
                cls._explain_base64url()
            elif choice == "2":
                cls._explain_base32_dns()
            elif choice == "3":
                cls._explain_padding_matrix()

    @classmethod
    def _explain_base64url(cls) -> None:
        UIComponents.header("BASE64URL: WEB APPLICATION SECURITY & JWT TOKENS")
        lines = [
            "THE PROBLEM WITH STANDARD BASE64 IN WEB APPS:",
            "  Standard Base64 contains two problematic characters: '+' and '/'.",
            "  1. In URL query strings, '+' is interpreted as a space by web servers.",
            "  2. The '/' character is a URL path delimiter.",
            "  3. In file systems, '/' represents directory separation.",
            "",
            "RFC 4648 SECTION 5 RESOLUTION (Base64URL):",
            "  - Replaces '+' with '-' (dash)",
            "  - Replaces '/' with '_' (underscore)",
            "  - Often omits padding '=' altogether to avoid URL percent-encoding (%3D).",
            "",
            "WHERE YOU SEE THIS IN REAL SECURITY:",
            "  JSON Web Tokens (JWT) consist of three Base64URL strings separated by dots:",
            "  [Header].[Payload].[Signature]",
            "  When inspecting JWTs in Burp Suite or during pentesting, they are Base64URL!",
        ]
        UIComponents.box(lines, title="BASE64URL ESSENTIALS", style="rounded")
        UIComponents.pause()

    @classmethod
    def _explain_base32_dns(cls) -> None:
        UIComponents.header("BASE32: DNS EXFILTRATION & COMMAND-AND-CONTROL (C2)")
        lines = [
            "WHY ATTACKERS CHOOSE BASE32 FOR DNS TUNNELING:",
            "  1. DNS is strictly case-insensitive. Standard Base64 requires uppercase",
            "     and lowercase distinction ('a' vs 'A'). Over DNS, 'a' and 'A' collide!",
            "  2. Base32 (RFC 4648 Sec 6) uses only uppercase A-Z and digits 2-7.",
            "  3. It avoids digits 0, 1, and 8 to prevent visual confusion with O, I, and B.",
            "",
            "THE ATTACK PATTERN (MITRE T1071.004):",
            "  Attacker chunks an exfiltrated file into Base32 blocks and requests:",
            "  stage1.<base32_blob_here>.attacker-c2.com",
            "  The attacker's authoritative DNS nameserver logs the query and decodes the file!",
            "",
            "DEFENSIVE MITIGATION:",
            "  SOC analysts monitor DNS query length anomalies and high entropy in subdomains."
        ]
        UIComponents.box(lines, title="BASE32 IN DNS TUNNELING", style="rounded")
        UIComponents.pause()

    @classmethod
    def _explain_padding_matrix(cls) -> None:
        UIComponents.header("RFC 4648 PADDING COMPLIANCE MATRIX")
        headers = ["SCHEME", "BITS/CHAR", "INPUT MULTIPLE", "OUTPUT BLOCK", "VALID PADDING LENGTHS"]
        rows = [
            ["Base64", "6 bits", "3 bytes (24b)", "4 characters", "0, 1 ('='), 2 ('==')"],
            ["Base32", "5 bits", "5 bytes (40b)", "8 characters", "0, 1, 3, 4, 6 ('=')"],
            ["Base16", "4 bits", "1 byte (8b)", "2 characters", "0 (No padding)"],
        ]
        UIComponents.table(headers, rows)
        UIComponents.pause()
