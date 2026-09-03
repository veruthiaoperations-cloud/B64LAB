"""
Visual Bitwise Mastery Lesson: From Octets to Sextets.
Pure Python standard library implementation.
"""

from ..core.bitwise import BitwiseEngine, BitwiseTrace
from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI

class BitwiseLesson:
    """
    Interactive lesson breaking down the exact binary mechanics of RFC 4648 Base64:
    3 Octets (8 bits each) -> 24-bit Buffer -> 4 Sextets (6 bits each) -> Lookup Table.
    """

    @classmethod
    def run(cls) -> None:
        """Interactive bitwise lesson loop."""
        while True:
            UIComponents.header(
                "MODULE 1: BITWISE MECHANICS & BINARY TRANSFORMATION",
                "Understand Base64 at the CPU and bit-shift level (Octets to Sextets)"
            )

            print("  Base64 solves a classic computing problem:")
            print("  Many communication protocols (Email/SMTP, HTTP, JSON, XML) were built for")
            print("  7-bit or 8-bit ASCII text. Binary files (PDFs, EXEs, images) contain non-printable")
            print("  null bytes and control codes that corrupt text transmission channels.\n")

            content = [
                "THE CORE MATHEMATICAL INSIGHT:",
                "  1. Take 3 raw bytes (3 * 8 bits = 24 bits).",
                "  2. Regroup those 24 bits into 4 chunks of 6 bits each (4 * 6 bits = 24 bits).",
                "  3. Each 6-bit value ranges from 0 to 63 (2^6 = 64 combinations).",
                "  4. Map each 6-bit value to a safe printable character in the 64-character table.",
                "  5. Result: 3 raw bytes expand into 4 safe ASCII characters (33.3% size expansion)."
            ]
            UIComponents.box(content, title="24-BIT BITWISE RATIO", style="rounded")

            print("\n  [1] Walkthrough Classic Example ('Man' -> 'TWFu')")
            print("  [2] Interactive Custom Input (Type your own string and view live bit breakdown)")
            print("  [3] Padding Mechanics Deep-Dive (Why '=' and '==' exist)")
            print("  [0] Return to Academy Menu\n")

            choice = UIComponents.prompt("Select option (0-3)")
            if choice == "0":
                break
            elif choice == "1":
                cls._walkthrough_example("Man")
            elif choice == "2":
                val = input("\n  Enter text to analyze in bitwise engine: ").strip()
                if val:
                    cls._walkthrough_example(val)
                else:
                    print("  [!] Input cannot be empty.")
            elif choice == "3":
                cls._explain_padding()

    @classmethod
    def _walkthrough_example(cls, text: str) -> None:
        """Renders an aligned visual bitwise trace for any string."""
        raw_bytes = text.encode("utf-8")
        traces = BitwiseEngine.trace_encode(raw_bytes)
        palette = Theme.get_palette()
        p = palette.primary
        s = palette.secondary
        r = ANSI.RESET

        UIComponents.header(f"BITWISE TRACE: '{text}' ({len(raw_bytes)} bytes)", "Step-by-step binary transformation")

        for trace in traces:
            print(f"\n  {s}{ANSI.BOLD}─── CHUNK #{trace.chunk_index + 1} ({len(trace.raw_bytes)} bytes) ───{r}")
            
            # Step 1: Input bytes
            chars_str = "  ".join(f"'{chr(b)}'" if 32 <= b <= 126 else f"\\x{b:02X}" for b in trace.raw_bytes)
            hex_str = "   ".join(trace.raw_hex)
            bin_str = " ".join(trace.raw_binaries)
            
            print(f"  [1] Raw Input Characters :  {chars_str}")
            print(f"  [2] Hexadecimal (8-bit)  :  {hex_str}")
            print(f"  [3] Binary Octets (8-bit):  {bin_str}")
            
            # Step 2: 24-bit combined buffer
            buf_str = trace.buffer_24bit_bin
            buf_spaced = f"{buf_str[:8]} {buf_str[8:16]} {buf_str[16:]}"
            print(f"\n  [4] Combined 24-bit Buffer:")
            print(f"      {p}{buf_spaced}{r}")

            # Step 3: Regroup into 4 sextets of 6 bits
            sextet_line = " ".join(trace.sextets_bin)
            dec_line = "      ".join(f"{v:02d}" for v in trace.sextets_dec)
            print(f"\n  [5] Regroup into 4x 6-bit Sextets:")
            print(f"      {palette.accent}{sextet_line}{r}")
            print(f"      {dec_line}  (Decimal indices 0-63)")

            # Step 4: Lookup output characters
            out_chars_str = "         ".join(f"'{c}'" for c in trace.output_chars)
            print(f"\n  [6] Base64 Table Lookup:")
            print(f"      {s}{ANSI.BOLD}{out_chars_str}{r}")

            print(f"\n  Note: {trace.note}")

        final_b64 = BitwiseEngine.encode(raw_bytes)
        print(f"\n  {palette.success}{ANSI.BOLD}✓ Final Result: \"{final_b64}\"{r}")
        UIComponents.pause()

    @classmethod
    def _explain_padding(cls) -> None:
        """Explains the mathematical requirement for '=' padding."""
        UIComponents.header("THE MATHEMATICS OF PADDING ('=' and '==')", "Why padding exists and how attackers exploit it")

        lines = [
            "Input byte counts do not always divide cleanly by 3:",
            "",
            "Case A: Length % 3 == 0 (e.g., 'ABC' = 3 bytes / 24 bits)",
            "  -> Maps into exactly 4 sextets of 6 bits.",
            "  -> Zero padding characters needed. Output ends without '='.",
            "",
            "Case B: Length % 3 == 2 (e.g., 'AB' = 2 bytes / 16 bits)",
            "  -> 16 bits = two 6-bit sextets (12 bits) + 4 remaining bits.",
            "  -> 2 zero bits are padded on the right to make the 3rd 6-bit sextet.",
            "  -> Exactly ONE '=' is added to reach the required 4-character block.",
            "  -> Example: 'AB' -> 'QUI='",
            "",
            "Case C: Length % 3 == 1 (e.g., 'A' = 1 byte / 8 bits)",
            "  -> 8 bits = one 6-bit sextet + 2 remaining bits.",
            "  -> 4 zero bits are padded on the right to make the 2nd 6-bit sextet.",
            "  -> Exactly TWO '==' characters are added to complete the 4-char block.",
            "  -> Example: 'A' -> 'QQ=='",
            "",
            "DEFENSIVE GOTCHA (The Regex Padding Bypass):",
            "  Many intrusion detection rules (Snort/Suricata) search for Base64 using regexes",
            "  that demand valid padding at the end. Attackers purposely strip trailing '='",
            "  characters! Robust forensic tools automatically re-pad unpadded strings."
        ]
        UIComponents.box(lines, title="PADDING MATRIX", style="double")
        UIComponents.pause()
