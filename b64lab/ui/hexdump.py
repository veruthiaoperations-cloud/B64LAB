"""
Canonical Hex Dump Engine with Syntax Highlighting.
Pure Python standard library implementation.
"""

from typing import List, Optional
from .ansi import ANSI, Terminal
from .themes import Theme

class HexViewer:
    """
    Renders binary data in standard forensic hex dump format:
    Offset (00000000) | Hex representation (8 or 16 bytes) | ASCII representation
    """

    @classmethod
    def render(
        cls,
        data: bytes,
        max_bytes: int = 256,
        color: bool = True,
        bytes_per_line: Optional[int] = None,
    ) -> str:
        """Formats bytes into a canonical hex dump string, adapting responsively to width."""
        if not data:
            return "  [EMPTY DATA BUFFER]"

        palette = Theme.get_palette()
        p = palette.primary
        d = palette.dim
        s = palette.secondary
        t = palette.text
        r = ANSI.RESET if color else ""

        if bytes_per_line is None:
            bytes_per_line = 8 if Terminal.get_width() < 72 else 16

        lines = []
        truncated = len(data) > max_bytes
        view_data = data[:max_bytes]

        # Header
        if bytes_per_line == 8:
            header = f"  {d}OFFSET    00 01 02 03 04 05 06 07   |ASCII   |{r}"
            lines.append(header)
            lines.append(f"  {d}────────  ────────────────────────  +────────+{r}")
        else:
            header = f"  {d}OFFSET    00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F  |ASCII           |{r}"
            lines.append(header)
            lines.append(f"  {d}────────  ────────────────────────────────────────────────  +────────────────+{r}")

        for offset in range(0, len(view_data), bytes_per_line):
            chunk = view_data[offset:offset + bytes_per_line]
            offset_str = f"  {p}{offset:08X}{r} "

            hex_parts_1 = []
            hex_parts_2 = []
            ascii_parts = []

            for i in range(bytes_per_line):
                if i < len(chunk):
                    b = chunk[i]
                    if color:
                        if b == 0x00:
                            hex_str = f"{d}00{r}"
                        elif 0x20 <= b <= 0x7E:
                            hex_str = f"{s}{b:02X}{r}"
                        elif b in [0x4D, 0x5A, 0x7F, 0x45, 0x4C, 0x46]: # Potential magic byte
                            hex_str = f"{ANSI.BOLD}{ANSI.BRIGHT_YELLOW}{b:02X}{r}"
                        else:
                            hex_str = f"{t}{b:02X}{r}"
                    else:
                        hex_str = f"{b:02X}"

                    if 0x20 <= b <= 0x7E:
                        ascii_str = f"{s}{chr(b)}{r}" if color else chr(b)
                    else:
                        ascii_str = f"{d}.{r}" if color else "."
                else:
                    hex_str = "  "
                    ascii_str = " "

                if bytes_per_line == 8 or i < 8:
                    hex_parts_1.append(hex_str)
                else:
                    hex_parts_2.append(hex_str)
                ascii_parts.append(ascii_str)

            if bytes_per_line == 8:
                hex_line = " ".join(hex_parts_1)
            else:
                hex_line = " ".join(hex_parts_1) + "  " + " ".join(hex_parts_2)
            ascii_line = "".join(ascii_parts)
            lines.append(f"{offset_str} {hex_line}  |{ascii_line}|")

        if truncated:
            lines.append(f"  {d}... [Truncated {len(data) - max_bytes} bytes. Displaying first {max_bytes} bytes] ...{r}")

        return "\n".join(lines)
